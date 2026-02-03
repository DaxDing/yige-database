INSERT OVERWRITE TABLE dim_xhs_ad_product_df PARTITION (ds='${bizdate}')
SELECT
    COALESCE(h.ad_product_id,
        CONCAT(t.project_id, LPAD(CAST(ROW_NUMBER() OVER(PARTITION BY t.project_id ORDER BY t.ad_product_name) AS STRING), 3, '0'))
    ) AS ad_product_id,
    t.ad_product_name,
    t.project_id,
    t.brand_name,
    t.product_category,
    t.etl_time,
    t.dt
FROM (
    -- 当天数据按 (project_id, ad_product_name) 去重，确保重跑幂等
    SELECT ad_product_name, project_id, brand_name, product_category, etl_time, dt
    FROM (
        SELECT ad_product_name, project_id, brand_name, product_category, etl_time, dt,
               ROW_NUMBER() OVER(PARTITION BY project_id, ad_product_name ORDER BY etl_time DESC) AS rn
        FROM dim_xhs_ad_product_df
        WHERE ds = '${bizdate}'
    ) dedup
    WHERE rn = 1
) t
LEFT JOIN (
    -- 历史数据取最新 ad_product_id，确保唯一
    SELECT project_id, ad_product_name, ad_product_id
    FROM (
        SELECT project_id, ad_product_name, ad_product_id,
               ROW_NUMBER() OVER(PARTITION BY project_id, ad_product_name ORDER BY ds DESC) AS rn
        FROM dim_xhs_ad_product_df
        WHERE ds < '${bizdate}'
    ) ranked
    WHERE rn = 1
) h ON t.project_id = h.project_id AND t.ad_product_name = h.ad_product_name;
