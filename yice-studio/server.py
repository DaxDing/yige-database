#!/usr/bin/env python3
"""YICE 数据服务

提供 ADS 报表（MaxCompute）和一致性检查（PostgreSQL）的 API 接口。

启动:
    export $(cat .env | xargs) && python3 yice-studio/server.py [port]
"""

import gzip as gzip_mod
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from decimal import Decimal
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs, urlencode

import psycopg2
import psycopg2.extras
from odps import ODPS

from settings import (
    STUDIO_DIR, PROJECT_ROOT, CONFIG_DIR, SERVER, CACHE,
    MAXCOMPUTE, ADS_TABLES, POSTGRES, FEISHU, GLM, API_ROUTES, check_env,
)

# ── 缓存 ──

_cache = {}
_cache_lock = threading.Lock()
_odps = None
_DS_RE = re.compile(r'^\d{8}$')


def _get_cache(key):
    with _cache_lock:
        entry = _cache.get(key)
        if entry and time.time() - entry['ts'] < CACHE['ttl']:
            return entry['data']
    return None


def _get_cache_bytes(key, accept_gzip=False):
    """返回预序列化 bytes，跳过 json.dumps"""
    with _cache_lock:
        entry = _cache.get(key)
        if entry and time.time() - entry['ts'] < CACHE['ttl']:
            if accept_gzip and entry.get('gz'):
                return entry['gz'], True
            return entry.get('jb'), False
    return None, False


def _set_cache(key, data):
    with _cache_lock:
        if len(_cache) >= CACHE['max_entries']:
            oldest = min(_cache, key=lambda k: _cache[k]['ts'])
            del _cache[oldest]
        jb = json.dumps(data, ensure_ascii=False).encode('utf-8')
        gz = gzip_mod.compress(jb, compresslevel=6) if len(jb) > 1024 else None
        _cache[key] = {'ts': time.time(), 'data': data, 'jb': jb, 'gz': gz}


def _clear_cache():
    with _cache_lock:
        _cache.clear()


def _warm_cache():
    """清空缓存并重新预热所有数据"""
    _clear_cache()
    print(f'[{datetime.now():%H:%M}] 开始缓存预热…')
    # 默认日期范围（与前端一致：T-9 ~ T-1）
    today = datetime.now()
    end_ds = (today - timedelta(days=1)).strftime('%Y%m%d')
    start_ds = (today - timedelta(days=9)).strftime('%Y%m%d')
    tasks = [
        ('ads', lambda: query_ads(start_ds, end_ds)),
        ('project_names', lambda: query_project_names()),
        ('cherk', lambda: query_cherk()),
        ('dim_stats', lambda: query_dim_stats()),
        ('feishu_depts', lambda: query_feishu_departments('0', recursive=True)),
        ('feishu_emps', lambda: query_feishu_employees()),
    ]
    for name, fn in tasks:
        try:
            fn()
            print(f'  ✓ {name}')
        except Exception as e:
            print(f'  ✗ {name}: {e}')
    print(f'[{datetime.now():%H:%M}] 缓存预热完成')


def _schedule_nightly_refresh():
    """每天凌晨 3:00 清空并预热缓存"""
    def _run():
        while True:
            now = datetime.now()
            target = now.replace(hour=3, minute=0, second=0, microsecond=0)
            if target <= now:
                target += timedelta(days=1)
            time.sleep((target - now).total_seconds())
            _warm_cache()
    t = threading.Thread(target=_run, daemon=True)
    t.start()


# ── MaxCompute ──

def get_odps():
    global _odps
    if _odps is None:
        mc = MAXCOMPUTE
        if not mc['access_key_id'] or not mc['access_key_secret']:
            raise RuntimeError('ALIYUN_ACCESS_KEY_ID / SECRET 未配置')
        _odps = ODPS(
            mc['access_key_id'], mc['access_key_secret'],
            project=mc['project'],
            endpoint=mc['endpoint'],
        )
    return _odps


def serialize(val):
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    return val


