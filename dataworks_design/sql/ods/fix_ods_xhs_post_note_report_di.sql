-- ============================================================
-- 补充 ODS 层 etl_time，清理 raw_data 零值键（支持嵌套）
-- 源表/目标表: ods_xhs_post_note_report_di
-- 上游依赖: sync_xhs_post_note_report_di
-- 下游依赖: etl_xhs_post_note_daily
-- 调度参数: bizdate, brand_user_id
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_post_note_report_di PARTITION (ds='${bizdate}')
SELECT
    dt,
    REGEXP_REPLACE(
    REGEXP_REPLACE(
    REGEXP_REPLACE(
        REGEXP_REPLACE(
        REGEXP_REPLACE(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
            REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                REGEXP_REPLACE(
                REGEXP_REPLACE(
                    raw_data,
                    '"[^"]+":0,?',
                    ''
                ),
                '"[^"]+":null,?',
                ''
                ),
            ',}', '}'
            ),
            '\\{,', '{'
            ),
            '"[^"]+":\\{\\},?', ''
            ),
        ',}', '}'
        ),
        '\\{,', '{'
        ),
        '"[^"]+":\\{\\},?', ''
        ),
    ',}', '}'
    ),
    '\\{,', '{'
    ),
    '"[^"]+":\\{\\},?', ''
    ) AS raw_data,
    COALESCE(etl_time, GETDATE()) AS etl_time,
    COALESCE(brand_user_id, '${brand_user_id}') AS brand_user_id
FROM ods_xhs_post_note_report_di
WHERE ds = '${bizdate}'
;
