# ads_xhs_task_group_bytask_daily_agg 计算字段

## 计算字段列表

| 字段名 | 中文名 | 计算公式 |
|--------|--------|----------|
| enter_shop_rate | 进店率 | `enter_shop_uv / read_uv` |
| conversion_rate | 成交转化率 | `shop_order_uv / enter_shop_uv` |
| average_order_value | 客单价 | `shop_order_gmv / shop_order_uv` |
| collect_rate | 收加率 | 待确认 |
| rpv | UV价值 | `shop_order_gmv / enter_shop_uv` |
| cpuv | CPUV【综合】 | `fee / enter_shop_uv` |
| roi | ROI | `shop_order_gmv / fee` |

## 基础字段（聚合/原始）

| 字段名 | 中文名 | 类型 |
|--------|--------|------|
| attribution_period | 归因口径 | INTEGER |
| dt | 数据更新日期 | INTEGER |
| ad_product_name | 归属产品 | STRING |
| task_group_name | 任务组 | STRING |
| read_uv | 阅读/播放UV | INTEGER |
| enter_shop_uv | 进店UV | INTEGER |
| shop_order_uv | 成交UV | INTEGER |
| shop_order_gmv | 成交GMV | DECIMAL |
| task_product_gmv | 任务商品成交GMV | DECIMAL |
| kols_fee | 蒲公英金额 | DECIMAL |
| ad_fee | 投流金额 | DECIMAL |
| fee | 总金额 | DECIMAL |
