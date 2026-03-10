"""
PostgreSQL → MaxCompute 数据同步脚本

用法:
  export $(cat .env | xargs)
  python3 platform/scripts/sync_pg_to_mc.py \
    --table dim_xhs_note_df \
    --partitions 20260126,20260127,20260128,20260129
"""
import argparse
import os
import sys
from datetime import datetime
from odps import ODPS
import psycopg2
from psycopg2.extras import RealDictCursor

# 表字段映射（PostgreSQL dt(DATE) → MaxCompute ds(STRING)）
TABLE_CONFIGS = {
    'dim_xhs_ad_product_df': {
        'pg_fields': ['ad_product_id', 'ad_product_name', 'project_id', 'brand_name', 'product_category', 'dt'],
        'mc_fields': ['ad_product_id', 'ad_product_name', 'project_id', 'brand_name', 'product_category', 'etl_time', 'dt'],
        'partition_field': 'dt'
    },
    'dim_xhs_note_df': {
        'pg_fields': ['note_id', 'content_theme', 'ad_product_name', 'dt'],
        'mc_fields': ['note_id', 'content_theme', 'ad_product_name', 'task_group_id', 'etl_time', 'dt', 'ad_product_id'],
        'partition_field': 'dt'
    },
    'dim_xhs_project_df': {
        'pg_fields': ['project_id', 'project_name', 'valid_from', 'valid_to', 'marketing_target', 'exec_dept_name', 'dt'],
        'mc_fields': ['project_id', 'project_name', 'valid_from', 'valid_to', 'marketing_target', 'exec_dept_name', 'etl_time', 'dt', 'kpi_fetch_time'],
        'partition_field': 'dt'
    },
    'dim_xhs_task_group_df': {
        'pg_fields': ['task_group_id', 'task_id', 'task_group_name', 'brand_user_id', 'grass_alliance', 'pgy_project_id', 'confirm_time', 'task_auth_status', 'dt'],
        'mc_fields': ['task_group_id', 'task_id', 'task_group_name', 'brand_user_id', 'grass_alliance', 'pgy_project_id', 'confirm_time', 'task_auth_status', 'etl_time', 'dt'],
        'partition_field': 'dt'
    },
    'brg_xhs_note_project_df': {
        'pg_fields': ['note_id', 'project_id', 'dt', 'is_proxy'],
        'mc_fields': ['note_id', 'project_id', 'dt', 'is_proxy', 'etl_time'],
        'partition_field': 'dt'
    }
}


def connect_pg():
    """连接 PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )


def connect_mc():
    """连接 MaxCompute"""
    return ODPS(
        access_id=os.getenv('ALIYUN_ACCESS_KEY_ID'),
        secret_access_key=os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
        project=os.getenv('MC_PROJECT', 'df_ch_530486'),
        endpoint=f"http://service.{os.getenv('MC_REGION', 'cn-hangzhou')}.maxcompute.aliyun.com/api"
    )


def fetch_partition_data(pg_conn, table_name, partition_date, config):
    """从 PostgreSQL 拉取指定分区数据"""
    with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
        fields_str = ', '.join(config['pg_fields'])
        sql = f"""
        SELECT {fields_str}
        FROM {table_name}
        WHERE {config['partition_field']} = %s
        """
        cur.execute(sql, (partition_date,))
        return cur.fetchall()


def format_value(val):
    """格式化字段值"""
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    return str(val)


def sync_partition(table_name, partition_ds, pg_conn, mc):
    """同步单个分区"""
    config = TABLE_CONFIGS[table_name]

    # 转换分区格式：YYYYMMDD → YYYY-MM-DD
    partition_date = f"{partition_ds[:4]}-{partition_ds[4:6]}-{partition_ds[6:8]}"

    print(f"\n[{table_name}] 同步分区 ds={partition_ds} (pg dt={partition_date})")

    # 1. 从 PostgreSQL 拉取数据
    print(f"  1. 从 PostgreSQL 拉取数据...")
    rows = fetch_partition_data(pg_conn, table_name, partition_date, config)
    if not rows:
        print(f"  ⚠️  PostgreSQL 中无数据，跳过")
        return 0

    print(f"  ✓ 拉取到 {len(rows)} 条记录")

    # 2. 删除 MaxCompute 旧分区
    print(f"  2. 删除 MaxCompute 旧分区...")
    try:
        mc.execute_sql(f"ALTER TABLE {table_name} DROP IF EXISTS PARTITION (ds='{partition_ds}')")
        print(f"  ✓ 旧分区已删除")
    except Exception as e:
        print(f"  ℹ️  分区不存在或删除失败: {e}")

    # 3. 添加新分区
    print(f"  3. 添加新分区...")
    mc.execute_sql(f"ALTER TABLE {table_name} ADD IF NOT EXISTS PARTITION (ds='{partition_ds}')")
    print(f"  ✓ 新分区已创建")

    # 4. 写入数据
    print(f"  4. 写入数据到 MaxCompute...")
    table = mc.get_table(table_name)

    # 获取当前时间作为 etl_time
    etl_time = datetime.now()
    # 转换分区日期格式作为 dt: YYYYMMDD → YYYY-MM-DD
    dt_value = partition_date

    # 转换数据格式
    records = []
    for row in rows:
        record = []
        for field in config['mc_fields']:
            if field == 'etl_time':
                record.append(etl_time)
            elif field == 'dt':
                record.append(dt_value)
            elif field in ('task_group_id', 'ad_product_id', 'kpi_fetch_time'):
                # 这些字段在 PostgreSQL 中不存在，设置为 NULL
                record.append(None)
            else:
                val = row.get(field)
                record.append(format_value(val))
        records.append(record)

    # 批量写入
    with table.open_writer(partition=f"ds={partition_ds}", create_partition=False) as writer:
        writer.write(records)

    print(f"  ✓ 写入 {len(records)} 条记录")
    return len(records)


def main():
    parser = argparse.ArgumentParser(description='PostgreSQL → MaxCompute 同步')
    parser.add_argument('--table', required=True, choices=list(TABLE_CONFIGS.keys()), help='表名')
    parser.add_argument('--partitions', required=True, help='分区列表（逗号分隔），格式: YYYYMMDD')
    args = parser.parse_args()

    # 解析分区列表
    partitions = [p.strip() for p in args.partitions.split(',')]

    print(f"=== PostgreSQL → MaxCompute 数据同步 ===")
    print(f"表名: {args.table}")
    print(f"分区: {', '.join(partitions)}")

    # 连接数据源
    print(f"\n连接 PostgreSQL...")
    pg_conn = connect_pg()
    print(f"✓ PostgreSQL 连接成功")

    print(f"\n连接 MaxCompute...")
    mc = connect_mc()
    print(f"✓ MaxCompute 连接成功")

    # 同步各分区
    total_records = 0
    for partition_ds in partitions:
        try:
            count = sync_partition(args.table, partition_ds, pg_conn, mc)
            total_records += count
        except Exception as e:
            print(f"  ✗ 同步失败: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            continue

    # 关闭连接
    pg_conn.close()

    print(f"\n=== 同步完成 ===")
    print(f"总计: {total_records} 条记录")


if __name__ == '__main__':
    main()
