INSERT OVERWRITE TABLE dim_xhs_ad_product_df PARTITION (ds='${bizdate}')
SELECT
    COALESCE(h.ad_product_id,
        CONCAT(t.project_id, LPAD(CAST(ROW_NUMBER() OVER(PARTITION BY t.project_id ORDER BY t.ad_product_name) AS STRING), 3, '0'))
    ) AS ad_product_id,
    t.ad_product_name,
    t.project_id,
    t.brand_name,
    t.product_category,
    GETDATE() AS etl_time,
    t.dt
FROM dim_xhs_ad_product_df t
LEFT JOIN (
    SELECT ad_product_id, project_id, ad_product_name
    FROM dim_xhs_ad_product_df
    WHERE ds < '${bizdate}'
    GROUP BY ad_product_id, project_id, ad_product_name
) h ON t.project_id = h.project_id AND t.ad_product_name = h.ad_product_name
WHERE t.ds = '${bizdate}';
