"""MaxCompute 查询"""

import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from odps import ODPS

from settings import MAXCOMPUTE, ADS_TABLES
from lib import cache
from lib.utils import serialize, validate_ds

_odps = None


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


def query_table(key, start_ds, end_ds):
    validate_ds(start_ds)
    validate_ds(end_ds)
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
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    print(f'  查询 {ADS_TABLES[table]["name"]}: ds {start_ds} ~ {end_ds} ...', flush=True)
    t0 = time.time()
    rows = query_table(table, start_ds, end_ds)
    elapsed = time.time() - t0
    print(f'  完成: {len(rows)} rows, {elapsed:.1f}s', flush=True)

    result = {
        'table': table,
        'rows': rows,
        'count': len(rows),
        'query_seconds': round(elapsed, 1),
    }
    cache.put(cache_key, result)
    return result


def query_ads(start_ds, end_ds, refresh=False):
    cache_key = f'ads_{start_ds}_{end_ds}'
    if not refresh:
        cached = cache.get(cache_key)
        if cached:
            return cached

    print(f'  查询 MaxCompute: ds {start_ds} ~ {end_ds} ...', flush=True)
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            key: executor.submit(query_table, key, start_ds, end_ds)
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
        from lib.pg import query_project_names
        pnames = query_project_names()
    except Exception:
        pnames = {}

    data = {'meta': meta, 'project_names': pnames, **result}
    if not errors:
        cache.put(cache_key, data)
        for key, rows in result.items():
            cache.put(f'ads_{key}_{start_ds}_{end_ds}', {
                'table': key, 'rows': rows, 'count': len(rows),
            })

    total = sum(len(v) for v in result.values())
    print(f'  完成: {total} rows, {elapsed:.1f}s', flush=True)
    return data
