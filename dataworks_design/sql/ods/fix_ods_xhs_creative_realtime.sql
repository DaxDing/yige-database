-- ============================================================
-- 补充 ODS 层 advertiser_id、dt、etl_time，清理 raw_data 零值键
-- 源表/目标表: ods_xhs_creative_realtime_hi
-- 上游依赖: sync_xhs_creative_realtime_hi
-- 下游依赖: etl_dwd_xhs_creative_realtime_hi
-- 调度参数: bizdate, advertiser_id
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_creative_realtime_hi PARTITION (ds='${bizdate}')
SELECT
    COALESCE(advertiser_id, '${advertiser_id}')   AS advertiser_id,
    COALESCE(dt, '${bizdate}')                    AS dt,
    -- 清理 raw_data 中值为 null/0/空的键值对
    REGEXP_REPLACE(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    raw_data,
                    '"[^"]+":null,?',                  -- 删除 null 值键值对
                    ''
                ),
                '"[^"]+":"(0|0\\.0|0\\.0%|)",?',      -- 删除零值键值对
                ''
            ),
            ',}',   -- 修复末尾逗号
            '}'
        ),
        '\\{,',     -- 修复开头逗号
        '{'
    )                                             AS raw_data,
    COALESCE(etl_time, GETDATE())                 AS etl_time
FROM ods_xhs_creative_realtime_hi
WHERE ds = '${bizdate}'
  AND GET_JSON_OBJECT(raw_data, '$.hourly_data') IS NOT NULL
;
