-- ============================================================
-- 清理: ODS 种草联盟转化表生命周期管理
-- 说明: 删除 7 天前的 ODS 全量快照分区，节省存储
-- 调度: 放在 DWD ETL 之后执行
-- ============================================================

ALTER TABLE ods_xhs_grass_bycontent_conversion_df DROP IF EXISTS PARTITION (ds < '$[yyyymmdd-7]');
ALTER TABLE ods_xhs_grass_bytask_conversion_df DROP IF EXISTS PARTITION (ds < '$[yyyymmdd-7]');
