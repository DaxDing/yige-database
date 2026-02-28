-- ============================================================
-- 删除笔记报表 ODS 表指定 ds 分区
-- 调度参数: bizdate
-- ============================================================

ALTER TABLE ods_xhs_post_note_report_di DROP IF EXISTS PARTITION (ds='${bizdate}');
