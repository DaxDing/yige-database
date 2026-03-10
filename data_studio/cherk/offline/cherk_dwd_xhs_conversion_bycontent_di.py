# DataWorks PyODPS 节点：按项目校验内容维度转化数据（星河/京准通 × 15/30天归因）
# 基准：brg 非代投笔记，通过 dim_task_group 在项目级别判断 alliance
import json
from odps import options
options.sql.settings = {'odps.sql.type.system.odps2': 'true'}

ds = args['bizdate']
base_table = 'brg_xhs_note_project_df'
cherk_table = 'dwd_xhs_conversion_bycontent_di'

checks = [
    ('tb', '15', '星河内容数据（15）'),
    ('tb', '30', '星河内容数据（30）'),
    ('jd', '15', '京准通内容数据（15）'),
    ('jd', '30', '京准通内容数据（30）'),
]

total = 0
for alliance, period, cherk_source in checks:
    # 1. 按项目统计：仅含该 alliance 任务组的项目，brg 全量非代投笔记 vs DWD 转化记录
    count_sql = f"""
    SELECT brg.project_id,
           MAX(p.project_name) AS project_name,
           COUNT(DISTINCT brg.note_id) AS base_count,
           COUNT(DISTINCT b.note_id) AS cherk_count
    FROM {base_table} brg
    LEFT JOIN {cherk_table} b
      ON brg.note_id = b.note_id AND b.ds = '{ds}'
      AND b.grass_alliance = '{alliance}' AND CAST(b.attribution_period AS STRING) = '{period}'
    LEFT JOIN dim_xhs_project_df p ON brg.project_id = p.project_id AND p.ds = '{ds}'
    WHERE brg.ds = '{ds}' AND brg.is_proxy = FALSE
      AND brg.project_id IN (
        SELECT DISTINCT project_id FROM dim_xhs_task_group_df
        WHERE ds = '{ds}' AND grass_alliance = '{alliance}'
      )
    GROUP BY brg.project_id
    """
    with o.execute_sql(count_sql).open_reader() as reader:
        projects = list(reader)

    # 2. 逐项目查缺失 & 写入结果
    for row in projects:
        project_id = row['project_id']
        project_name = row['project_name'] or ''
        base_count = row['base_count']
        cherk_count = row['cherk_count']

        missing = []
        if base_count > cherk_count:
            miss_sql = f"""
            SELECT DISTINCT brg.note_id
            FROM {base_table} brg
            LEFT JOIN {cherk_table} b
              ON brg.note_id = b.note_id AND b.ds = '{ds}'
              AND b.grass_alliance = '{alliance}' AND CAST(b.attribution_period AS STRING) = '{period}'
            WHERE brg.ds = '{ds}' AND brg.is_proxy = FALSE
              AND brg.project_id = '{project_id}' AND b.note_id IS NULL
            """
            with o.execute_sql(miss_sql).open_reader() as r:
                missing = [row2['note_id'] for row2 in r]

        missing_count = len(missing)
        status = 'FAIL' if missing_count > 0 else 'PASS'
        missing_sample = json.dumps(missing, ensure_ascii=False)

        print(f'[{status}] {cherk_source} {project_name}({project_id}) 基准: {base_count}, 核对: {cherk_count}, 缺失: {missing_count}')

        insert_sql = f"""
        INSERT INTO TABLE cherk_xhs_data_check_df PARTITION (ds='{ds}')
        SELECT '{base_table}', {base_count},
               '{cherk_table}', {cherk_count},
               {missing_count}, '{missing_sample}', '{status}', GETDATE(),
               '{cherk_source}', '{ds}', '{project_id}', '{project_name}'
        """
        o.execute_sql(insert_sql)
        total += 1

print(f'共校验 {total} 条记录，结果已写入 cherk_xhs_data_check_df')
