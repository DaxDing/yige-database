CREATE TABLE IF NOT EXISTS dim_xhs_target_df (
    target_id     STRING   COMMENT '定向包ID',
    target_name   STRING   COMMENT '定向包名称',
    project_id    STRING   COMMENT '项目ID',
    unit_id       STRING   COMMENT '单元ID',
    campaign_id   STRING   COMMENT '计划ID',
    advertiser_id STRING   COMMENT '投流账户ID',
    etl_time      DATETIME COMMENT 'ETL处理时间',
    dt            STRING   COMMENT '数据时间段'
) COMMENT '小红书定向包维度表'
PARTITIONED BY (ds STRING COMMENT '分区日期');
