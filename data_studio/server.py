#!/usr/bin/env python3
"""YICE 数据服务

提供 ADS 报表（MaxCompute）和一致性检查（PostgreSQL）的 API 接口。

启动:
    export $(cat .env | xargs) && python3 data_studio/server.py [port]
"""

import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from decimal import Decimal
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import psycopg2
import psycopg2.extras
from odps import ODPS

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
    'host': 'pgm-bp17nt187ku2460hho.rwlb.rds.aliyuncs.com',
    'port': 5432,
    'dbname': 'data_cherk',
    'user': 'crawler',
    'password': 'F3UnAU3WPj69PY',
}

# ── PostgreSQL 维度表 ──

SYNC_DIM_DB = {
    'host': os.environ.get('DB_HOST', 'pgm-bp17nt187ku2460hho.rwlb.rds.aliyuncs.com'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'dbname': 'sync_dim',
    'user': os.environ.get('DB_USER', 'crawler'),
    'password': os.environ.get('DB_PASSWORD', 'F3UnAU3WPj69PY'),
}

# ── 缓存 ──

_cache = {}
_cache_lock = threading.Lock()
CACHE_TTL = 3600  # 1 小时

_odps = None


def _get_cache(key):
    with _cache_lock:
        if key in _cache:
            entry = _cache[key]
            if time.time() - entry['ts'] < CACHE_TTL:
                return entry['data']
    return None


def _set_cache(key, data):
    with _cache_lock:
        _cache[key] = {'ts': time.time(), 'data': data}


# ── MaxCompute ──

def get_odps():
    global _odps
    if _odps is None:
        _odps = ODPS(
            os.environ['ALIYUN_ACCESS_KEY_ID'],
            os.environ['ALIYUN_ACCESS_KEY_SECRET'],
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


def query_mc_table(key, start_ds, end_ds):
    cfg = ADS_TABLES[key]
    sql = (
        f"SELECT * FROM {cfg['name']} "
        f"WHERE ds >= '{start_ds}' AND ds <= '{end_ds}' "
        f"ORDER BY {cfg['order']};"
    )
    o = get_odps()
    with o.execute_sql(sql).open_reader() as reader:
        col_names = [c.name for c in reader._schema.columns]
        rows = []
        for record in reader:
            row = {name: serialize(record[name]) for name in col_names}
            rows.append(row)
    return rows


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
        result = {key: fut.result() for key, fut in futures.items()}

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

    # 注入项目名称
    try:
        pnames = query_project_names()
    except Exception:
        pnames = {}

    data = {'meta': meta, 'project_names': pnames, **result}
    _set_cache(cache_key, data)

    total = sum(len(v) for v in result.values())
    print(f'  完成: {total} rows, {elapsed:.1f}s', flush=True)
    return data


# ── PostgreSQL 一致性检查 ──

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


# ── PostgreSQL 维度统计 ──

def query_dim_stats(dt=None, refresh=False):
    cache_key = f'dim_stats_{dt or "latest"}'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached:
            return cached

    print(f'  查询 PostgreSQL: sync_dim 维度表 (dt={dt or "latest"}) ...', flush=True)
    t0 = time.time()

    stats = {}  # project_id → { note: {}, task_group: {}, ... }

    def norm_pid(pid):
        """统一 project_id 为 6 位零填充格式"""
        return pid.zfill(6) if pid else pid

    def dt_clause(table):
        """按指定日期或最新日期过滤"""
        if dt:
            return f"AND dt = %s"
        return f"AND dt = (SELECT MAX(dt) FROM {table})"

    def dt_params():
        return (dt,) if dt else ()

    with psycopg2.connect(**SYNC_DIM_DB) as conn:
        with conn.cursor() as cur:
            # 笔记: 执行笔记(非代投) / 复用笔记标记(回链)
            t_name = 'brg_xhs_note_project_df'
            cur.execute(f"""
                SELECT project_id,
                    COUNT(*) FILTER (WHERE NOT is_proxy) AS exec_notes,
                    COUNT(*) FILTER (WHERE is_backlink) AS backlink_notes
                FROM {t_name}
                WHERE project_id IS NOT NULL {dt_clause(t_name)}
                GROUP BY project_id
            """, dt_params())
            for pid, exec_n, bl_n in cur.fetchall():
                stats.setdefault(norm_pid(pid), {})['note'] = {
                    'total': exec_n, 'active': bl_n
                }

            # 任务组: 小红星(tb) / 小红盟(jd)
            t_name = 'dim_xhs_task_group_df'
            cur.execute(f"""
                SELECT project_id,
                    COUNT(*) FILTER (WHERE grass_alliance = 'tb') AS tb_cnt,
                    COUNT(*) FILTER (WHERE grass_alliance = 'jd') AS jd_cnt
                FROM {t_name}
                WHERE project_id IS NOT NULL {dt_clause(t_name)}
                GROUP BY project_id
            """, dt_params())
            for pid, tb, jd in cur.fetchall():
                stats.setdefault(norm_pid(pid), {})['task_group'] = {
                    'total': tb, 'active': jd
                }

            # 创意: 总数 / 有效(status=T)
            t_name = 'dim_xhs_creativity_df'
            cur.execute(f"""
                SELECT project_id,
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE creativity_status = 'T') AS active
                FROM {t_name}
                WHERE project_id IS NOT NULL {dt_clause(t_name)}
                GROUP BY project_id
            """, dt_params())
            for pid, total, active in cur.fetchall():
                stats.setdefault(norm_pid(pid), {})['creative'] = {
                    'total': total, 'active': active
                }

            # 关键词
            t_name = 'dim_xhs_keyword_df'
            cur.execute(f"""
                SELECT project_id, COUNT(*) AS total
                FROM {t_name}
                WHERE project_id IS NOT NULL {dt_clause(t_name)}
                GROUP BY project_id
            """, dt_params())
            for pid, total in cur.fetchall():
                stats.setdefault(norm_pid(pid), {})['keyword'] = {
                    'total': total, 'active': 0
                }

            # 定向包 / 人群包
            t_name = 'dim_xhs_target_df'
            cur.execute(f"""
                SELECT project_id, COUNT(*) AS total
                FROM {t_name}
                WHERE project_id IS NOT NULL {dt_clause(t_name)}
                GROUP BY project_id
            """, dt_params())
            for pid, total in cur.fetchall():
                stats.setdefault(norm_pid(pid), {})['target'] = {
                    'total': total, 'active': 0
                }

            # 人群包补充到 target.active
            t_name = 'dim_xhs_audience_segment_df'
            cur.execute(f"""
                SELECT project_id, COUNT(*) AS total
                FROM {t_name}
                WHERE project_id IS NOT NULL {dt_clause(t_name)}
                GROUP BY project_id
            """, dt_params())
            for pid, total in cur.fetchall():
                npid = norm_pid(pid)
                if npid in stats and 'target' in stats[npid]:
                    stats[npid]['target']['active'] = total
                else:
                    stats.setdefault(npid, {})['target'] = {
                        'total': 0, 'active': total
                    }

            # 投流账户
            t_name = 'dim_xhs_advertiser_df'
            cur.execute(f"""
                SELECT project_id, COUNT(*) AS total
                FROM {t_name}
                WHERE project_id IS NOT NULL {dt_clause(t_name)}
                GROUP BY project_id
            """, dt_params())
            for pid, total in cur.fetchall():
                stats.setdefault(norm_pid(pid), {})['account'] = {
                    'total': total
                }

    elapsed = time.time() - t0
    data = {
        'meta': {
            'queried_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'projects': len(stats),
            'query_seconds': round(elapsed, 2),
        },
        'stats': stats,
    }

    _set_cache(cache_key, data)
    print(f'  完成: {len(stats)} projects, {elapsed:.2f}s', flush=True)
    return data


# ── 飞书项目管理 ──

FEISHU_BITABLE = {
    'app_token': 'LcQ7b94dMae4sMsfU5hcCB3Infe',
    'table_id': 'tblP3a2BkKSJULpE',
}


def _feishu_token():
    import urllib.request
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = json.dumps({
        'app_id': os.environ['FEISHU_APP_ID'],
        'app_secret': os.environ['FEISHU_APP_SECRET'],
    }).encode()
    req = urllib.request.Request(url, data=data,
        headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)['tenant_access_token']


def _feishu_api(method, path, token, data=None):
    import urllib.request, urllib.error
    url = f'https://open.feishu.cn/open-apis{path}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json; charset=utf-8',
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def _parse_link(val):
    if isinstance(val, dict):
        return {'link': val.get('link', ''), 'text': val.get('text', '')}
    if isinstance(val, str) and val != 'None':
        return {'link': val, 'text': val}
    return None


def _parse_links(val):
    """Parse field that may contain one or multiple links."""
    if isinstance(val, list):
        return [_parse_link(v) for v in val if _parse_link(v)]
    single = _parse_link(val)
    return [single] if single else []


def _parse_people(val):
    if not val or not isinstance(val, list):
        return []
    return [{'name': p.get('name', ''), 'id': p.get('id', '')} for p in val]


def _parse_project(item):
    f = item['fields']
    start = f.get('开始时间')
    end = f.get('结束时间')
    adv_ids = f.get('投放账户 ID', [])
    if isinstance(adv_ids, str):
        adv_ids = [adv_ids]

    return {
        'record_id': item['record_id'],
        'project_id': f.get('项目 ID', ''),
        'project_name': f.get('项目名称', ''),
        'department': f.get('执行部门', ''),
        'marketing_target': f.get('营销目标', ''),
        'start_time': datetime.fromtimestamp(start / 1000).strftime('%Y-%m-%d') if start else None,
        'end_time': datetime.fromtimestamp(end / 1000).strftime('%Y-%m-%d') if end else None,
        'advertiser_ids': adv_ids,
        'creator': f.get('创建人', {}).get('name', '') if isinstance(f.get('创建人'), dict) else '',
        'members': _parse_people(f.get('团队成员')),
        'links': {
            'dashboard': _parse_link(f.get('业务看板链接')),
            'content_exec': _parse_links(f.get('内容执行表链接')),
            'folder': _parse_link(f.get('项目文件夹')),
            'budget': _parse_link(f.get('预算表链接')),
        },
    }


def query_projects(refresh=False):
    cache_key = 'projects'
    if not refresh:
        cached = _get_cache(cache_key)
        if cached:
            return cached

    print('  查询飞书: 项目列表 ...', flush=True)
    t0 = time.time()

    token = _feishu_token()
    cfg = FEISHU_BITABLE
    path = f'/bitable/v1/apps/{cfg["app_token"]}/tables/{cfg["table_id"]}/records?page_size=100'
    result = _feishu_api('GET', path, token)

    projects = [_parse_project(item) for item in result.get('data', {}).get('items', [])]

    elapsed = time.time() - t0
    data = {
        'meta': {
            'queried_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': len(projects),
            'query_seconds': round(elapsed, 2),
        },
        'projects': projects,
    }

    _set_cache(cache_key, data)
    print(f'  完成: {len(projects)} projects, {elapsed:.2f}s', flush=True)
    return data


# ── HTTP Handler ──

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/ads':
            self.handle_ads(parsed)
        elif parsed.path == '/api/cherk':
            self.handle_cherk(parsed)
        elif parsed.path == '/api/dim-stats':
            self.handle_dim_stats(parsed)
        elif parsed.path == '/api/projects':
            self.handle_projects(parsed)
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
        try:
            data = query_ads(start, end, refresh)
            self.send_json(200, data)
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

    def handle_dim_stats(self, parsed):
        params = parse_qs(parsed.query)
        refresh = params.get('refresh', ['0'])[0] == '1'
        dt = params.get('dt', [None])[0]
        try:
            data = query_dim_stats(dt=dt, refresh=refresh)
            self.send_json(200, data)
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def handle_projects(self, parsed):
        params = parse_qs(parsed.query)
        refresh = params.get('refresh', ['0'])[0] == '1'
        try:
            data = query_projects(refresh)
            self.send_json(200, data)
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/projects/save':
            self._save_json('projects.json')
        elif parsed.path == '/api/accounts/save':
            self._save_json('accounts.json')
        else:
            self.send_json(404, {'error': 'not found'})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _save_json(self, filename):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            json_path = os.path.join(os.getcwd(), filename)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write('\n')
            self.send_json(200, {'ok': True})
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


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

    portal_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'yice-studio'
    )
    os.chdir(portal_dir)

    print(f'YICE Data Server: http://localhost:{port}')
    print(f'  /api/ads       → MaxCompute ADS 报表')
    print(f'  /api/cherk     → PostgreSQL 一致性检查')
    print(f'  /api/dim-stats → PostgreSQL 维度基准统计')
    print(f'  /api/projects  → 飞书项目管理')

    server = HTTPServer(('0.0.0.0', port), APIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')
