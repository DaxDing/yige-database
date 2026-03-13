"""PostgreSQL 查询"""

import time
from datetime import datetime
from decimal import Decimal

import psycopg2
import psycopg2.extras

from settings import POSTGRES
from lib import cache


def query_project_names(refresh=False):
    if not refresh:
        cached = cache.get('project_names')
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
    cache.put('project_names', mapping)
    return mapping


def query_cherk(refresh=False):
    cache_key = 'cherk'
    if not refresh:
        cached = cache.get(cache_key)
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

    cache.put(cache_key, data)
    print(f'  完成: {len(result)} rows, {elapsed:.2f}s', flush=True)
    return data


def query_dim_stats(refresh=False):
    cache_key = 'dim_stats'
    if not refresh:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    print('  查询 PostgreSQL(sync_dim): 维度基准统计 ...', flush=True)
    t0 = time.time()

    stats = {}

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

    cache.put(cache_key, data)
    print(f'  完成: {len(stats)} projects, {elapsed:.2f}s', flush=True)
    return data
