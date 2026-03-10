-- ============================================================
-- 清理 ODS 层 raw_data 零值键，补充 etl_time
-- 源表/目标表: ods_xhs_account_flow_di
-- 上游依赖: sync_xhs_account_flow_di
-- 下游依赖: etl_dwd_xhs_account_flow_di
-- 调度参数: bizdate
-- 说明: account_name 由同步任务直接写入，无需事后补全
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_account_flow_di PARTITION (ds='${bizdate}')
SELECT
    account_name,
    dt,
    REGEXP_REPLACE(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    raw_data,
                    '"[^"]+":null,?',                  -- 删除 null 值键值对
                    ''
                ),
                '"[^"]+":"(-|0(\\.0+)?%?|)",?',        -- 删除零值/横杠/空值键值对
                ''
            ),
            ',}',   -- 修复末尾逗号
            '}'
        ),
        '\\{,',     -- 修复开头逗号
        '{'
    )                                             AS raw_data,
    COALESCE(etl_time, GETDATE())                 AS etl_time
FROM ods_xhs_account_flow_di
WHERE ds = '${bizdate}'
;
