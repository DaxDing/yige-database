# ads_xhs_note_bycontent_daily_agg 计算字段

## 计算字段列表

| 字段名 | 中文名 | 计算公式 |
|--------|--------|----------|
| cpm | 千次曝光成本 | `fee / impression * 1000` |
| cpe | 单次互动成本 | `fee / interaction` |
| cpc | 单次阅读成本 | `fee / read_uv` |
| ctr | 阅读率 | `read_uv / impression` |
| search_cmt_click_ctr | 搜索组件CTR | `search_cmt_click / search_cmt_impression` |
| cpuv | 单UV成本 | `fee / enter_shop_uv` |
| enter_shop_rate | 进店率 | `enter_shop_uv / read_uv` |
| new_visitor_rate | 新访客率 | `shop_new_visitor_uv / enter_shop_uv` |
| conversion_rate | 成交转化率 | `shop_order_uv / enter_shop_uv` |
| average_order_value | 客单价 | `shop_order_gmv / shop_order_uv` |
| rpv | UV价值 | `shop_order_gmv / enter_shop_uv` |
| new_customer_rate | 新客率 | `shop_new_customer_uv / enter_shop_uv` |
| cac | 新客成本 | `fee / shop_new_customer_uv` |
| roi | 全店ROI | `shop_order_gmv / fee` |
| single_product_roi | 单品ROI | `task_product_gmv / fee` |

## 维度字段

| 字段名 | 中文名 | 类型 |
|--------|--------|------|
| project_id | 项目ID | STRING |
| attribution_period | 归因口径 | INTEGER |
| dt | 数据更新日期 | INTEGER |
| brand_name | 归属品牌 | STRING |
| product_category | 归属品类 | STRING |
| delivery_product | 归属产品 | STRING |
| kol_name | 博主昵称 | STRING |
| note_id | 笔记ID | STRING |

## 基础字段（聚合/原始）

| 字段名 | 中文名 | 类型 |
|--------|--------|------|
| fee | 总金额 | DECIMAL |
| ad_fee | 投流金额 | DECIMAL |
| kols_fee | 蒲公英金额 | INTEGER |
| note_count | 笔记数量 | INTEGER |
| impression | 曝光量 | INTEGER |
| read_uv | 阅读量 | INTEGER |
| interaction | 互动量 | INTEGER |
| search_cmt_click | 搜索组件点击数 | INTEGER |
| search_cmt_impression | 搜索组件曝光数 | INTEGER |
| enter_shop_uv | 星河-进店UV | INTEGER |
| shop_new_visitor_uv | 星河-店铺新访客 | INTEGER |
| shop_order_uv | 星河-全店成交UV | INTEGER |
| shop_new_customer_uv | 星河-店铺新客UV | INTEGER |
| shop_order_gmv | 星河-全店成交GMV | DECIMAL |
| task_product_gmv | 星河-单品成交GMV | DECIMAL |
