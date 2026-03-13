# 数据术语表

小红书营销数仓标准术语（267 项），建表、字段命名、指标定义时引用。

- **attr**: 归因层级（创意/内容/任务组）
- **scope**: 统计口径（每日/日累计/回溯至统计日）

### 标识属性

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| ad_product_id | 投放产品ID | STRING | - | - | - |
| ad_product_name | 投放产品名称 | STRING | - | - | - |
| advertiser_id | 投放账号ID | STRING | - | - | - |
| advertiser_name | 投放账号名称 | STRING | - | - | - |
| apply_id | 资质ID | STRING | - | - | - |
| apply_name | 资质名称 | STRING | - | - | - |
| brand_id | 品牌ID | STRING | - | - | - |
| brand_name | 品牌名称 | STRING | - | - | - |
| brand_qual_id | 品牌资质ID | STRING | - | - | - |
| brand_qual_name | 品牌资质名称 | STRING | - | - | - |
| brand_user_id | 品牌商ID | STRING | - | - | - |
| brand_user_name | 品牌商名称 | STRING | - | - | - |
| campaign_group_id | 广告组ID | STRING | - | - | - |
| campaign_group_name | 广告组名称 | STRING | - | - | - |
| campaign_id | 计划ID | STRING | - | - | - |
| campaign_name | 计划名称 | STRING | - | - | - |
| comment_comp_type | 评论区组件类型 | INT | - | - | - |
| content_comp_type | 正文组件类型 | INT | - | - | - |
| creativity_id | 创意ID | STRING | - | - | - |
| creativity_name | 创意名称 | STRING | - | - | - |
| exec_dept_id | 执行部门ID | STRING | - | - | - |
| exec_dept_name | 执行部门 | STRING | - | - | - |
| group_id | 人群包ID | STRING | - | - | - |
| is_last_click | 是否去重 | STRING | - | - | 用于转化指标的去重问题 |
| is_proxy | 是否代投笔记 | STRING | - | - | - |
| kol_id | 达人ID | STRING | - | - | 博主ID |
| kol_name | 博主名称 | STRING | - | - | 博主昵称/达人昵称 |
| kol_red_id | 小红书ID | STRING | - | - | - |
| note_id | 笔记ID | STRING | - | - | - |
| note_name | 笔记名称 | STRING | - | - | 笔记标题 |
| order_id | 订单ID | STRING | - | - | - |
| order_name | 订单名称 | STRING | - | - | - |
| project_id | 项目ID | STRING | - | - | - |
| project_name | 项目名称 | STRING | - | - | - |
| spu_id | SPU ID | STRING | - | - | - |
| spu_name | SPU名称 | STRING | - | - | - |
| sub_task_id | 子任务ID | STRING | - | - | - |
| sub_task_name | 子任务名称 | STRING | - | - | - |
| target_id | 定向ID | STRING | - | - | - |
| target_name | 定向名称 | INT | - | - | - |
| task_id | 任务组ID | STRING | - | - | - |
| task_name | 任务组名称 | STRING | - | - | - |
| unit_id | 单元ID | STRING | - | - | - |
| unit_name | 单元名称 | STRING | - | - | - |
| user_id | 用户ID | STRING | - | - | - |
| user_name | 用户名称 | STRING | - | - | - |
| virtual_seller_id | 子账户ID | STRING | - | - | 代理商vsellerId |
| virtual_seller_name | 子账户名称 | STRING | - | - | - |
| xhs_product_id | 跨域项目ID | STRING | - | - | - |
| xhs_product_name | 跨域项目名称 | STRING | - | - | - |

### 时间维度

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| delivery_date | 投放日期 | DATE | - | - | - |
| dt | 日期 | DATE | - | - | - |
| event_group_end_time | 联盟结束时间 | DATETIME | - | - | - |
| event_group_start_time | 联盟开始时间 | DATETIME | - | - | - |
| hh | 小时 | STRING | - | - | - |
| month | 月 | STRING | - | - | - |
| week | 周 | STRING | - | - | - |
| year | 年 | STRING | - | - | - |