def _validate_ds(ds):
    if not _DS_RE.match(ds):
        raise ValueError(f'日期格式错误: {ds}，需要 YYYYMMDD')


def query_mc_table(key, start_ds, end_ds):
    _validate_ds(start_ds)
    _validate_ds(end_ds)
    cfg = ADS_TABLES[key]
    sql = (
        f"SELECT * FROM {cfg['name']} "
        f"WHERE ds >= '{start_ds}' AND ds <= '{end_ds}' "
        f"ORDER BY {cfg['order']};"
    )
    o = get_odps()
    with o.execute_sql(sql).open_reader() as reader:
        col_names = [c.name for c in reader._schema.columns]
        return [
            {name: serialize(record[name]) for name in col_names}
            for record in reader
        ]


def query_ads_table(table, start_ds, end_ds, refresh=False):
    """查询单张 ADS 表（支持缓存）"""
    cache_key = f'ads_{table}_{start_ds}_{end_ds}'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached is not None:
            return cached

    print(f'  查询 {ADS_TABLES[table]["name"]}: ds {start_ds} ~ {end_ds} ...', flush=True)
    t0 = time.time()
    rows = query_mc_table(table, start_ds, end_ds)
    elapsed = time.time() - t0
    print(f'  完成: {len(rows)} rows, {elapsed:.1f}s', flush=True)

    result = {
        'table': table,
        'rows': rows,
        'count': len(rows),
        'query_seconds': round(elapsed, 1),
    }
    _set_cache(cache_key, result)
    return result


def query_ads(start_ds, end_ds, refresh=False):
    cache_key = f'ads_{start_ds}_{end_ds}'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached:
            return cached

    print(f'  查询 MaxCompute: ds {start_ds} ~ {end_ds} ...', flush=True)
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            key: executor.submit(query_mc_table, key, start_ds, end_ds)
            for key in ADS_TABLES
        }
        result = {}
        errors = {}
        for key, fut in futures.items():
            try:
                result[key] = fut.result()
            except Exception as e:
                errors[key] = str(e)
                result[key] = []

    elapsed = time.time() - t0
    meta = {
        'queried_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': {
            'start': f'{start_ds[:4]}-{start_ds[4:6]}-{start_ds[6:8]}',
            'end': f'{end_ds[:4]}-{end_ds[4:6]}-{end_ds[6:8]}',
        },
        'tables': {k: len(v) for k, v in result.items()},
        'query_seconds': round(elapsed, 1),
    }
    if errors:
        meta['errors'] = errors

    try:
        pnames = query_project_names()
    except Exception:
        pnames = {}

    data = {'meta': meta, 'project_names': pnames, **result}
    if not errors:
        _set_cache(cache_key, data)

    total = sum(len(v) for v in result.values())
    print(f'  完成: {total} rows, {elapsed:.1f}s', flush=True)
    return data


# ── PostgreSQL ──

def query_project_names():
    cached = _get_cache('project_names')
    if cached:
        return cached
    with psycopg2.connect(**POSTGRES['cherk']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                'SELECT DISTINCT project_id, project_name '
                'FROM cherk_xhs_data_check_df WHERE project_name IS NOT NULL'
            )
            rows = cur.fetchall()
    mapping = {r['project_id']: r['project_name'] for r in rows}
    _set_cache('project_names', mapping)
    return mapping


