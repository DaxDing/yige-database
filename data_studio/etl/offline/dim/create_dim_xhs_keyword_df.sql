CREATE TABLE IF NOT EXISTS dim_xhs_keyword_df (
    keyword_id  STRING   COMMENT '关键词ID',
    keyword_name STRING  COMMENT '关键词名称',
    project_id  STRING   COMMENT '项目ID',
    unit_id     STRING   COMMENT '单元ID',
    campaign_id   STRING   COMMENT '计划ID',
    advertiser_id STRING   COMMENT '投流账户ID',
    placement     STRING   COMMENT '投放位置',
    etl_time      DATETIME COMMENT 'ETL处理时间',
    dt          STRING   COMMENT '数据时间段'
) COMMENT '小红书关键词维度表'
PARTITIONED BY (ds STRING COMMENT '分区日期');
