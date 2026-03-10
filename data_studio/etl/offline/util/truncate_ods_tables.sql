-- ============================================================
-- 清空 6 张 ODS 表指定 ds 分区
-- 调度参数: bizdate
-- ============================================================

ALTER TABLE ods_xhs_creative_report_hi DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_campaign_report_hi DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_keyword_report_di DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_searchword_report_di DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_audience_report_di DROP IF EXISTS PARTITION (ds='${bizdate}');
ALTER TABLE ods_xhs_account_flow_di DROP IF EXISTS PARTITION (ds='${bizdate}');
