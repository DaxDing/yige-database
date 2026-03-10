#!/usr/bin/env python3
"""导出 ADS 聚合表数据为 JSON，供前端报表使用。

Usage:
    export $(cat .env | xargs) && python3 data_studio/scripts/export_ads_data.py \
        --start 2026-03-01 --end 2026-03-09
"""

import argparse
import json
import os
import sys
from datetime import datetime
from decimal import Decimal

from odps import ODPS

TABLES = {
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

OUTPUT_DIR = 'yice-studio/data'


def serialize(val):
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    return val


def export_table(odps, key, cfg, start_ds, end_ds):
    sql = (
        f"SELECT * FROM {cfg['name']} "
        f"WHERE ds >= '{start_ds}' AND ds <= '{end_ds}' "
        f"ORDER BY {cfg['order']};"
    )
    print(f'  {cfg["name"]} ...', end=' ', flush=True)

    with odps.execute_sql(sql).open_reader() as reader:
        col_names = [c.name for c in reader._schema.columns]
        rows = []
        for record in reader:
            row = {name: serialize(record[name]) for name in col_names}
            rows.append(row)

    output = os.path.join(OUTPUT_DIR, f'ads_{key}.json')
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False)

    print(f'{len(rows)} rows → {output}')
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description='导出 ADS 表为 JSON')
    parser.add_argument('--start', required=True, help='起始日期 YYYY-MM-DD')
    parser.add_argument('--end', required=True, help='结束日期 YYYY-MM-DD')
    parser.add_argument('--tables', nargs='+', choices=list(TABLES.keys()),
                        default=list(TABLES.keys()))
    args = parser.parse_args()

    start_ds = args.start.replace('-', '')
    end_ds = args.end.replace('-', '')

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    odps = ODPS(
        os.environ['ALIYUN_ACCESS_KEY_ID'],
        os.environ['ALIYUN_ACCESS_KEY_SECRET'],
        project='df_ch_530486',
        endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api',
    )

    print(f'导出 ADS 数据: {args.start} ~ {args.end}')

    summary = {}
    for key in args.tables:
        count = export_table(odps, key, TABLES[key], start_ds, end_ds)
        summary[key] = count

    meta = {
        'exported_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': {'start': args.start, 'end': args.end},
        'tables': summary,
    }
    meta_path = os.path.join(OUTPUT_DIR, 'meta.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f'\n完成! 元数据 → {meta_path}')


if __name__ == '__main__':
    main()