### 内容维度

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| content_category | 内容类目 | INT | - | - | - |
| content_subtype | 内容分型 | STRING | - | - | 内容细分类型 |
| content_theme | 内容方向 | STRING | - | - | 内容主题 |
| note_source | 笔记来源 | STRING | - | - | - |
| note_type | 笔记类型 | INT | - | - | - |
| note_url | 笔记链接 | STRING | - | - | - |

### 达人维度

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| kol_type | 达人类型 | STRING | - | - | - |
| kol_url | 达人链接 | STRING | - | - | - |

### 产品维度

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| industry_category | 行业类目 | INT | - | - | - |
| product_category | 产品品类 | STRING | - | - | 品牌商内部的品类区分 |

### 定向维度

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| crowd_target | 人群包 | INT | - | - | - |
| industry_interest_target | 行业兴趣 | INT | 创意 | - | - |
| intelligent_expansion | 智能扩量 | STRING | - | - | - |
| interest_keywords | 关键词兴趣定向 | STRING | 创意 | - | - |
| keywords | 关键词定向 | STRING | 创意 | - | - |
| reverse_target_crowd | 排除特定人群 | INT | 创意 | - | - |
| search_target_city_intent | 搜索意图城市定向 | INT | 创意 | - | - |
| target_age | 年龄定向 | INT | 创意 | - | - |
| target_city | 城市定向 | INT | 创意 | - | 城市 |
| target_device | 设备定向 | INT | 创意 | - | - |
| target_device_price | 手机价格 | INT | 创意 | - | 设备价格 |
| target_gender | 性别定向 | INT | 创意 | - | - |
| target_type | 定向类型 | STRING | - | - | - |

### 活动策略

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| bidding_strategy | 竞价策略 | INT | 创意 | - | 出价方式 |
| delivery_days | 投放天数 | STRING | - | - | - |
| execution_element | 执行要素 | STRING | - | - | 执行层面的关键要素 |
| kfs_type | KFS | STRING | - | - | KOL/Feed/Search 投放策略类型 |
| delivery_period | 投放节奏 | STRING | - | - | - |
| delivery_strategy | 投放策略 | STRING | - | - | - |
| marketing_target | 营销目标 | INT | 创意 | - | 营销诉求 |
| optimize_target | 优化目标 | INT | 创意 | - | - |
| placement | 投放位置 | INT | 创意 | - | 广告类型 |
| product_selling_points | 属性买点 | STRING | - | - | - |
| promotion_target | 标的类型 | INT | - | - | 推广标的类型 |

### 规划指标

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| budget | 预算 | DECIMAL | - | 每日 | - |
| budget_ratio | 预算占比 | DECIMAL | - | - | - |
| effective_budget | 有效预算 | DECIMAL | - | - | - |
| execution_detail_cost | 执行细项费用 | DECIMAL | - | - | - |
| feed_budget | 信息流预算 | DECIMAL | - | - | - |
| image_text_count_budget | 图文数量预估 | BIGINT | - | - | - |
| kol_budget | 达人预算 | DECIMAL | - | - | - |
| phase_budget | 分阶段预算 | DECIMAL | - | - | - |
| phase_budget_ratio | 分阶段预算占比 | DECIMAL | - | - | - |
| phase_total_budget | 阶段总预算 | DECIMAL | - | - | - |
| plan_image_text_cnt | 图文规划数量 | INT | - | - | - |
| plan_video_cnt | 视频规划数量 | INT | - | - | - |
| planned_note_count | 笔记数量规划 | BIGINT | - | - | - |
| search_budget | 搜索流预算 | DECIMAL | - | - | - |

| total_budget | 总预算 | DECIMAL | - | - | - |
| video_count_budget | 视频数量预估 | BIGINT | - | - | - |

