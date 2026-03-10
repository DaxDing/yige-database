#!/usr/bin/env python3
"""YICE 数据服务

提供 ADS 报表（MaxCompute）和一致性检查（PostgreSQL）的 API 接口。

启动:
    export $(cat .env | xargs) && python3 yice-studio/server.py [port]
"""

import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from decimal import Decimal
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

# ── 路径 ──

STUDIO_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(STUDIO_DIR)
CONFIG_DIR = os.path.join(STUDIO_DIR, 'config')

# ── MaxCompute ADS 表 ──

ADS_TABLES = {
    'project': {
        'name': 'ads_xhs_project_bycontent_daily_agg',
        'order': 'ds, project_id, attribution_period',
    },
    'note': {
        'name': 'ads_xhs_note_bycontent_daily_agg',
        'order': 'ds, project_id, attribution_period, note_id',
    },
    'content_theme': {
        'name': 'ads_xhs_content_theme_bycontent_daily_agg',
        'order': 'ds, project_id, attribution_period, content_theme',
    },
    'task_group': {
        'name': 'ads_xhs_task_group_bytask_daily_agg',
        'order': 'ds, attribution_period, ad_product_name, task_group_name',
    },
}

# ── PostgreSQL 一致性检查 ──

CHERK_DB = {
    'host': os.environ.get('DB_HOST', ''),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'dbname': 'data_cherk',
    'user': os.environ.get('DB_USER', ''),
    'password': os.environ.get('DB_PASSWORD', ''),
}

# ── PostgreSQL 维度基准 ──

DIM_DB = {
    'host': os.environ.get('DB_HOST', ''),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'dbname': 'sync_dim',
    'user': os.environ.get('DB_USER', ''),
    'password': os.environ.get('DB_PASSWORD', ''),
}

# ── 缓存 ──

CACHE_TTL = 3600  # 1 小时
CACHE_MAX = 64    # 最大条目数

_cache = {}
_cache_lock = threading.Lock()
_odps = None

_DS_RE = re.compile(r'^\d{8}$')


def _get_cache(key):
    with _cache_lock:
        entry = _cache.get(key)
        if entry and time.time() - entry['ts'] < CACHE_TTL:
            return entry['data']
    return None


def _set_cache(key, data):
    with _cache_lock:
        if len(_cache) >= CACHE_MAX:
            oldest = min(_cache, key=lambda k: _cache[k]['ts'])
            del _cache[oldest]
        _cache[key] = {'ts': time.time(), 'data': data}


# ── MaxCompute ──

