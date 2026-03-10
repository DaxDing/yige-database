-- ============================================================
-- 清空 4 张 ODS 实时表指定 ds 分区
-- 调度参数: bizdate
-- ============================================================

ALTER TABLE ods_xhs_creative_realtime_hi DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_campaign_realtime_hi DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_keyword_realtime_hi DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_target_realtime_hi DROP IF EXISTS PARTITION (ds='${bizdate}');