### 流量指标

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| 
engage_num | 互动量 | BIGINT | 内容 | 日累计 | 全部互动效果 |
| action_button_click | 行动按钮点击量 | BIGINT | 创意 | 每日 | - |
| avg_view_time | 平均浏览时长(秒) | DECIMAL | 内容 | 日累计 | - |
| click | 点击量 | BIGINT | - | - | - |
| cmt_num | 评论量 | INT | 内容 | 日累计 | 全部互动效果 |
| content_comp_click | 内容组件点击量 | BIGINT | 内容 | 日累计 | - |
| content_comp_impression | 内容组件展现量 | BIGINT | 内容 | 日累计 | - |
| discovery_impression | 发现页展现量 | BIGINT | - | - | - |
| engage_comp_click | 互动组件点击量 | BIGINT | 内容 | 日累计 | 互动组件参与人数 |
| engage_comp_impression | 互动组件展现量 | BIGINT | 内容 | 日累计 | 互动组件组件总曝光人数 |
| fav_num | 收藏量 | INT | 内容 | 日累计 | 全部互动效果 |
| feed_interest | 推荐场种草数 | STRING | 内容 | 日累计 | - |
| finish_rate | 视频完播率 | DECIMAL | 内容 | 日累计 | - |
| follow_read | 关注阅读 | STRING | 内容 | 日累计 | 阅读来源分布占比（自然流量）-关注页 |
| heat_impression | 加热展现量 | BIGINT | 内容 | 日累计 | 加热曝光量 |
| heat_read | 加热阅读量 | BIGINT | 内容 | 日累计 | - |
| i_user_num | 新增种草人群 | BIGINT | 创意 | 每日 | 产品种草 |
| imp_num | 曝光量 | BIGINT | 内容 | 日累计 | 全部流量效果 |
| impression | 展现量 | BIGINT | - | - | 曝光量 |
| interest | 种草数 | STRING | 内容 | 日累计 | - |
| kol_tier | 达人量级 | INT | - | - | - |
| like_num | 点赞量 | INT | 内容 | 日累计 | 全部互动效果 |
| origin_impression | 自然流曝光 | BIGINT | 内容 | 日累计 | - |
| origin_read | 自然流阅读量 | BIGINT | 内容 | 日累计 | - |
| other_interest | 其他场种草数 | STRING | 内容 | 日累计 | - |
| pic_read_3s_rate | 3s阅读率 | DECIMAL | 内容 | 日累计 | - |
| promotion_impression | 推广展现量 | BIGINT | - | - | - |
| promotion_read | 推广阅读量 | STRING | 内容 | 日累计 | - |
| read_num | 阅读量 | BIGINT | 内容 | 日累计 | 全部流量效果 |
| read_uv | 阅读量 | BIGINT | - | - | - |
| read_uv | 阅读UV | INT | 内容 | 日累计 | 全部流量效果的阅读UV |
| reserve_pv | 预告组件点击量 | BIGINT | 创意 | 每日 | - |
| search_cmt_after_read | 搜后阅读量 | BIGINT | 创意 | 每日 | 产品种草 |
| search_cmt_click | 搜索组件点击量 | BIGINT | 创意 | 每日 | 产品种草，蒲公英的content_comp_click+蒲公英的content_comp_click |
| search_cmt_impression | 搜索组件展现量 | BIGINT | 内容 | 日累计 | 搜索组件曝光量; 产品种草，蒲公英的content_comp_impression+蒲公英的comp_impression |
| search_impression | 搜索页展现量 | BIGINT | 内容 | 日累计 | 曝光来源分布占比（自然流量）
-搜索页 |
| search_interest | 搜索场种草数 | STRING | 内容 | 日累计 | - |
| search_read | 搜索阅读量 | BIGINT | 内容 | 日累计 | 阅读来源分布占比（自然流量）-搜索页 |
| share_num | 分享量 | INT | 内容 | 日累计 | 全部互动效果 |
| third_cmt_num | 评论uv | INT | 内容 | 日累计 | 跨域项目数据 |
| third_fav_num | 收藏uv
 | INT | 内容 | 日累计 | 跨域项目数据 |
| third_like_num | 点赞uv | INT | 内容 | 日累计 | 跨域项目数据 |
| third_share_num | 分享uv | INT | 内容 | 日累计 | 跨域项目数据 |
| ti_user_num | 新增深度种草人群 | BIGINT | 创意 | 每日 | 产品种草 |
| video_play_5s_cnt | 5秒播放量 | BIGINT | 创意 | 每日 | - |
| video_play_5s_rate | 5s完播率 | DECIMAL | 创意 | 每日 | - |

