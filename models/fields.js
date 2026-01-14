/**
 * 小红书投流数据仓库 - 字段标准
 * 数据来源: DataWorks
 */

const FIELD_STANDARDS = {
    version: "1.0",
    updateDate: "2026年1月",
    fields: [
    {
        "category": "维度字段.达人维度",
        "code": "72",
        "nameEn": "kol_url",
        "nameCn": "达人链接",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.产品维度",
        "code": "13",
        "nameEn": "industry_category",
        "nameCn": "行业类目",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.产品维度",
        "code": "17",
        "nameEn": "e_commerce_categories",
        "nameCn": "电商品类",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.产品维度",
        "code": "99",
        "nameEn": "delivery_product",
        "nameCn": "投放产品",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "69",
        "nameEn": "product_selling_points",
        "nameCn": "属性买点",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "11",
        "nameEn": "optimize_target",
        "nameCn": "优化目标",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "10",
        "nameEn": "bidding_strategy",
        "nameCn": "竞价策略",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "8",
        "nameEn": "marketing_target",
        "nameCn": "营销目标",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "7",
        "nameEn": "placement",
        "nameCn": "投放位置",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "30",
        "nameEn": "target_city",
        "nameCn": "城市定向",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "45",
        "nameEn": "delivery_period",
        "nameCn": "投放节奏",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "68",
        "nameEn": "delivery_strategy",
        "nameCn": "投放策略",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.活动策略",
        "code": "94",
        "nameEn": "delivery_days",
        "nameCn": "投放天数",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "29",
        "nameEn": "industry_interest_target",
        "nameCn": "行业兴趣",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "28",
        "nameEn": "crowd_target",
        "nameCn": "人群包",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "27",
        "nameEn": "keywords",
        "nameCn": "关键词定向",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "26",
        "nameEn": "interest_keywords",
        "nameCn": "关键词兴趣定向",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "23",
        "nameEn": "search_target_city_intent",
        "nameCn": "搜索意图城市定向",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "21",
        "nameEn": "target_device_price",
        "nameCn": "手机价格",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "22",
        "nameEn": "reverse_target_crowd",
        "nameCn": "排除特定人群",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "19",
        "nameEn": "target_age",
        "nameCn": "年龄定向",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "18",
        "nameEn": "target_gender",
        "nameCn": "性别定向",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度.定向指标",
        "code": "20",
        "nameEn": "target_device",
        "nameCn": "设备定向",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "1",
        "nameEn": "budget",
        "nameCn": "预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "164",
        "nameEn": "reserve_pv",
        "nameCn": "预告组件点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "220",
        "nameEn": "engage_comp_impression",
        "nameCn": "互动组件展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "221",
        "nameEn": "engage_comp_click",
        "nameCn": "互动组件点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "公共字段",
        "code": "93",
        "nameEn": "remarks",
        "nameCn": "备注说明",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "241",
        "nameEn": "app_register_cnt",
        "nameCn": "注册数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "240",
        "nameEn": "first_app_pay_cnt",
        "nameCn": "首次付费数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "239",
        "nameEn": "current_app_pay_cnt",
        "nameCn": "当日付费次数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "238",
        "nameEn": "app_key_action_cnt",
        "nameCn": "关键行为数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "237",
        "nameEn": "app_pay_cnt_7d",
        "nameCn": "7日付费次数",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "236",
        "nameEn": "app_pay_amount",
        "nameCn": "付费金额",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "235",
        "nameEn": "app_activate_amount_1d",
        "nameCn": "当日LTV",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "234",
        "nameEn": "app_activate_amount_3d",
        "nameCn": "三日LTV",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "233",
        "nameEn": "app_activate_amount_7d",
        "nameCn": "七日LTV",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "232",
        "nameEn": "retention_1d_cnt",
        "nameCn": "次留",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "231",
        "nameEn": "retention_3d_cnt",
        "nameCn": "3日留存",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "230",
        "nameEn": "retention_7d_cnt",
        "nameCn": "7日留存",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "229",
        "nameEn": "app_activate_cnt",
        "nameCn": "激活数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "228",
        "nameEn": "order_amount",
        "nameCn": "订单流水",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "227",
        "nameEn": "fee",
        "nameCn": "消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "226",
        "nameEn": "roi",
        "nameCn": "投资回报率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "228",
        "nameEn": "roas",
        "nameCn": "广告支出回报率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "225",
        "nameEn": "gmv",
        "nameCn": "商品交易总额",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "224",
        "nameEn": "cpe",
        "nameCn": "平均互动成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "223",
        "nameEn": "cpm",
        "nameCn": "平均千次展示消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "222",
        "nameEn": "cpi",
        "nameCn": "互动单价",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "219",
        "nameEn": "content_comp_click",
        "nameCn": "内容组件点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "218",
        "nameEn": "content_comp_impression",
        "nameCn": "内容组件展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "217",
        "nameEn": "comp_click",
        "nameCn": "组件点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "216",
        "nameEn": "comp_impression",
        "nameCn": "组件展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "215",
        "nameEn": "ad_cpuv",
        "nameCn": "投流 CPUV",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "214",
        "nameEn": "cash_amount",
        "nameCn": "现金消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "213",
        "nameEn": "organic_shop_uv",
        "nameCn": "自然进店UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "212",
        "nameEn": "daily_organic_shop_uv",
        "nameCn": "日均自然进店UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "211",
        "nameEn": "total_platform_price",
        "nameCn": "平台服务费",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "210",
        "nameEn": "kol_price",
        "nameCn": "达人报价",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "209",
        "nameEn": "ad_enter_shop_uv",
        "nameCn": "投流进店UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "208",
        "nameEn": "ad_interaction",
        "nameCn": "投流互动量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "207",
        "nameEn": "ad_click",
        "nameCn": "投流点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "206",
        "nameEn": "ad_impression",
        "nameCn": "投流展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "205",
        "nameEn": "ad_fee",
        "nameCn": "投流消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "204",
        "nameEn": "kols_fee",
        "nameCn": "蒲公英消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "203",
        "nameEn": "jd_ad_fee",
        "nameCn": "小红盟投流消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "202",
        "nameEn": "tb_ad_fee",
        "nameCn": "小红星投流消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "201",
        "nameEn": "jd_fee",
        "nameCn": "小红盟消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "200",
        "nameEn": "tb_fee",
        "nameCn": "小红星消费",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "199",
        "nameEn": "total_budget",
        "nameCn": "总预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "198",
        "nameEn": "budget_ratio",
        "nameCn": "预算占比",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "197",
        "nameEn": "video_count_budget",
        "nameCn": "视频数量预估",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "196",
        "nameEn": "image_text_count_budget",
        "nameCn": "图文数量预估",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "195",
        "nameEn": "kol_budget",
        "nameCn": "达人预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.业务指标",
        "code": "194",
        "nameEn": "ad_budget",
        "nameCn": "投流预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "193",
        "nameEn": "planned_note_count",
        "nameCn": "笔记数量规划",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "192",
        "nameEn": "execution_detail_cost",
        "nameCn": "执行细项费用",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "191",
        "nameEn": "phase_budget",
        "nameCn": "分阶段预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "190",
        "nameEn": "phase_budget_ratio",
        "nameCn": "分阶段预算占比",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "189",
        "nameEn": "feed_budget",
        "nameCn": "信息流预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "188",
        "nameEn": "search_budget",
        "nameCn": "搜索流预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "187",
        "nameEn": "phase_total_budget",
        "nameCn": "阶段总预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "属性字段.配置属性",
        "code": "186",
        "nameEn": "optimization_goal",
        "nameCn": "重点优化目标",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.规划指标",
        "code": "185",
        "nameEn": "effective_budget",
        "nameCn": "有效预算",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "184",
        "nameEn": "read_uv",
        "nameCn": "阅读量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "183",
        "nameEn": "promotion_impression",
        "nameCn": "推广展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "182",
        "nameEn": "heat_read",
        "nameCn": "加热阅读量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "181",
        "nameEn": "discovery_impression",
        "nameCn": "发现页展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "180",
        "nameEn": "heat_impression",
        "nameCn": "加热展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "179",
        "nameEn": "follow_read",
        "nameCn": "关注阅读",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "178",
        "nameEn": "promotion_read",
        "nameCn": "推广阅读量",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "177",
        "nameEn": "search_impression",
        "nameCn": "搜索页展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "176",
        "nameEn": "search_read",
        "nameCn": "搜索阅读量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "175",
        "nameEn": "finish_rate",
        "nameCn": "视频完播率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "174",
        "nameEn": "avg_view_time",
        "nameCn": "平均浏览时长(秒)",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "173",
        "nameEn": "video_play_5s_rate",
        "nameCn": "5s完播率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "172",
        "nameEn": "video_play_5s_cnt",
        "nameCn": "5秒播放量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "171",
        "nameEn": "comment",
        "nameCn": "评论",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "170",
        "nameEn": "collect",
        "nameCn": "收藏",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "169",
        "nameEn": "follow",
        "nameCn": "关注",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "168",
        "nameEn": "share",
        "nameCn": "分享",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "167",
        "nameEn": "action_button_click",
        "nameCn": "行动按钮点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "166",
        "nameEn": "screenshot",
        "nameCn": "截图",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "165",
        "nameEn": "pic_save",
        "nameCn": "保存图片",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "163",
        "nameEn": "like",
        "nameCn": "点赞",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "162",
        "nameEn": "impression",
        "nameCn": "展现量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "161",
        "nameEn": "click",
        "nameCn": "点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "160",
        "nameEn": "ctr",
        "nameCn": "点击率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "159",
        "nameEn": "pic_read_3s_rate",
        "nameCn": "3s阅读率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "158",
        "nameEn": "feed_interest",
        "nameCn": "推荐场种草数",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "157",
        "nameEn": "cp",
        "nameCn": "消费意向",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "156",
        "nameEn": "other_interest",
        "nameCn": "其他场种草数",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "155",
        "nameEn": "search_interest",
        "nameCn": "搜索场种草数",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "154",
        "nameEn": "interest",
        "nameCn": "种草数",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "153",
        "nameEn": "search_cmt_after_read",
        "nameCn": "搜后阅读量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "152",
        "nameEn": "i_user_num",
        "nameCn": "新增种草人群",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "151",
        "nameEn": "ti_user_num",
        "nameCn": "新增深度种草人群",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "150",
        "nameEn": "search_cmt_click",
        "nameCn": "搜索组件点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "149",
        "nameEn": "search_revisit_rate",
        "nameCn": "回搜率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.互动指标",
        "code": "148",
        "nameEn": "interaction",
        "nameCn": "互动量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "147",
        "nameEn": "cpc",
        "nameCn": "点击成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "146",
        "nameEn": "action_button_ctr",
        "nameCn": "行动按钮点击转化率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "145",
        "nameEn": "search_cmt_click_cvr",
        "nameCn": "搜索组件点击转化率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "144",
        "nameEn": "cpti",
        "nameCn": "深度种草成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "143",
        "nameEn": "cpax",
        "nameCn": "行动成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "142",
        "nameEn": "cpuv",
        "nameCn": "访问成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "141",
        "nameEn": "cost_per_conversion",
        "nameCn": "成交成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "140",
        "nameEn": "average_order_value",
        "nameCn": "客单价",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "139",
        "nameEn": "enter_shop_rate",
        "nameCn": "进店率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "138",
        "nameEn": "conversion_rate",
        "nameCn": "转化率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "137",
        "nameEn": "new_visitor_cost",
        "nameCn": "新访客成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "136",
        "nameEn": "cac",
        "nameCn": "新客成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "135",
        "nameEn": "new_visitor_rate",
        "nameCn": "新访客率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "134",
        "nameEn": "customer_acquisition_rate",
        "nameCn": "拉客率",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "133",
        "nameEn": "shop_order_gmv",
        "nameCn": "成交GMV",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "132",
        "nameEn": "shop_order_uv",
        "nameCn": "成交UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "131",
        "nameEn": "add_cart_uv",
        "nameCn": "加购UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "130",
        "nameEn": "shop_new_visitor_uv",
        "nameCn": "新访客UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "129",
        "nameEn": "shop_new_customer_uv",
        "nameCn": "新客UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "128",
        "nameEn": "enter_shop_uv",
        "nameCn": "进店UV",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "127",
        "nameEn": "landing_page_visit",
        "nameCn": "落地页访问量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "126",
        "nameEn": "leads_button_impression",
        "nameCn": "表单按钮曝光量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "125",
        "nameEn": "message_user",
        "nameCn": "私信进线人数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "124",
        "nameEn": "message",
        "nameCn": "私信开口条数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "123",
        "nameEn": "message_consult",
        "nameCn": "私信进线数",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "122",
        "nameEn": "initiative_message",
        "nameCn": "私信开口数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "121",
        "nameEn": "msg_leads_num",
        "nameCn": "私信留资数",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "120",
        "nameEn": "leads",
        "nameCn": "表单提交",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "119",
        "nameEn": "invoke_app_enter_store_cnt",
        "nameCn": "APP进店量（唤起）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "118",
        "nameEn": "invoke_app_engagement_cnt",
        "nameCn": "APP互动量（唤起）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "117",
        "nameEn": "invoke_app_payment_cnt",
        "nameCn": "APP支付次数（唤起）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "116",
        "nameEn": "search_invoke_button_click_cnt",
        "nameCn": "APP打开按钮点击量（唤起）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "115",
        "nameEn": "invoke_app_payment_amount",
        "nameCn": "APP支付金额（唤起）",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "114",
        "nameEn": "invoke_app_open_cnt",
        "nameCn": "APP打开量（唤起）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "113",
        "nameEn": "invoke_app_payment_cost",
        "nameCn": "APP订单支付成本（唤起）",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "112",
        "nameEn": "invoke_app_open_cost",
        "nameCn": "APP打开成本（唤起）",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "111",
        "nameEn": "first_app_pay_cost",
        "nameCn": "首次付费成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "110",
        "nameEn": "app_activate_cost",
        "nameCn": "激活成本",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "109",
        "nameEn": "external_goods_order_7",
        "nameCn": "行业商品成交订单量（7日）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "108",
        "nameEn": "external_rgmv_7",
        "nameCn": "行业商品GMV（7日）",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "107",
        "nameEn": "external_goods_order_price_7",
        "nameCn": "行业商品成交订单成本（7日）",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "106",
        "nameEn": "external_goods_order_15",
        "nameCn": "行业商品成交订单量（15日）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "105",
        "nameEn": "external_rgmv_15",
        "nameCn": "行业商品GMV（15日）",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "104",
        "nameEn": "external_goods_order_price_15",
        "nameCn": "行业商品成交订单成本（15日）",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "103",
        "nameEn": "external_goods_order_30",
        "nameCn": "行业商品成交订单量（30日）",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "102",
        "nameEn": "external_rgmv_30",
        "nameCn": "行业商品GMV（30日）",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "指标字段.成本指标",
        "code": "101",
        "nameEn": "external_goods_order_price_30",
        "nameCn": "行业商品成交订单成本（30日）",
        "dataType": "DECIMAL",
        "definition": ""
    },
    {
        "category": "指标字段.转化指标",
        "code": "100",
        "nameEn": "external_goods_visit_7",
        "nameCn": "行业商品点击量",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度",
        "code": "98",
        "nameEn": "kol_type",
        "nameCn": "达人类型",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "指标字段.流量指标",
        "code": "97",
        "nameEn": "kol_tier",
        "nameCn": "达人量级",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.配置属性",
        "code": "96",
        "nameEn": "window_period",
        "nameCn": "窗口期",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "95",
        "nameEn": "delivery_date",
        "nameCn": "投放日期",
        "dataType": "DATE",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "92",
        "nameEn": "user_name",
        "nameCn": "用户名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "91",
        "nameEn": "brand_user_name",
        "nameCn": "品牌商名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "90",
        "nameEn": "virtual_seller_name",
        "nameCn": "子账户名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "89",
        "nameEn": "advertiser_name",
        "nameCn": "投放账号名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "88",
        "nameEn": "brand_qual_name",
        "nameCn": "品牌资质名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "87",
        "nameEn": "apply_name",
        "nameCn": "资质名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "86",
        "nameEn": "brand_name",
        "nameCn": "品牌名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "85",
        "nameEn": "spu_name",
        "nameCn": "SPU名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "84",
        "nameEn": "unit_name",
        "nameCn": "单元名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "83",
        "nameEn": "target_name",
        "nameCn": "定向名称",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "82",
        "nameEn": "creativity_name",
        "nameCn": "创意名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "81",
        "nameEn": "xhs_product_name",
        "nameCn": "跨域项目名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "80",
        "nameEn": "task_name",
        "nameCn": "任务组名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "79",
        "nameEn": "sub_task_name",
        "nameCn": "子任务名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "78",
        "nameEn": "project_name",
        "nameCn": "项目名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "77",
        "nameEn": "kol_name",
        "nameCn": "博主名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "76",
        "nameEn": "order_name",
        "nameCn": "订单名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.内容维度",
        "code": "75",
        "nameEn": "note_url",
        "nameCn": "笔记链接",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "74",
        "nameEn": "note_name",
        "nameCn": "笔记名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "73",
        "nameEn": "campaign_group_name",
        "nameCn": "广告组名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.配置属性",
        "code": "71",
        "nameEn": "group_name",
        "nameCn": "人群包名",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "70",
        "nameEn": "campaign_name",
        "nameCn": "计划名称",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "67",
        "nameEn": "advertiser_id",
        "nameCn": "投放账号ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "66",
        "nameEn": "apply_id",
        "nameCn": "资质ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "65",
        "nameEn": "brand_id",
        "nameCn": "品牌ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "64",
        "nameEn": "brand_qual_id",
        "nameCn": "品牌资质ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "63",
        "nameEn": "brand_user_id",
        "nameCn": "品牌商ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "62",
        "nameEn": "campaign_id",
        "nameCn": "计划ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "61",
        "nameEn": "note_id",
        "nameCn": "笔记ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "60",
        "nameEn": "creativity_id",
        "nameCn": "创意ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "59",
        "nameEn": "group_id",
        "nameCn": "人群包ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "58",
        "nameEn": "kol_id",
        "nameCn": "博主ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "57",
        "nameEn": "order_id",
        "nameCn": "订单ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "56",
        "nameEn": "xhs_product_id",
        "nameCn": "跨域项目ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "55",
        "nameEn": "project_id",
        "nameCn": "项目ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "54",
        "nameEn": "kol_red_id",
        "nameCn": "小红书ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "53",
        "nameEn": "spu_id",
        "nameCn": "SPU ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "52",
        "nameEn": "target_id",
        "nameCn": "定向ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "51",
        "nameEn": "task_id",
        "nameCn": "任务组ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "50",
        "nameEn": "unit_id",
        "nameCn": "单元ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "49",
        "nameEn": "user_id",
        "nameCn": "用户ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "48",
        "nameEn": "virtual_seller_id",
        "nameCn": "子账户ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "47",
        "nameEn": "campaign_group_id",
        "nameCn": "广告组ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "属性字段.标识属性",
        "code": "46",
        "nameEn": "sub_task_id",
        "nameCn": "子任务ID",
        "dataType": "BIGINT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度",
        "code": "44",
        "nameEn": "operate_type",
        "nameCn": "消费类型",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度",
        "code": "43",
        "nameEn": "account_type",
        "nameCn": "资金类型",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "属性字段.配置属性",
        "code": "42",
        "nameEn": "statistic_type",
        "nameCn": "统计类型",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "属性字段.配置属性",
        "code": "41",
        "nameEn": "evaluation_metrics",
        "nameCn": "评估指标",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.状态属性",
        "code": "40",
        "nameEn": "task_auth_status",
        "nameCn": "授权状态",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "39",
        "nameEn": "year",
        "nameCn": "年",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "38",
        "nameEn": "month",
        "nameCn": "月",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "37",
        "nameEn": "week",
        "nameCn": "周",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "36",
        "nameEn": "dt",
        "nameCn": "日期",
        "dataType": "DATE",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "35",
        "nameEn": "event_group_end_time",
        "nameCn": "联盟结束时间",
        "dataType": "DATETIME",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "34",
        "nameEn": "event_group_start_time",
        "nameCn": "联盟开始时间",
        "dataType": "DATETIME",
        "definition": ""
    },
    {
        "category": "维度字段.时间维度",
        "code": "33",
        "nameEn": "hh",
        "nameCn": "小时",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度",
        "code": "32",
        "nameEn": "grass_alliance",
        "nameCn": "种草联盟",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "属性字段.配置属性",
        "code": "31",
        "nameEn": "attribution_period",
        "nameCn": "归因口径",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度",
        "code": "25",
        "nameEn": "intelligent_expansion",
        "nameCn": "智能扩量",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度",
        "code": "24",
        "nameEn": "target_type",
        "nameCn": "定向类型",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "属性字段.状态属性",
        "code": "16",
        "nameEn": "note_status",
        "nameCn": "笔记状态",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.内容维度",
        "code": "15",
        "nameEn": "note_type",
        "nameCn": "笔记类型",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.内容维度",
        "code": "14",
        "nameEn": "note_source",
        "nameCn": "笔记来源",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.内容维度",
        "code": "12",
        "nameEn": "content_category",
        "nameCn": "内容类目",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "维度字段.投放维度",
        "code": "9",
        "nameEn": "promotion_target",
        "nameCn": "标的类型",
        "dataType": "INT",
        "definition": ""
    },
    {
        "category": "属性字段.配置属性",
        "code": "6",
        "nameEn": "kfs",
        "nameCn": "投放位置分配",
        "dataType": "STRING",
        "definition": ""
    },
    {
        "category": "维度字段.内容维度",
        "code": "5",
        "nameEn": "content_theme",
        "nameCn": "内容主题",
        "dataType": "STRING",
        "definition": ""
    }
]
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = FIELD_STANDARDS;
}