def query_cherk(refresh=False):
    cache_key = 'cherk'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached:
            return cached

    print('  查询 PostgreSQL: cherk_xhs_data_check_df ...', flush=True)
    t0 = time.time()

    with psycopg2.connect(**POSTGRES['cherk']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                'SELECT * FROM cherk_xhs_data_check_df '
                'ORDER BY dt DESC, project_id, cherk_source'
            )
            rows = cur.fetchall()

    result = []
    for r in rows:
        row = {}
        for k, v in r.items():
            if isinstance(v, datetime):
                row[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(v, Decimal):
                row[k] = float(v)
            else:
                row[k] = v
        result.append(row)

    elapsed = time.time() - t0
    data = {
        'meta': {
            'queried_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': len(result),
            'query_seconds': round(elapsed, 2),
        },
        'rows': result,
    }

    _set_cache(cache_key, data)
    print(f'  完成: {len(result)} rows, {elapsed:.2f}s', flush=True)
    return data


# ── 维度基准查询 ──

def query_dim_stats(refresh=False):
    cache_key = 'dim_stats'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached is not None:
            return cached

    print('  查询 PostgreSQL(sync_dim): 维度基准统计 ...', flush=True)
    t0 = time.time()

    stats = {}  # project_id → { note: {total, active}, ... }

    with psycopg2.connect(**POSTGRES['dim']) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('''
                SELECT b.project_id,
                       COUNT(DISTINCT CASE WHEN b.is_proxy = 'f' THEN b.note_id END) AS total,
                       COUNT(DISTINCT CASE WHEN b.is_backlink = 't' THEN b.note_id END) AS active
                FROM brg_xhs_note_project_df b
                WHERE b.project_id IS NOT NULL
                GROUP BY b.project_id
            ''')
            for r in cur.fetchall():
                pid = r['project_id']
                stats.setdefault(pid, {})
                stats[pid]['note'] = {'total': r['total'], 'active': r['active']}

            cur.execute('''
                SELECT project_id,
                       COUNT(DISTINCT task_group_id) AS total,
                       COUNT(DISTINCT CASE WHEN task_auth_status IS NOT NULL THEN task_group_id END) AS active
                FROM dim_xhs_task_group_df
                WHERE project_id IS NOT NULL
                GROUP BY project_id
            ''')
            for r in cur.fetchall():
                pid = r['project_id']
                stats.setdefault(pid, {})
                stats[pid]['task_group'] = {'total': r['total'], 'active': r['active']}

            cur.execute('''
                SELECT project_id,
                       COUNT(DISTINCT creativity_id) AS total,
                       COUNT(DISTINCT CASE WHEN creativity_status IS NOT NULL THEN creativity_id END) AS active
                FROM dim_xhs_creativity_df
                WHERE project_id IS NOT NULL
                GROUP BY project_id
            ''')
            for r in cur.fetchall():
                pid = r['project_id']
                stats.setdefault(pid, {})
                stats[pid]['creative'] = {'total': r['total'], 'active': r['active']}

            cur.execute('''
                SELECT project_id,
                       COUNT(DISTINCT keyword_id) AS total
                FROM dim_xhs_keyword_df
                WHERE project_id IS NOT NULL
                GROUP BY project_id
            ''')
            for r in cur.fetchall():
                pid = r['project_id']
                stats.setdefault(pid, {})
                stats[pid]['keyword'] = {'total': r['total'], 'active': 0}

            cur.execute('''
                SELECT project_id,
                       COUNT(DISTINCT target_id) AS total
                FROM dim_xhs_target_df
                WHERE project_id IS NOT NULL
                GROUP BY project_id
            ''')
            for r in cur.fetchall():
                pid = r['project_id']
                stats.setdefault(pid, {})
                stats[pid]['target'] = {'total': r['total'], 'active': 0}

            cur.execute('''
                SELECT project_id,
                       COUNT(DISTINCT advertiser_id) AS total
                FROM dim_xhs_advertiser_df
                WHERE project_id IS NOT NULL
                GROUP BY project_id
            ''')
            for r in cur.fetchall():
                pid = r['project_id']
                stats.setdefault(pid, {})
                stats[pid]['account'] = {'total': r['total']}

    elapsed = time.time() - t0
    data = {
        'meta': {
            'queried_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'query_seconds': round(elapsed, 2),
        },
        'stats': stats,
    }

    _set_cache(cache_key, data)
    print(f'  完成: {len(stats)} projects, {elapsed:.2f}s', flush=True)
    return data


# ── 飞书 API ──

def _feishu_tenant_token():
    """获取飞书 tenant_access_token"""
    cached = _get_cache('feishu_token')
    if cached:
        return cached

    fs = FEISHU
    url = f"{fs['base_url']}/auth/v3/tenant_access_token/internal"
    body = json.dumps({
        'app_id': fs['app_id'],
        'app_secret': fs['app_secret'],
    }).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    if data.get('code') != 0:
        raise RuntimeError(f"飞书认证失败: {data.get('msg')}")
    token = data['tenant_access_token']
    _set_cache('feishu_token', token)
    return token


def _feishu_get(path, params=None):
    """飞书 GET 请求"""
    token = _feishu_tenant_token()
    url = f"{FEISHU['base_url']}{path}"
    if params:
        url += '?' + urlencode(params)
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        code = body.get('code', '')
        msg = body.get('msg', '')
        if code == 99991672:
            raise RuntimeError('飞书应用缺少通讯录权限，请到飞书开放平台开通 contact:contact:readonly_as_app')
        raise RuntimeError(f'飞书 API 错误 {code}: {msg}')


def _feishu_list_departments(parent_id='0'):
    """查询飞书某一层级的部门"""
    all_depts = []
    page_token = None
    while True:
        params = {'department_id_type': 'open_department_id', 'parent_department_id': parent_id, 'page_size': '50'}
        if page_token:
            params['page_token'] = page_token
        data = _feishu_get('/contact/v3/departments', params)
        if data.get('code') != 0:
            raise RuntimeError(f"飞书部门查询失败: {data.get('msg')}")
        items = data.get('data', {}).get('items', [])
        all_depts.extend(items)
        if not data.get('data', {}).get('has_more'):
            break
        page_token = data['data'].get('page_token')
    return all_depts


def _format_dept(d):
    return {
        'department_id': d.get('open_department_id', ''),
        'name': d.get('name', ''),
        'parent_id': d.get('parent_department_id', ''),
        'leader_user_id': d.get('leader_user_id', ''),
        'member_count': d.get('member_count', 0),
        'status': d.get('status', {}),
    }


def query_feishu_departments(parent_id='0', recursive=False, refresh=False):
    """查询飞书部门列表，recursive=True 递归获取所有子部门"""
    cache_key = f'feishu_dept_{parent_id}_{"r" if recursive else "f"}'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached is not None:
            return cached

    print(f'  查询飞书部门: parent={parent_id} recursive={recursive} ...', flush=True)
    top_depts = _feishu_list_departments(parent_id)
    result = [_format_dept(d) for d in top_depts]

    if recursive:
        queue = [d.get('open_department_id', '') for d in top_depts]
        while queue:
            pid = queue.pop(0)
            children = _feishu_list_departments(pid)
            for c in children:
                result.append(_format_dept(c))
                queue.append(c.get('open_department_id', ''))

    _set_cache(cache_key, result)
    print(f'  完成: {len(result)} departments', flush=True)
    return result


def _feishu_list_users(department_id=None):
    """查询飞书某部门的直属员工"""
    all_users = []
    page_token = None
    while True:
        params = {'department_id_type': 'open_department_id', 'page_size': '50'}
        if department_id:
            params['department_id'] = department_id
        if page_token:
            params['page_token'] = page_token
        data = _feishu_get('/contact/v3/users', params)
        if data.get('code') != 0:
            raise RuntimeError(f"飞书员工查询失败: {data.get('msg')}")
        items = data.get('data', {}).get('items', [])
        all_users.extend(items)
        if not data.get('data', {}).get('has_more'):
            break
        page_token = data['data'].get('page_token')
    return all_users


def _format_user(u):
    return {
        'user_id': u.get('user_id', ''),
        'open_id': u.get('open_id', ''),
        'name': u.get('name', ''),
        'en_name': u.get('en_name', ''),
        'email': u.get('email', ''),
        'mobile': u.get('mobile', ''),
        'avatar': u.get('avatar', {}).get('avatar_72', ''),
        'department_ids': u.get('department_ids', []),
        'status': u.get('status', {}),
        'job_title': u.get('job_title', ''),
    }


def query_feishu_employees(department_id=None, refresh=False):
    """查询飞书员工列表。department_id=None 时递归查询全部部门员工"""
    cache_key = f'feishu_emp_{department_id or "all"}'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached is not None:
            return cached

    print(f'  查询飞书员工: dept={department_id or "全部"} ...', flush=True)

    if department_id:
        raw = _feishu_list_users(department_id)
        result = [_format_user(u) for u in raw]
    else:
        # 递归所有部门获取全量员工，按 open_id 去重
        depts = query_feishu_departments(parent_id='0', recursive=True)
        seen = set()
        result = []
        # 先查根部门直属
        for u in _feishu_list_users():
            fu = _format_user(u)
            if fu['open_id'] not in seen:
                seen.add(fu['open_id'])
                result.append(fu)
        # 再查每个子部门
        for dept in depts:
            for u in _feishu_list_users(dept['department_id']):
                fu = _format_user(u)
                if fu['open_id'] not in seen:
                    seen.add(fu['open_id'])
                    result.append(fu)

    _set_cache(cache_key, result)
    print(f'  完成: {len(result)} employees', flush=True)
    return result


# ── Config 读写 ──

def _read_config(name):
    path = os.path.join(CONFIG_DIR, name)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write_config(name, data):
    path = os.path.join(CONFIG_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── HTTP Handler ──

R = API_ROUTES  # 路由别名


class APIHandler(SimpleHTTPRequestHandler):

    # ── CORS ──

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _read_body(self, max_size=SERVER['max_body']):
        length = int(self.headers.get('Content-Length', 0))
        if length > max_size:
            raise ValueError(f'请求体过大: {length} > {max_size}')
        return self.rfile.read(length)

    # ── POST ──

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path == R['chat']:
                self.handle_chat()
            elif parsed.path == R['projects_save']:
                data = json.loads(self._read_body())
                _write_config('projects.json', data)
                self.send_json(200, {'ok': True})
            elif parsed.path == R['accounts_save']:
                data = json.loads(self._read_body())
                _write_config('accounts.json', data)
                self.send_json(200, {'ok': True})
            else:
                self.send_error(404)
        except ValueError as e:
            self.send_json(400, {'error': str(e)})
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def handle_chat(self):
        """流式代理 GLM API（纯 Python urllib，无子进程）"""
        try:
            body = json.loads(self._read_body(100 * 1024))
            messages = body.get('messages', [])
            if not messages:
                self.send_json(400, {'error': 'messages required'})
                return

            payload = json.dumps({
                'model': GLM['model'],
                'messages': messages[-20:],
                'stream': True,
            }, ensure_ascii=False).encode('utf-8')

            req = urllib.request.Request(
                GLM['url'], data=payload,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {GLM["key"]}',
                },
            )

            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('X-Accel-Buffering', 'no')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    while True:
                        line = resp.readline()
                        if not line:
                            break
                        self.wfile.write(line)
                        self.wfile.flush()
            except BrokenPipeError:
                pass
        except urllib.error.HTTPError as e:
            err = e.read().decode() if e.fp else str(e)
            try:
                self.send_json(e.code, {'error': err})
            except Exception:
                pass
        except Exception as e:
            try:
                self.send_json(500, {'error': str(e)})
            except Exception:
                pass

    # ── GET ──

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == R['ads']:
            self.handle_ads(parsed)
        elif path == R['project_names']:
            try:
                self.send_json(200, query_project_names())
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == R['cherk']:
            self.handle_cherk(parsed)
        elif path == R['feishu_departments']:
            params = parse_qs(parsed.query)
            parent_id = params.get('parent_id', ['0'])[0]
            recursive = params.get('recursive', ['0'])[0] == '1'
            refresh = params.get('refresh', ['0'])[0] == '1'
            try:
                depts = query_feishu_departments(parent_id, recursive=recursive, refresh=refresh)
                self.send_json(200, {'departments': depts})
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == R['feishu_employees']:
            params = parse_qs(parsed.query)
            dept_id = params.get('department_id', [None])[0]
            refresh = params.get('refresh', ['0'])[0] == '1'
            try:
                emps = query_feishu_employees(dept_id, refresh=refresh)
                self.send_json(200, {'employees': emps})
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == R['feishu_config']:
            app_id = FEISHU['app_id']
            secret = FEISHU['app_secret']
            masked = secret[:4] + '****' + secret[-4:] if len(secret) > 8 else '****'
            self.send_json(200, {'app_id': app_id, 'secret_masked': masked, 'secret': secret})
        elif path == R['dim_stats']:
            params = parse_qs(parsed.query)
            refresh = 'refresh' in params
            try:
                self.send_json(200, query_dim_stats(refresh))
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == '/':
            self.send_response(302)
            self.send_header('Location', SERVER['default_redirect'])
            self.end_headers()
        elif path in ('/projects.json', '/accounts.json'):
            name = os.path.basename(path)
            try:
                self.send_json(200, _read_config(name))
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        else:
            super().do_GET()

    def handle_ads(self, parsed):
        params = parse_qs(parsed.query)
        today = datetime.now()
        default_end = today - timedelta(days=1)
        default_start = default_end - timedelta(days=8)
        start = params.get('start', [default_start.strftime('%Y%m%d')])[0].replace('-', '')
        end = params.get('end', [default_end.strftime('%Y%m%d')])[0].replace('-', '')
        refresh = params.get('refresh', ['0'])[0] == '1'
        table = params.get('table', [None])[0]
        counts_only = params.get('counts', ['0'])[0] == '1'
        try:
            _validate_ds(start)
            _validate_ds(end)
            if counts_only:
                counts = {}
                for key in ADS_TABLES:
                    cached = _get_cache(f'ads_{key}_{start}_{end}')
                    counts[key] = cached['count'] if cached else 0
                self.send_json(200, {'counts': counts})
                return
            if table and table in ADS_TABLES:
                cache_key = f'ads_{table}_{start}_{end}'
                if not refresh and self.send_cached(200, cache_key):
                    return
                data = query_ads_table(table, start, end, refresh)
            else:
                cache_key = f'ads_{start}_{end}'
                if not refresh and self.send_cached(200, cache_key):
                    return
                data = query_ads(start, end, refresh)
            self.send_json(200, data)
        except ValueError as e:
            self.send_json(400, {'error': str(e)})
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def handle_cherk(self, parsed):
        params = parse_qs(parsed.query)
        refresh = params.get('refresh', ['0'])[0] == '1'
        try:
            data = query_cherk(refresh)
            self.send_json(200, data)
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        is_gz = False
        if 'gzip' in self.headers.get('Accept-Encoding', '') and len(body) > 1024:
            body = gzip_mod.compress(body, compresslevel=6)
            is_gz = True
        self._write_json_response(code, body, is_gz)

    def send_cached(self, code, cache_key):
        """发送预序列化缓存，跳过 json.dumps + gzip"""
        accept_gz = 'gzip' in self.headers.get('Accept-Encoding', '')
        body, is_gz = _get_cache_bytes(cache_key, accept_gz)
        if body:
            self._write_json_response(code, body, is_gz)
            return True
        return False

    def _write_json_response(self, code, body, is_gzip=False):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        if is_gzip:
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        if '/api/' in str(args[0]):
            super().log_message(fmt, *args)


class ThreadedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


# ── Startup ──

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else SERVER['port']

    os.chdir(STUDIO_DIR)

    print(f'YICE Data Studio: http://localhost:{port}')
    for key, route in API_ROUTES.items():
        print(f'  {route}')
    warns = check_env()
    for w in warns:
        print(f'  ⚠ {w}')

    _schedule_nightly_refresh()
    # 启动后台预热缓存（不阻塞服务）
    threading.Thread(target=_warm_cache, daemon=True).start()
    server = ThreadedServer((SERVER['host'], port), APIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')
