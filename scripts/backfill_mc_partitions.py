"""
MaxCompute 分区回填脚本 - 用指定分区数据覆盖所有分区

用法:
  export $(cat .env | xargs)
  python3 platform/scripts/backfill_mc_partitions.py \
    --table dim_xhs_note_df \
    --source-partition 20260129 \
    --target-partitions 20251128,20251129,...,20260129
"""
import argparse
import sys
from datetime import datetime
from odps import ODPS


def connect_mc():
    """连接 MaxCompute"""
    import os
    return ODPS(
        access_id=os.getenv('ALIYUN_ACCESS_KEY_ID'),
        secret_access_key=os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
        project=os.getenv('MC_PROJECT', 'df_ch_530486'),
        endpoint=f"http://service.{os.getenv('MC_REGION', 'cn-hangzhou')}.maxcompute.aliyun.com/api"
    )


def read_partition(mc, table_name, partition_ds):
    """从源分区读取数据"""
    sql = f"SELECT * FROM {table_name} WHERE ds = '{partition_ds}'"

    print(f"  读取源分区 ds={partition_ds}...")
    with mc.execute_sql(sql).open_reader() as reader:
        records = [list(record.values) for record in reader]

    print(f"  ✓ 读取到 {len(records)} 条记录")
    return records


def write_partition(mc, table_name, partition_ds, records):
    """写入目标分区"""
    table = mc.get_table(table_name)

    # 删除旧分区
    try:
        mc.execute_sql(f"ALTER TABLE {table_name} DROP IF EXISTS PARTITION (ds='{partition_ds}')")
    except Exception:
        pass

    # 创建新分区
    mc.execute_sql(f"ALTER TABLE {table_name} ADD IF NOT EXISTS PARTITION (ds='{partition_ds}')")

    # 查找 dt 字段索引
    dt_index = None
    for i, col in enumerate(table.table_schema.columns):
        if col.name == 'dt':
            dt_index = i
            break

    # 转换分区日期格式：YYYYMMDD → YYYY-MM-DD
    target_dt = f"{partition_ds[:4]}-{partition_ds[4:6]}-{partition_ds[6:8]}"

    # 更新记录中的 dt 字段
    updated_records = []
    for record in records:
        record_list = list(record)
        if dt_index is not None:
            record_list[dt_index] = target_dt
        updated_records.append(record_list)

    # 写入数据
    with table.open_writer(partition=f"ds={partition_ds}", create_partition=False) as writer:
        writer.write(updated_records)

    print(f"  ✓ 写入 {len(updated_records)} 条记录到 ds={partition_ds} (dt={target_dt})")


def backfill_partitions(table_name, source_partition, target_partitions):
    """执行分区回填"""
    print(f"=== MaxCompute 分区回填 ===")
    print(f"表名: {table_name}")
    print(f"源分区: {source_partition}")
    print(f"目标分区数: {len(target_partitions)}")

    # 连接 MaxCompute
    print(f"\n连接 MaxCompute...")
    mc = connect_mc()
    print(f"✓ MaxCompute 连接成功")

    # 读取源分区数据
    print(f"\n从源分区读取数据...")
    source_records = read_partition(mc, table_name, source_partition)

    if not source_records:
        print(f"✗ 源分区无数据，退出")
        return 0

    # 回填所有目标分区
    print(f"\n开始回填 {len(target_partitions)} 个分区...")
    success_count = 0

    for i, target_ds in enumerate(target_partitions, 1):
        try:
            print(f"\n[{i}/{len(target_partitions)}] 回填分区 ds={target_ds}")
            write_partition(mc, table_name, target_ds, source_records)
            success_count += 1
        except Exception as e:
            print(f"  ✗ 回填失败: {e}", file=sys.stderr)
            continue

    print(f"\n=== 回填完成 ===")
    print(f"成功: {success_count}/{len(target_partitions)} 个分区")
    print(f"总计: {success_count * len(source_records)} 条记录")

    return success_count


def main():
    parser = argparse.ArgumentParser(description='MaxCompute 分区回填')
    parser.add_argument('--table', required=True, help='表名')
    parser.add_argument('--source-partition', required=True, help='源分区（格式: YYYYMMDD）')
    parser.add_argument('--target-partitions', required=True, help='目标分区列表（逗号分隔，格式: YYYYMMDD）')
    args = parser.parse_args()

    # 解析目标分区列表
    target_partitions = [p.strip() for p in args.target_partitions.split(',')]

    # 执行回填
    backfill_partitions(args.table, args.source_partition, target_partitions)


if __name__ == '__main__':
    main()