### 互动指标

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| collect | 收藏 | BIGINT | - | 每日/日累计 | - |
| comment | 评论 | BIGINT | - | 每日/日累计 | - |
| follow | 关注 | BIGINT | 创意 | 每日 | - |
| interaction | 互动量 | BIGINT | - | - | - |
| like | 点赞 | BIGINT | - | 每日/日累计 | - |
| pic_save | 保存图片 | BIGINT | 创意 | 每日 | - |
| screenshot | 截图 | BIGINT | 创意 | 每日 | - |
| share | 分享 | BIGINT | - | 每日/日累计 | - |

### 转化指标

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| action_button_ctr | 行动按钮点击转化率 | DECIMAL | - | - | 产品种草 |
| add_cart_rate | 加购率 | DECIMAL | - | - | - |
| add_cart_uv | 加购UV | BIGINT | 任务组/内容 | 每日 | 商品加购UV; 产品种草 |
| app_activate_amount_1d | 当日LTV | STRING | 创意 | 每日 | 应用推广 |
| app_activate_amount_3d | 三日LTV | STRING | 创意 | 回溯至统计日 | 应用推广 |
| app_activate_amount_7d | 七日LTV | STRING | 创意 | 回溯至统计日 | 应用推广 |
| app_activate_cnt | 激活数 | BIGINT | 创意 | 每日 | 应用推广 |
| app_key_action_cnt | 关键行为数 | BIGINT | 创意 | 每日 | 应用推广 |
| app_pay_cnt_7d | 7日付费次数 | STRING | 创意 | 回溯至统计日 | 应用推广 |
| app_register_cnt | 注册数 | BIGINT | 创意 | 每日 | 应用推广 |
| average_order_value | 客单价 | DECIMAL | 任务组/内容 | 每日/日累计 | 全店成交客单价/成交客单价 |
| cac | 新客成本 | DECIMAL | 任务组/内容 | 每日/日累计 | 产品种草 |
| content_interaction_rate | 内容互动率 | DECIMAL | 任务组/内容 | 每日 | 产品种草 |
| conversion_rate | 转化率 | DECIMAL | 任务组/内容 | 每日/日累计 | 成交转化率/意向行为转化率; 产品种草 |
| cp | 消费意向 | STRING | 内容 | 日累计 | - |
| current_app_pay_cnt | 当日付费次数 | BIGINT | 创意 | 每日 | 应用推广 |
| customer_acquisition_rate | 拉客率 | DECIMAL | - | - | 产品种草 |
| daily_organic_shop_uv | 日均自然进店UV | BIGINT | - | - | - |
| enter_shop_uv | 进店UV | BIGINT | 任务组/内容 | 每日 | 产品种草 |
| external_goods_order_15 | 行业商品成交订单量（15日） | BIGINT | 创意 | 回溯至统计日 | 种草直达 |
| external_goods_order_30 | 行业商品成交订单量（30日） | BIGINT | 创意 | 回溯至统计日 | 种草直达 |
| external_goods_order_7 | 行业商品成交订单量（7日） | BIGINT | 创意 | 回溯至统计日 | 种草直达 |
| external_goods_visit_7 | 行业商品点击量 | BIGINT | 创意 | 每日 | 种草直达 |
| first_app_pay_cnt | 首次付费数 | BIGINT | 创意 | 回溯至统计日 | 应用推广 |
| initiative_message | 私信开口数 | BIGINT | 创意 | 每日 | 客资收集 |
| invoke_app_engagement_cnt | APP互动量（唤起） | BIGINT | 创意 | 每日 | 应用推广 |
| invoke_app_enter_store_cnt | APP进店量（唤起） | BIGINT | 创意 | 每日 | 应用推广 |
| invoke_app_open_cnt | APP打开量（唤起） | BIGINT | 创意 | 每日 | 应用推广 |
| invoke_app_payment_cnt | APP支付次数（唤起） | BIGINT | 创意 | 每日 | 应用推广 |
| jd_active_num | 京东站外活跃行为UV | INT | 内容 | 回溯至统计日 | - |
| landing_page_visit | 落地页访问量 | BIGINT | 创意 | 每日 | 客资收集 |
| leads | 表单提交 | BIGINT | 创意 | 每日 | 客资收集 |
| leads_button_impression | 表单按钮曝光量 | BIGINT | 创意 | 每日 | 客资收集 |
| main_product_deal_gmv | 主推商品成交GMV | BIGINT | - | - | 产品种草 |
| main_product_deal_uv | 主推商品成交UV | BIGINT | - | - | 产品种草 |
| main_product_order_gmv | 主推商品下单GMV | BIGINT | - | - | 产品种草 |
| main_product_order_uv | 主推商品下单UV | BIGINT | - | - | 产品种草 |
| message | 私信开口条数 | BIGINT | 创意 | 每日 | 客资收集 |
| message_consult | 私信进线数 | INT | 创意 | 每日 | 客资收集 |
| message_user | 私信进线人数 | BIGINT | 创意 | 每日 | 客资收集 |
| msg_leads_num | 私信留资数 | BIGINT | 创意 | 每日 | 客资收集 |
| new_visitor_cost | 新访客成本 | DECIMAL | - | - | 产品种草 |
| new_visitor_rate | 新访客率 | DECIMAL | 任务组/内容 | 每日/日累计 | 店铺新访客率; 产品种草 |
| non_task_product_gmv | 非任务商品成交GMV | DECIMAL | 任务组/内容 | 每日 | 非任务商品成交 GMV (元); 产品种草 |
| offsite_action_cvr | 站外行为转化率 | DECIMAL | - | - | - |
| order_amount | 订单流水 | DECIMAL | - | - | - |
| order_gmv | 下单GMV | BIGINT | - | - | 产品种草 |
| order_uv | 下单UV | BIGINT | - | - | 产品种草 |
| organic_shop_uv | 自然进店UV | BIGINT | - | - | - |
| presale_deposit_gmv | 预售付定GMV | DECIMAL | 任务组/内容 | 每日 | preSaleAlipayAmtShop,预售付定 GMV (元); 产品种草 |
| presale_deposit_uv | 预售付定UV | BIGINT | 任务组/内容 | 每日 | 产品种草 |
| presale_estimated_gmv | 预售整单预估GMV | DECIMAL | 任务组/内容 | 每日 | 预售整单预估 GMV (元); 产品种草 |
| product_collect | 商品收藏UV | BIGINT | - | - | 产品种草 |
| product_detail_uv | 商详浏览UV | BIGINT | - | - | 产品种草 |
| retention_1d_cnt | 次留 | BIGINT | 创意 | 回溯至统计日 | 应用推广 |
| retention_3d_cnt | 3日留存 | BIGINT | 创意 | 回溯至统计日 | 应用推广 |
| retention_7d_cnt | 7日留存 | BIGINT | 创意 | 回溯至统计日 | 应用推广 |
| roas | 广告支出回报率 | DECIMAL | - | - | - |
| search_impression_uv | 搜索曝光UV | BIGINT | - | - | 产品种草 |
| search_invoke_button_click_cnt | APP打开按钮点击量（唤起） | BIGINT | 创意 | 每日 | 应用推广 |
| search_revisit_rate | 回搜率 | DECIMAL | - | - | 产品种草 |
| search_view_uv | 搜索浏览UV | BIGINT | - | - | 产品种草 |
| shop_member_uv | 店铺会员UV | BIGINT | 任务组/内容 | 每日 | 产品种草 |
| shop_new_customer_uv | 新客UV | BIGINT | 任务组/内容 | 每日 | 店铺新客 UV; 产品种草 |
| shop_new_visitor_uv | 新访客UV | BIGINT | 任务组/内容 | 每日 | 店铺新访客/店铺新访客 UV; 产品种草 |
| shop_order_gmv | 成交GMV | DECIMAL | 任务组/内容 | 每日 | 全店成交 GMV (元); 产品种草 |
| shop_order_uv | 成交UV | BIGINT | 任务组/内容 | 每日 | 全店成交 UV; 产品种草 |
| taobao_search_enter_shop_uv | 手淘搜索进店UV | BIGINT | 任务组/内容 | 每日 | 产品种草 |
| taobao_search_impression_uv | 手淘搜索曝光UV | BIGINT | 任务组/内容 | 每日 | 产品种草 |
| task_product_gmv | 任务商品成交GMV | DECIMAL | 任务组/内容 | 每日 | 任务商品成交 GMV (元); 产品种草 |
| task_product_new_customer_gmv | 任务商品新客成交GMV | DECIMAL | 任务组/内容 | 每日 | 任务商品新客成交 GMV (元); 产品种草 |

