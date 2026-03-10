CREATE TABLE IF NOT EXISTS dim_xhs_creativity_df (
    creativity_id     STRING   COMMENT '创意ID',
    creativity_name   STRING   COMMENT '创意名称',
    unit_id           STRING   COMMENT '单元ID',
    campaign_id       STRING   COMMENT '计划ID',
    campaign_group_id STRING   COMMENT '广告组ID',
    advertiser_id     STRING   COMMENT '投流账户ID',
    project_id        STRING   COMMENT '项目ID',
    creativity_status STRING   COMMENT '创意状态(F/T)',
    etl_time          DATETIME COMMENT 'ETL处理时间',
    dt                STRING   COMMENT '数据时间段'
) COMMENT '小红书创意维度表'
PARTITIONED BY (ds STRING COMMENT '分区日期');
