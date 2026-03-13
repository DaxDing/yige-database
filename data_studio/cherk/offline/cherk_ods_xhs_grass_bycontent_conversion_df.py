# DataWorks PyODPS 节点：按项目校验内容维度转化数据（星河/京准通 × 15/30天归因）
# 基准：brg 非代投笔记，通过 dim_task_group 在项目级别判断 alliance
# 核对：DWD 全分区去重（转化数据按 dt 分区，不同笔记分布在不同 ds）
import json
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from odps import options
options.sql.settings = {
    'odps.sql.type.system.odps2': 'true',
    'odps.sql.allow.fullscan': 'true',
}

ds = args['bizdate']
cherk_time = (datetime.strptime(ds, '%Y%m%d') + timedelta(days=2)).strftime('%Y%m%d')
base_table = 'brg_xhs_note_project_df'
cherk_table = 'ods_xhs_grass_bycontent_conversion_df'

checks = [
    ('tb', '15', '星河内容数据（15）'),
    ('tb', '30', '星河内容数据（30）'),
    ('jd', '15', '京准通内容数据（15）'),
    ('jd', '30', '京准通内容数据（30）'),
]


def run_check(alliance, period, cherk_source):
    """单个 check 的完整流程：统计 → 查缺失 → 写入"""
    count_sql = f"""
    SELECT brg.project_id,
           MAX(p.project_name) AS project_name,
           COUNT(DISTINCT brg.note_id) AS base_count,
           COUNT(DISTINCT b.note_id) AS cherk_count
    FROM {base_table} brg
    LEFT JOIN (
        SELECT DISTINCT note_id
        FROM {cherk_table}
        WHERE ds = '{ds}' AND grass_alliance = '{alliance}' AND CAST(attribution_period AS STRING) = '{period}'
    ) b ON brg.note_id = b.note_id
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

    # 获取核对表的分区范围（元数据，零开销）
    all_ds = sorted([p.partition_spec['ds'] for p in o.get_table(cherk_table).partitions])
    cherk_min_ds = all_ds[0] if all_ds else None
    cherk_max_ds = all_ds[-1] if all_ds else None

    results = []
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
            LEFT JOIN (
                SELECT DISTINCT note_id
                FROM {cherk_table}
                WHERE ds = '{ds}' AND grass_alliance = '{alliance}' AND CAST(attribution_period AS STRING) = '{period}'
            ) b ON brg.note_id = b.note_id
            WHERE brg.ds = '{ds}' AND brg.is_proxy = FALSE
              AND brg.project_id = '{project_id}' AND b.note_id IS NULL
            """
            with o.execute_sql(miss_sql).open_reader() as r:
                missing = [row2['note_id'] for row2 in r]

        missing_count = len(missing)
        status = 'FAIL' if missing_count > 0 else 'PASS'
        missing_sample = json.dumps(missing, ensure_ascii=False)
        min_ds_sql = f"'{cherk_min_ds}'" if cherk_min_ds else 'NULL'
        max_ds_sql = f"'{cherk_max_ds}'" if cherk_max_ds else 'NULL'

        print(f'[{status}] {cherk_source} {project_name}({project_id}) 基准: {base_count}, 核对: {cherk_count}, 缺失: {missing_count}, 分区: {cherk_min_ds or "-"}~{cherk_max_ds or "-"}')

        insert_sql = f"""
        INSERT INTO TABLE cherk_xhs_data_check_df PARTITION (ds='{ds}')
        SELECT '{base_table}', {base_count},
               '{cherk_table}', {cherk_count},
               {missing_count}, '{missing_sample}', '{status}', GETDATE(),
               '{cherk_source}', '{ds}', '{project_id}', '{project_name}', '{cherk_time}',
               {min_ds_sql}, {max_ds_sql}
        """
        o.execute_sql(insert_sql)
        results.append((cherk_source, project_id, status))

    return results


# 4 个 check 并发执行
total = 0
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(run_check, a, p, s): s for a, p, s in checks}
    for future in as_completed(futures):
        results = future.result()
        total += len(results)

print(f'共校验 {total} 条记录，结果已写入 cherk_xhs_data_check_df')