def get_odps():
    global _odps
    if _odps is None:
        ak = os.environ.get('ALIYUN_ACCESS_KEY_ID', '')
        sk = os.environ.get('ALIYUN_ACCESS_KEY_SECRET', '')
        if not ak or not sk:
            raise RuntimeError('ALIYUN_ACCESS_KEY_ID / SECRET 未配置')
        _odps = ODPS(
            ak, sk,
            project='df_ch_530486',
            endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api',
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
    with psycopg2.connect(**CHERK_DB) as conn:
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

    with psycopg2.connect(**CHERK_DB) as conn:
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

    with psycopg2.connect(**DIM_DB) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # 笔记: total=执行笔记(is_proxy='f'), active=复用笔记标记(is_backlink='t')
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

            # 任务组: total=全部, active=有 task_auth_status
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

            # 创意: total=全部, active=有效(creativity_status有值)
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

            # 关键词: total=关键词数, active=0(无搜索词维度)
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

            # 定向: total=定向包数, active=0
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

            # 投流账户: total=账户数
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

MAX_BODY = 1 * 1024 * 1024  # 1 MB

import psycopg2
import psycopg2.extras
from odps import ODPS


class APIHandler(SimpleHTTPRequestHandler):
    _chat_first = True
    _chat_lock = threading.Lock()
    _chat_busy = False

    # ── CORS ──

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _read_body(self, max_size=MAX_BODY):
        length = int(self.headers.get('Content-Length', 0))
        if length > max_size:
            raise ValueError(f'请求体过大: {length} > {max_size}')
        return self.rfile.read(length)

    # ── POST ──

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path == '/api/chat':
                self.handle_chat()
            elif parsed.path == '/api/chat/reset':
                with APIHandler._chat_lock:
                    APIHandler._chat_first = True
                self.send_json(200, {'ok': True})
            elif parsed.path == '/api/projects/save':
                data = json.loads(self._read_body())
                _write_config('projects.json', data)
                self.send_json(200, {'ok': True})
            elif parsed.path == '/api/accounts/save':
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
        with APIHandler._chat_lock:
            if APIHandler._chat_busy:
                self.send_json(429, {'error': '正在处理中，请稍后'})
                return
            APIHandler._chat_busy = True

        try:
            body = json.loads(self._read_body(100 * 1024))
            message = body.get('message', '')

            args = ['claude', '--pipe', '--output-format', 'stream-json']
            if not APIHandler._chat_first:
                args.append('--continue')

            env = {k: v for k, v in os.environ.items() if k != 'CLAUDECODE'}
            proc = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=PROJECT_ROOT,
                env=env,
            )

            proc.stdin.write(message.encode('utf-8'))
            proc.stdin.close()

            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            try:
                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    line = line.decode('utf-8').strip()
                    if not line:
                        continue
                    try:
                        evt = json.loads(line)
                        if evt.get('type') == 'content_block_delta':
                            delta = evt.get('delta', {})
                            if delta.get('type') == 'text_delta':
                                sse = f"data: {json.dumps({'text': delta['text']}, ensure_ascii=False)}\n\n"
                                self.wfile.write(sse.encode('utf-8'))
                                self.wfile.flush()
                    except (json.JSONDecodeError, KeyError):
                        pass
            except BrokenPipeError:
                proc.kill()

            proc.wait()
            APIHandler._chat_first = False

            try:
                self.wfile.write(b'data: [DONE]\n\n')
                self.wfile.flush()
            except BrokenPipeError:
                pass

        finally:
            with APIHandler._chat_lock:
                APIHandler._chat_busy = False

    # ── GET ──

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/ads':
            self.handle_ads(parsed)
        elif path == '/api/project_names':
            try:
                self.send_json(200, query_project_names())
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == '/api/cherk':
            self.handle_cherk(parsed)
        elif path == '/api/dim-stats':
            params = parse_qs(parsed.query)
            refresh = 'refresh' in params
            try:
                self.send_json(200, query_dim_stats(refresh))
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == '/':
            self.send_response(302)
            self.send_header('Location', '/ads-report.html')
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
        try:
            _validate_ds(start)
            _validate_ds(end)
            if table and table in ADS_TABLES:
                data = query_ads_table(table, start, end, refresh)
            else:
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
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        if '/api/' in str(args[0]):
            super().log_message(fmt, *args)


class ThreadedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


# ── Startup ──

def check_env():
    """启动时检查关键环境变量"""
    warns = []
    if not os.environ.get('ALIYUN_ACCESS_KEY_ID'):
        warns.append('ALIYUN_ACCESS_KEY_ID 未设置 → MaxCompute API 不可用')
    if not os.environ.get('DB_HOST'):
        warns.append('DB_HOST 未设置 → PostgreSQL API 不可用')
    for w in warns:
        print(f'  ⚠ {w}')
    return warns


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

    os.chdir(STUDIO_DIR)

    print(f'YICE Data Studio: http://localhost:{port}')
    print(f'  /             → ads-report.html')
    print(f'  /api/ads      → MaxCompute ADS 报表')
    print(f'  /api/cherk    → PostgreSQL 一致性检查')
    print(f'  /api/chat     → Claude Code 对话')
    check_env()

    server = ThreadedServer(('0.0.0.0', port), APIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')
