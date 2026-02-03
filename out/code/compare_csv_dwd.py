"""比对蒲公英源数据 CSV 与 dwd_xhs_note_cum 表"""
import csv
import os
import json
from collections import defaultdict
from decimal import Decimal

# ── CSV 字段 → DWD 字段映射 ──
FIELD_MAP = {
    '曝光量': 'impression',
    '阅读UV': 'read_uv',
    '互动量': 'interaction',
    '点赞量': 'like',
    '收藏量': 'collect',
    '评论量': 'comment',
    '分享量': 'share',
    '关注量': 'follow',
    '自然曝光量': 'origin_impression',
    '自然阅读量': 'origin_read',
    '推广曝光量': 'promotion_impression',
    '推广阅读量': 'promotion_read',
    '加热曝光量': 'heat_impression',
    '加热阅读量': 'heat_read',
    '博主报价': 'kol_price',
    '正文组件曝光量': 'content_comp_impression',
    '正文组件点击量': 'content_comp_click',
    '正文组件点击人数': 'content_comp_click_uv',
    '评论区组件曝光量': 'comment_comp_impression',
    '评论区组件点击量': 'comment_comp_click',
    '评论区组件点击人数': 'comment_comp_click_uv',
    '互动组件曝光人数': 'engage_comp_impression',
    '互动组件参与人数': 'engage_comp_click',
    '笔记底栏组件曝光量': 'note_bottom_comp_impression',
    '笔记底栏组件点击量': 'note_bottom_comp_click',
    '笔记底栏组件点击人数': 'note_bottom_comp_click_uv',
}