### 成本指标

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| app_activate_cost | 激活成本 | DECIMAL | 创意 | 每日 | 应用推广 |
| app_pay_amount | 付费金额 | DECIMAL | 创意 | 每日 | 应用推广 |
| cash_amount | 现金消费 | DECIMAL | - | - | - |
| cost_per_conversion | 成交成本 | DECIMAL | - | - | - |
| cpax | 行动成本 | DECIMAL | - | - | - |
| cpe | 平均互动成本 | DECIMAL | 内容 | - | 单位互动成本 |
| cpi | 互动单价 | DECIMAL | 创意 | 每日 | 平均互动成本 |
| cpm | 平均千次展示消费 | DECIMAL | 内容 | - | 千人展现成本 |
| cpti | 深度种草成本 | DECIMAL | - | - | - |
| external_goods_order_price_15 | 行业商品成交订单成本（15日） | DECIMAL | 创意 | 回溯至统计日 | 种草直达 |
| external_goods_order_price_30 | 行业商品成交订单成本（30日） | DECIMAL | 创意 | 回溯至统计日 | 种草直达 |
| external_goods_order_price_7 | 行业商品成交订单成本（7日） | DECIMAL | 创意 | 回溯至统计日 | 应用推广 |
| external_rgmv_15 | 行业商品GMV（15日） | STRING | 创意 | 回溯至统计日 | 种草直达 |
| external_rgmv_30 | 行业商品GMV（30日） | STRING | 创意 | 回溯至统计日 | 种草直达 |
| external_rgmv_7 | 行业商品GMV（7日） | STRING | 创意 | 回溯至统计日 | 种草直达 |
| fee | 消费 | DECIMAL | - | - | 总金额 |
| first_app_pay_cost | 首次付费成本 | DECIMAL | 创意 | 每日 | 应用推广 |
| invoke_app_open_cost | APP打开成本（唤起） | DECIMAL | 创意 | 每日 | 应用推广 |
| invoke_app_payment_amount | APP支付金额（唤起） | DECIMAL | 创意 | 每日 | 应用推广 |
| invoke_app_payment_cost | APP订单支付成本（唤起） | DECIMAL | 创意 | 每日 | 应用推广 |
| pgy_actual_amt | 蒲公英实际金额 | DECIMAL | - | - | - |
| third_bcoo_income_amt | 蒲公英金额 | DECIMAL | 内容 | - | - |

### 业务指标

| en | cn | type | attr | scope | desc |
|---|---|---|---|---|---|
| ad_budget | 投流预算 | DECIMAL | - | - | - |
| ad_click | 投流点击量 | BIGINT | 创意 | 每日 | 展现量 |
| ad_cpuv | 投流 CPUV | DECIMAL | - | - | - |
| ad_enter_shop_uv | 投流进店UV | BIGINT | - | - | - |
| ad_fee | 投流消费 | DECIMAL | 创意 | 每日 | 消费 |
| ad_impression | 投流展现量 | BIGINT | 创意 | 每日 | 展现量 |
| ad_interaction | 投流互动量 | BIGINT | 创意 | 每日 | 互动量 |
| jd_ad_fee | 小红盟投流消费 | DECIMAL | - | - | - |
| jd_fee | 小红盟消费 | DECIMAL | - | - | - |
| note_count | 笔记数量 | BIGINT | - | - | - |
| tb_ad_fee | 小红星投流消费 | DECIMAL | - | - | - |
| tb_fee | 小红星消费 | DECIMAL | - | - | - |
