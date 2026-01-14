/**
 * 小红书投流数据仓库 - 指标定义
 * 数据来源: DataWorks
 */

const METRICS = {
    version: "1.0",
    updateDate: "2026年1月",
    atomic: [
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_goods_visit_7",
        "nameCn": "行业商品点击量",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_goods_order_30",
        "nameCn": "行业商品成交订单量（30日）",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_goods_order_15",
        "nameCn": "行业商品成交订单量（15日）",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_rgmv_7",
        "nameCn": "行业商品GMV（7日）",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_rgmv_15",
        "nameCn": "行业商品GMV（15日）",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_rgmv_30",
        "nameCn": "行业商品GMV（30日）",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_goods_order_7",
        "nameCn": "行业商品成交订单量（7日）",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "cp",
        "nameCn": "消费意向",
        "function": "COUNT",
        "unit": "cny_yuan",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "interaction",
        "nameCn": "互动量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "interest",
        "nameCn": "种草数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "shop_order_gmv",
        "nameCn": "成交GMV",
        "function": "COUNT",
        "unit": "cny_yuan",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "shop_order_uv",
        "nameCn": "成交UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "enter_shop_uv",
        "nameCn": "进店UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "add_cart_uv",
        "nameCn": "加购UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "search_cmt_after_read",
        "nameCn": "搜后阅读量",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "search_interest",
        "nameCn": "搜索场种草数",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "other_interest",
        "nameCn": "其他场种草数",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "feed_interest",
        "nameCn": "推荐场种草数",
        "function": "",
        "unit": "cny_yuan",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "ti_user_num",
        "nameCn": "新增深度种草人群",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "i_user_num",
        "nameCn": "新增种草人群",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "shop_new_customer_uv",
        "nameCn": "新客UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "shop_new_visitor_uv",
        "nameCn": "新访客UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "ad_enter_shop_uv",
        "nameCn": "投流进店UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "daily_organic_shop_uv",
        "nameCn": "日均自然进店UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "organic_shop_uv",
        "nameCn": "自然进店UV",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "landing_page_visit",
        "nameCn": "落地页访问量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "leads_button_impression",
        "nameCn": "表单按钮曝光量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "message_user",
        "nameCn": "私信进线人数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "message",
        "nameCn": "私信开口条数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "msg_leads_num",
        "nameCn": "私信留资数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "initiative_message",
        "nameCn": "私信开口数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "leads",
        "nameCn": "表单提交",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.lg",
        "nameEn": "message_consult",
        "nameCn": "私信进线数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "ad_interaction",
        "nameCn": "投流互动量",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "search_read",
        "nameCn": "搜索阅读量",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "promotion_read",
        "nameCn": "推广阅读量",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "follow_read",
        "nameCn": "关注阅读",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "heat_read",
        "nameCn": "加热阅读量",
        "function": "",
        "unit": "",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "click",
        "nameCn": "点击量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "impression",
        "nameCn": "展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "like",
        "nameCn": "点赞",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "pic_save",
        "nameCn": "保存图片",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "screenshot",
        "nameCn": "截图",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "share",
        "nameCn": "分享",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "follow",
        "nameCn": "关注",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "collect",
        "nameCn": "收藏",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "comment",
        "nameCn": "评论",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "video_play_5s_cnt",
        "nameCn": "5秒播放量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "read_uv",
        "nameCn": "阅读量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(distinct user_id)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "ad_click",
        "nameCn": "投流点击量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "ad_impression",
        "nameCn": "投流展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "promotion_impression",
        "nameCn": "推广展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "discovery_impression",
        "nameCn": "发现页展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "heat_impression",
        "nameCn": "加热展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "search_impression",
        "nameCn": "搜索页展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "action_button_click",
        "nameCn": "行动按钮点击量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "reserve_pv",
        "nameCn": "预告组件点击",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "content_comp_click",
        "nameCn": "内容组件点击量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "content_comp_impression",
        "nameCn": "内容组件展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "comp_click",
        "nameCn": "组件点击量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "search_cmt_click",
        "nameCn": "搜索组件点击量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "comp_impression",
        "nameCn": "组件展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "engage_comp_impression",
        "nameCn": "互动组件展现量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "engage_comp_click",
        "nameCn": "互动组件点击量",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_activate_cnt",
        "nameCn": "激活数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_pay_amount",
        "nameCn": "付费金额",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_register_cnt",
        "nameCn": "注册数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "gmv",
        "nameCn": "商品交易总额",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "order_amount",
        "nameCn": "订单流水",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_key_action_cnt",
        "nameCn": "关键行为数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "search_invoke_button_click_cnt",
        "nameCn": "APP打开按钮点击量（唤起）",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "invoke_app_engagement_cnt",
        "nameCn": "APP互动量（唤起）",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_pay_cnt_7d",
        "nameCn": "7日付费次数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_activate_amount_1d",
        "nameCn": "当日LTV",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_activate_amount_3d",
        "nameCn": "三日LTV",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_activate_amount_7d",
        "nameCn": "七日LTV",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "retention_1d_cnt",
        "nameCn": "次留",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "retention_3d_cnt",
        "nameCn": "3日留存",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "retention_7d_cnt",
        "nameCn": "7日留存",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "invoke_app_payment_cnt",
        "nameCn": "APP支付次数（唤起）",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "invoke_app_payment_amount",
        "nameCn": "APP支付金额（唤起）",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "first_app_pay_cnt",
        "nameCn": "首次付费数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "current_app_pay_cnt",
        "nameCn": "当日付费次数",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "invoke_app_open_cnt",
        "nameCn": "APP打开量（唤起）",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "invoke_app_enter_store_cnt",
        "nameCn": "APP进店量（唤起）",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "total_budget",
        "nameCn": "总预算",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "video_count_budget",
        "nameCn": "视频数量预估",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "image_text_count_budget",
        "nameCn": "图文数量预估",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "kol_budget",
        "nameCn": "达人预算",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "phase_budget",
        "nameCn": "分阶段预算",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "phase_total_budget",
        "nameCn": "阶段总预算",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "effective_budget",
        "nameCn": "有效预算",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "budget",
        "nameCn": "预算",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "planned_note_count",
        "nameCn": "笔记数量规划",
        "function": "COUNT",
        "unit": "",
        "logic": "count(*) / sum(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "ad_budget",
        "nameCn": "投流预算",
        "function": "",
        "unit": "cny_yuan",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "feed_budget",
        "nameCn": "信息流预算",
        "function": "",
        "unit": "cny_yuan",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "search_budget",
        "nameCn": "搜索流预算",
        "function": "",
        "unit": "cny_yuan",
        "logic": "agg_function(field)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "fee",
        "nameCn": "消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "cash_amount",
        "nameCn": "现金消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "kols_fee",
        "nameCn": "蒲公英消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "jd_fee",
        "nameCn": "小红盟消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "tb_fee",
        "nameCn": "小红星消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(cost)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "jd_ad_fee",
        "nameCn": "小红盟投流消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "tb_ad_fee",
        "nameCn": "小红星投流消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "ad_fee",
        "nameCn": "投流消费",
        "function": "SUM",
        "unit": "cny_yuan",
        "logic": "sum(amount)"
    },
    {
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.ad_default",
        "nameEn": "kol_tier",
        "nameCn": "达人量级",
        "function": "",
        "unit": "",
        "logic": "kol_tier"
    }
],
    composite: [
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "budget_ratio",
        "nameCn": "预算占比",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "actual_budget / total_budget"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "execution_detail_cost",
        "nameCn": "执行细项费用",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / execution_detail_cnt"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.plan",
        "nameEn": "phase_budget_ratio",
        "nameCn": "分阶段预算占比",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "phase_budget / total_budget"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "ctr",
        "nameCn": "点击率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "click / impression"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.ad_default",
        "nameEn": "kol_price",
        "nameCn": "达人报价",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / kol_cnt"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "cpc",
        "nameCn": "点击成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / click"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "cpax",
        "nameCn": "行动成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / action_button_click"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "cpuv",
        "nameCn": "访问成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / read_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "invoke_app_open_cost",
        "nameCn": "APP打开成本（唤起）",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / invoke_app_open_cnt"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "cpm",
        "nameCn": "平均千次展示消费",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / impression * 1000"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "avg_view_time",
        "nameCn": "平均浏览时长(秒)",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "sum(view_time) / count(user_id)"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "video_play_5s_rate",
        "nameCn": "5s完播率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "video_play_5s_cnt / impression"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "pic_read_3s_rate",
        "nameCn": "3s阅读率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "read_3s_cnt / impression"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "cpe",
        "nameCn": "平均互动成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / interaction"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "cpti",
        "nameCn": "深度种草成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / ti_user_num"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "finish_rate",
        "nameCn": "视频完播率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "finish_cnt / impression"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "conversion_rate",
        "nameCn": "转化率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "shop_order_uv / enter_shop_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "cost_per_conversion",
        "nameCn": "成交成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / shop_order_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "invoke_app_payment_cost",
        "nameCn": "APP订单支付成本（唤起）",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / invoke_app_payment_cnt"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "first_app_pay_cost",
        "nameCn": "首次付费成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / first_app_pay_cnt"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ap",
        "nameEn": "app_activate_cost",
        "nameCn": "激活成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / app_activate_cnt"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_goods_order_price_30",
        "nameCn": "行业商品成交订单成本（30日）",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / external_goods_order_30"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_goods_order_price_15",
        "nameCn": "行业商品成交订单成本（15日）",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / external_goods_order_15"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "action_button_ctr",
        "nameCn": "行动按钮点击转化率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "conversion_cnt / click"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "roi",
        "nameCn": "投资回报率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "gmv / fee"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "average_order_value",
        "nameCn": "客单价",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "shop_order_gmv / shop_order_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.sd",
        "nameEn": "external_goods_order_price_7",
        "nameCn": "行业商品成交订单成本（7日）",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / external_goods_order_7"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.comp",
        "nameEn": "search_cmt_click_cvr",
        "nameCn": "搜索组件点击转化率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "search_cmt_click / impression"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "ad.fee",
        "nameEn": "total_platform_price",
        "nameCn": "平台服务费",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / total_platform_cnt"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "search_revisit_rate",
        "nameCn": "回搜率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "search_revisit_user / read_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "customer_acquisition_rate",
        "nameCn": "拉客率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "shop_new_customer_uv / enter_shop_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "new_visitor_rate",
        "nameCn": "新访客率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "shop_new_visitor_uv / enter_shop_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "cac",
        "nameCn": "新客成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / shop_new_customer_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "new_visitor_cost",
        "nameCn": "新访客成本",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "fee / shop_new_visitor_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "enter_shop_rate",
        "nameCn": "进店率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "enter_shop_uv / click"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.ps",
        "nameEn": "ad_cpuv",
        "nameCn": "投流 CPUV",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "ad_fee / ad_enter_shop_uv"
    },
    {
        "layer": "DWS",
        "category": "小红书广告投放(xhs_ad)",
        "process": "effect.effect_default",
        "nameEn": "roas",
        "nameCn": "广告支出回报率",
        "calcMode": "DERIVATIVE_COMPOSITE",
        "formula": "gmv / ad_fee"
    }
]
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = METRICS;
}
