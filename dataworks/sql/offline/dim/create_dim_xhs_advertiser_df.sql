CREATE TABLE IF NOT EXISTS dim_xhs_advertiser_df (
    advertiser_id STRING   COMMENT '投流账户ID',
    account_name  STRING   COMMENT '投流账户名称',
    project_id    STRING   COMMENT '项目ID',
    etl_time      DATETIME COMMENT 'ETL处理时间',
    dt            STRING   COMMENT '数据时间段'
) COMMENT '小红书投放账户维度表'
PARTITIONED BY (ds STRING COMMENT '分区日期');
