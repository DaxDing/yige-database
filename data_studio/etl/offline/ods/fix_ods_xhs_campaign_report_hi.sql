-- ============================================================
-- 补充 ODS 层 campaign_id、etl_time，清理 raw_data 零值键
-- 源表/目标表: ods_xhs_campaign_report_hi
-- 上游依赖: sync_xhs_campaign_report_hi
-- 下游依赖: etl_xhs_campaign_daily
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_campaign_report_hi PARTITION (ds='${bizdate}')
SELECT
    campaign_id,
    dt,
    -- 清理 raw_data 中值为 null/0/空的键值对
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
FROM ods_xhs_campaign_report_hi
WHERE ds = '${bizdate}'
;