def parse_number(val):
    """解析 CSV 数值：去逗号、处理百分号、空值"""
    if not val or val in ('-', '#DIV/0!', ''):
        return None
    val = val.replace(',', '').replace('%', '').strip()
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def load_csv(path):
    """加载 CSV，返回 {(note_id, ds): {field: value}} 字典"""
    data = {}
    with open(path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            note_id = row.get('笔记id', '').strip()
            date_str = row.get('数据更新日期', '').strip()
            if not note_id or not date_str:
                continue
            # 2026/01/26 → 20260126
            ds = date_str.replace('/', '')
            record = {}
            for csv_field, dwd_field in FIELD_MAP.items():
                record[dwd_field] = parse_number(row.get(csv_field))
            data[(note_id, ds)] = record
    return data


def query_dwd(note_ids, ds_list):
    """查询 MaxCompute dwd_xhs_note_cum，返回同结构字典"""
    from odps import ODPS

    o = ODPS(
        os.environ['ALIYUN_ACCESS_KEY_ID'],
        os.environ['ALIYUN_ACCESS_KEY_SECRET'],
        project='df_ch_530486',
        endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api',
    )

    fields = list(set(FIELD_MAP.values()))
    fields_sql = ', '.join(f'`{f}`' if f == 'like' else f for f in fields)
    ds_in = ', '.join(f"'{d}'" for d in ds_list)

    sql = f"""
    SELECT ds, note_id, {fields_sql}
    FROM dwd_xhs_note_cum
    WHERE ds IN ({ds_in})
    """

    data = {}
    with o.execute_sql(sql).open_reader() as reader:
        for row in reader:
            note_id = row['note_id']
            ds = row['ds']
            record = {}
            for f in fields:
                v = row[f]
                if isinstance(v, Decimal):
                    v = int(v) if v == int(v) else float(v)
                record[f] = v
            data[(note_id, ds)] = record
    return data


def compare(csv_data, dwd_data):
    """比较两份数据，输出差异报告"""
    csv_keys = set(csv_data.keys())
    dwd_keys = set(dwd_data.keys())

    # 1. 笔记覆盖度
    csv_note_ids = set(k[0] for k in csv_keys)
    dwd_note_ids = set(k[0] for k in dwd_keys)
    only_csv = csv_note_ids - dwd_note_ids
    only_dwd_relevant = dwd_note_ids - csv_note_ids  # DWD has more, that's expected

    print("=" * 60)
    print("数据比对报告：蒲公英 CSV vs dwd_xhs_note_cum")
    print("=" * 60)

    print(f"\n── 覆盖度 ──")
    print(f"CSV 笔记数: {len(csv_note_ids)}")
    print(f"DWD 笔记数 (对应分区): {len(dwd_note_ids)}")
    print(f"CSV 有 DWD 无: {len(only_csv)} 条")
    if only_csv:
        print(f"  缺失笔记ID: {list(only_csv)[:10]}{'...' if len(only_csv) > 10 else ''}")

    # 2. 可比对的 key
    common_keys = csv_keys & dwd_keys
    print(f"\n可比对记录: {len(common_keys)} / {len(csv_keys)} (CSV)")

    # 3. 逐字段比对
    field_stats = defaultdict(lambda: {'match': 0, 'mismatch': 0, 'csv_null': 0, 'dwd_null': 0, 'diffs': []})

    for key in common_keys:
        csv_rec = csv_data[key]
        dwd_rec = dwd_data[key]
        for field in FIELD_MAP.values():
            csv_val = csv_rec.get(field)
            dwd_val = dwd_rec.get(field)
            stats = field_stats[field]

            if csv_val is None and dwd_val is None:
                stats['match'] += 1
            elif csv_val is None:
                stats['csv_null'] += 1
            elif dwd_val is None:
                stats['dwd_null'] += 1
            elif csv_val == dwd_val:
                stats['match'] += 1
            else:
                stats['mismatch'] += 1
                if len(stats['diffs']) < 3:
                    stats['diffs'].append({
                        'note_id': key[0], 'ds': key[1],
                        'csv': csv_val, 'dwd': dwd_val,
                        'delta': csv_val - dwd_val if isinstance(csv_val, (int, float)) and isinstance(dwd_val, (int, float)) else 'N/A'
                    })

    # 输出字段级汇总
    print(f"\n── 字段级比对 ({len(common_keys)} 条记录) ──")
    print(f"{'字段':<30} {'匹配':>6} {'不匹配':>6} {'CSV空':>6} {'DWD空':>6} {'匹配率':>8}")
    print("-" * 72)

    total_match = 0
    total_mismatch = 0
    all_diffs = []

    for csv_name, dwd_name in FIELD_MAP.items():
        s = field_stats[dwd_name]
        total = s['match'] + s['mismatch'] + s['csv_null'] + s['dwd_null']
        comparable = s['match'] + s['mismatch']
        rate = f"{s['match']/comparable*100:.1f}%" if comparable > 0 else "N/A"
        flag = " ✗" if s['mismatch'] > 0 else " ✓"
        print(f"{csv_name:<28} {s['match']:>6} {s['mismatch']:>6} {s['csv_null']:>6} {s['dwd_null']:>6} {rate:>8}{flag}")
        total_match += s['match']
        total_mismatch += s['mismatch']
        if s['diffs']:
            for d in s['diffs']:
                d['field'] = csv_name
            all_diffs.extend(s['diffs'])

    print("-" * 72)
    overall_rate = total_match / (total_match + total_mismatch) * 100 if (total_match + total_mismatch) > 0 else 0
    print(f"{'总计':<28} {total_match:>6} {total_mismatch:>6} {'':>6} {'':>6} {overall_rate:.2f}%")

    # 差异样例
    if all_diffs:
        print(f"\n── 差异样例 (最多展示 10 条) ──")
        for d in all_diffs[:10]:
            print(f"  [{d['field']}] note={d['note_id']} ds={d['ds']} | CSV={d['csv']} DWD={d['dwd']} Δ={d['delta']}")

    # 结论
    print(f"\n── 结论 ──")
    if total_mismatch == 0 and len(only_csv) == 0:
        print("✓ 完全一致")
    elif total_mismatch == 0:
        print(f"△ 指标一致，但有 {len(only_csv)} 条笔记在 DWD 中缺失")
    else:
        print(f"✗ 存在差异：{total_mismatch} 个字段值不一致")

    return total_mismatch, only_csv


if __name__ == '__main__':
    csv_path = '/Users/Dax/Downloads/业务看板 - 蒲公英源数据表-核对用.csv'
    print("加载 CSV...")
    csv_data = load_csv(csv_path)
    print(f"  CSV 记录数: {len(csv_data)}")

    ds_list = sorted(set(k[1] for k in csv_data.keys()))
    note_ids = sorted(set(k[0] for k in csv_data.keys()))
    print(f"  分区日期: {ds_list}")
    print(f"  笔记数: {len(note_ids)}")

    print("\n查询 MaxCompute...")
    dwd_data = query_dwd(note_ids, ds_list)
    print(f"  DWD 记录数: {len(dwd_data)}")

    print()
    compare(csv_data, dwd_data)
