# DataWorks PyODPS 节点：按项目校验人群包维度是否全部存在于 dwd_audience，结果写入 MaxCompute
import json
from datetime import datetime, timedelta
from odps import options
options.sql.settings = {'odps.sql.type.system.odps2': 'true'}

ds = args['bizdate']
cherk_time = (datetime.strptime(ds, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')
base_table = 'dim_xhs_audience_segment_df'
cherk_table = 'dwd_xhs_audience_report_di'
cherk_source = '人群包离线报表'

# 1. 按项目统计基准数量 & 核对数量
count_sql = f"""
SELECT a.project_id,
       MAX(p.project_name) AS project_name,
       COUNT(DISTINCT a.group_id) AS base_count,
       COUNT(DISTINCT b.group_id) AS cherk_count
FROM {base_table} a
LEFT JOIN {cherk_table} b
  ON a.group_id = b.group_id AND b.ds = '{ds}'
LEFT JOIN dim_xhs_project_df p
  ON a.project_id = p.project_id AND p.ds = '{ds}'
WHERE a.ds = '{ds}'
GROUP BY a.project_id
"""
with o.execute_sql(count_sql).open_reader() as reader:
    projects = list(reader)

# 1.5 获取核对表的分区范围（元数据，零开销）
all_ds = sorted([p.partition_spec['ds'] for p in o.get_table(cherk_table).partitions])
cherk_min_ds = all_ds[0] if all_ds else None
cherk_max_ds = all_ds[-1] if all_ds else None

# 2. 逐项目查缺失 & 写入结果
for row in projects:
    project_id = row['project_id']
    project_name = row['project_name'] or ''
    base_count = row['base_count']
    cherk_count = row['cherk_count']

    missing = []
    if base_count > cherk_count:
        miss_sql = f"""
        SELECT a.group_id
        FROM {base_table} a
        LEFT JOIN {cherk_table} b
          ON a.group_id = b.group_id AND b.ds = '{ds}'
        WHERE a.ds = '{ds}' AND a.project_id = '{project_id}'
          AND b.group_id IS NULL
        """
        with o.execute_sql(miss_sql).open_reader() as r:
            missing = [row2['group_id'] for row2 in r]

    missing_count = len(missing)
    status = 'FAIL' if missing_count > 0 else 'PASS'
    missing_sample = json.dumps(missing, ensure_ascii=False)
    min_ds_sql = f"'{cherk_min_ds}'" if cherk_min_ds else 'NULL'
    max_ds_sql = f"'{cherk_max_ds}'" if cherk_max_ds else 'NULL'

    print(f'[{status}] {project_name}({project_id}) 基准: {base_count}, 核对: {cherk_count}, 缺失: {missing_count}, 分区: {cherk_min_ds or "-"}~{cherk_max_ds or "-"}')

    insert_sql = f"""
    INSERT INTO TABLE cherk_xhs_data_check_df PARTITION (ds='{ds}')
    SELECT '{base_table}', {base_count},
           '{cherk_table}', {cherk_count},
           {missing_count}, '{missing_sample}', '{status}', GETDATE(),
           '{cherk_source}', '{ds}', '{project_id}', '{project_name}', '{cherk_time}',
           {min_ds_sql}, {max_ds_sql}
    """
    o.execute_sql(insert_sql)

print(f'共校验 {len(projects)} 个项目，结果已写入 cherk_xhs_data_check_df')
