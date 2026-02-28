-- ============================================================
-- 补充 ODS 层 search_word、etl_time，清理 raw_data 零值键
-- 源表/目标表: ods_xhs_searchword_report_di
-- 上游依赖: sync_xhs_searchword_report_di
-- 下游依赖: (待定)
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_searchword_report_di PARTITION (ds='${bizdate}')
SELECT
    search_word,
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
FROM ods_xhs_searchword_report_di
WHERE ds = '${bizdate}'
;
