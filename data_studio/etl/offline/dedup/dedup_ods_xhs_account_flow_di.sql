-- ============================================================
-- 去重 ODS 投流账户消费表
-- 去重键: account_name + dt
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_account_flow_di PARTITION (ds='${bizdate}')
SELECT
    account_name,
    dt,
    raw_data,
    etl_time
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY account_name, dt
            ORDER BY etl_time DESC
        ) AS rn
    FROM ods_xhs_account_flow_di
    WHERE ds = '${bizdate}'
) t
WHERE t.rn = 1
;
