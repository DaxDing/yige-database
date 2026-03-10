# DataWorks PyODPS 节点：按项目校验计划实时数据完整性（通过创意维度表取 campaign_id）
import json
from odps import options
options.sql.settings = {'odps.sql.type.system.odps2': 'true'}

ds = args['bizdate']
base_table = 'dim_xhs_creativity_df'
cherk_table = 'dwd_xhs_campaign_realtime_hi'
cherk_source = '聚光计划层实时报表'

count_sql = f"""
SELECT a.project_id,
       MAX(p.project_name) AS project_name,
       COUNT(DISTINCT a.campaign_id) AS base_count,
       COUNT(DISTINCT b.campaign_id) AS cherk_count
FROM {base_table} a
LEFT JOIN {cherk_table} b
  ON a.campaign_id = b.campaign_id AND b.ds = '{ds}'
LEFT JOIN dim_xhs_project_df p
  ON a.project_id = p.project_id AND p.ds = '{ds}'
WHERE a.ds = '{ds}' AND a.creativity_status = 'T'
GROUP BY a.project_id
"""
with o.execute_sql(count_sql).open_reader() as reader:
    projects = list(reader)

for row in projects:
    project_id = row['project_id']
    project_name = row['project_name'] or ''
    base_count = row['base_count']
    cherk_count = row['cherk_count']

    missing = []
    if base_count > cherk_count:
        miss_sql = f"""
        SELECT DISTINCT a.campaign_id
        FROM {base_table} a
        LEFT JOIN {cherk_table} b
          ON a.campaign_id = b.campaign_id AND b.ds = '{ds}'
        WHERE a.ds = '{ds}' AND a.creativity_status = 'T'
          AND a.project_id = '{project_id}' AND b.campaign_id IS NULL
        """
        with o.execute_sql(miss_sql).open_reader() as r:
            missing = [row2['campaign_id'] for row2 in r]

    missing_count = len(missing)
    status = 'FAIL' if missing_count > 0 else 'PASS'
    missing_sample = json.dumps(missing, ensure_ascii=False)

    print(f'[{status}] {project_name}({project_id}) 基准: {base_count}, 核对: {cherk_count}, 缺失: {missing_count}')

    insert_sql = f"""
    INSERT INTO TABLE cherk_xhs_data_check_df PARTITION (ds='{ds}')
    SELECT '{base_table}', {base_count},
           '{cherk_table}', {cherk_count},
           {missing_count}, '{missing_sample}', '{status}', GETDATE(),
           '{cherk_source}', '{ds}', '{project_id}', '{project_name}'
    """
    o.execute_sql(insert_sql)

print(f'共校验 {len(projects)} 个项目，结果已写入 cherk_xhs_data_check_df')
