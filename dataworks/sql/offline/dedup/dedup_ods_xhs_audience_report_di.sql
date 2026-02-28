-- ============================================================
-- 去重 ODS 人群包报表
-- 去重键: group_id + dt + raw_data 内 campaignId + unitId + creativityId
-- 说明: 同一人群包在不同计划/单元/创意下各有记录，属正常数据
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_audience_report_di PARTITION (ds='${bizdate}')
SELECT
    group_id,
    dt,
    raw_data,
    etl_time
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY group_id, dt,
                GET_JSON_OBJECT(raw_data, '$.campaignId'),
                GET_JSON_OBJECT(raw_data, '$.unitId'),
                GET_JSON_OBJECT(raw_data, '$.creativityId')
            ORDER BY etl_time DESC
        ) AS rn
    FROM ods_xhs_audience_report_di
    WHERE ds = '${bizdate}'
) t
WHERE rn = 1
;
