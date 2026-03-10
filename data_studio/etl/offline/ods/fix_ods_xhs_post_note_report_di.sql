-- ============================================================
-- 补充 ODS 层 etl_time，清理 raw_data 零值键（支持嵌套）
-- 源表/目标表: ods_xhs_post_note_report_di
-- 上游依赖: sync_xhs_post_note_report_di
-- 下游依赖: etl_xhs_post_note_daily
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_post_note_report_di PARTITION (ds='${bizdate}')
SELECT
    dt,
    -- 清理 raw_data 中值为 0/空的键值对（支持嵌套，迭代3次）
    REGEXP_REPLACE(
    REGEXP_REPLACE(
    REGEXP_REPLACE(
        -- 第3次迭代
        REGEXP_REPLACE(
        REGEXP_REPLACE(
        REGEXP_REPLACE(
            -- 第2次迭代
            REGEXP_REPLACE(
            REGEXP_REPLACE(
            REGEXP_REPLACE(
                -- 第1次迭代：清理零值键值对
                REGEXP_REPLACE(
                REGEXP_REPLACE(
                REGEXP_REPLACE(
                    raw_data,
                    '"[^"]+":"(0|0\\.0|0\\.0%|)",?',  -- 字符串零值
                    ''
                ),
                '"[^"]+":(0|0\\.0)(,|(?=}))',        -- 数值零值
                ''
                ),
                '"[^"]+":null,?',                    -- null值
                ''
                ),
            ',}', '}'                                -- 修复末尾逗号
            ),
            '\\{,', '{'                              -- 修复开头逗号
            ),
            '"[^"]+":\\{\\},?', ''                   -- 清理空对象
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
    '"[^"]+":\\{\\},?', ''                           -- 清理空对象
    )                                             AS raw_data,
    COALESCE(etl_time, GETDATE())                 AS etl_time,
    brand_user_id
FROM ods_xhs_post_note_report_di
WHERE ds = '${bizdate}'
;
