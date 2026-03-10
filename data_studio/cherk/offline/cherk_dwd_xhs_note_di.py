# DataWorks PyODPS 节点：按项目校验 brg 笔记是否全部存在于 dwd，结果写入 MaxCompute
import json
from odps import options
options.sql.settings = {'odps.sql.type.system.odps2': 'true'}

ds = args['bizdate']
base_table = 'brg_xhs_note_project_df'
cherk_table = 'dwd_xhs_note_di'
cherk_source = '蒲公英投后数据'

# 1. 按项目统计基准数量 & 核对数量，关联维度表取项目名称
count_sql = f"""
SELECT a.project_id,
       MAX(p.project_name) AS project_name,
       COUNT(DISTINCT a.note_id) AS base_count,
       COUNT(DISTINCT b.note_id) AS cherk_count
FROM {base_table} a
LEFT JOIN {cherk_table} b
  ON a.note_id = b.note_id AND b.ds = '{ds}'
LEFT JOIN dim_xhs_project_df p
  ON a.project_id = p.project_id AND p.ds = '{ds}'
WHERE a.ds = '{ds}'
GROUP BY a.project_id
"""
with o.execute_sql(count_sql).open_reader() as reader:
    projects = list(reader)

# 2. 逐项目查缺失 & 写入结果
for row in projects:
    project_id = row['project_id']
    project_name = row['project_name'] or ''
    base_count = row['base_count']
    cherk_count = row['cherk_count']

    # 有差异时查缺失明细
    missing = []
    if base_count > cherk_count:
        miss_sql = f"""
        SELECT a.note_id
        FROM {base_table} a
        LEFT JOIN {cherk_table} b
          ON a.note_id = b.note_id AND b.ds = '{ds}'
        WHERE a.ds = '{ds}' AND a.project_id = '{project_id}'
          AND b.note_id IS NULL
        """
        with o.execute_sql(miss_sql).open_reader() as r:
            missing = [row2['note_id'] for row2 in r]

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
