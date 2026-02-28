-- ============================================================
-- 去重 ODS 搜索词报表
-- 去重键: search_word + dt + raw_data 内 campaign_id + unit_id + creativity_id
-- 说明: 同一搜索词在不同计划/单元/创意下各有记录，属正常数据
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_searchword_report_di PARTITION (ds='${bizdate}')
SELECT
    search_word,
    dt,
    raw_data,
    etl_time
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY search_word, dt,
                GET_JSON_OBJECT(raw_data, '$.campaign_id'),
                GET_JSON_OBJECT(raw_data, '$.unit_id'),
                GET_JSON_OBJECT(raw_data, '$.creativity_id')
            ORDER BY etl_time DESC
        ) AS rn
    FROM ods_xhs_searchword_report_di
    WHERE ds = '${bizdate}'
) t
WHERE rn = 1
;
