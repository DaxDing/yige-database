/**
 * 小红书投流数据仓库 - 标准代码
 * 数据来源: DataWorks
 */

const STANDARD_CODES = {
    version: "1.0",
    updateDate: "2026年1月",
    codes: [
    {
        "category": "业务枚举值",
        "code": "evaluation_metrics",
        "nameCn": "评估指标",
        "nameEn": "evaluation_metrics",
        "desc": "属于业务字段，主要用于业务分析",
        "values": [
            {
                "value": "4",
                "nameCn": "剩余期望达成值",
                "nameEn": "remaining_target"
            },
            {
                "value": "3",
                "nameCn": "达成情况",
                "nameEn": "achievement_status"
            },
            {
                "value": "2",
                "nameCn": "偏差值",
                "nameEn": "deviation_value"
            },
            {
                "value": "1",
                "nameCn": "预估值",
                "nameEn": "estimated_value"
            },
            {
                "value": "0",
                "nameCn": "实际值",
                "nameEn": "actual_value"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "account_type",
        "nameCn": "资金类型",
        "nameEn": "account_type",
        "desc": "",
        "values": [
            {
                "value": "6",
                "nameCn": "赔付返货",
                "nameEn": "compensation_rebate"
            },
            {
                "value": "2",
                "nameCn": "授信",
                "nameEn": "credit"
            },
            {
                "value": "1",
                "nameCn": "常规返货",
                "nameEn": "regular_rebate"
            },
            {
                "value": "0",
                "nameCn": "现金",
                "nameEn": "cash"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "operate_type",
        "nameCn": "消费类型",
        "nameEn": "operate_type",
        "desc": "",
        "values": [
            {
                "value": "18",
                "nameCn": "订单完结释放余额",
                "nameEn": "order_complete_release"
            },
            {
                "value": "17",
                "nameCn": "取消订单",
                "nameEn": "order_cancel"
            },
            {
                "value": "16",
                "nameCn": "下单冻结",
                "nameEn": "order_freeze"
            },
            {
                "value": "15",
                "nameCn": "电商货款充值",
                "nameEn": "ecommerce_payment_recharge"
            },
            {
                "value": "14",
                "nameCn": "出款",
                "nameEn": "debit"
            },
            {
                "value": "13",
                "nameCn": "入账",
                "nameEn": "credit"
            },
            {
                "value": "12",
                "nameCn": "打款失败",
                "nameEn": "payment_failure"
            },
            {
                "value": "11",
                "nameCn": "打款成功",
                "nameEn": "payment_success"
            },
            {
                "value": "10",
                "nameCn": "返货追回",
                "nameEn": "return_recovery"
            },
            {
                "value": "9",
                "nameCn": "回收",
                "nameEn": "recycle"
            },
            {
                "value": "8",
                "nameCn": "提现",
                "nameEn": "withdrawal"
            },
            {
                "value": "7",
                "nameCn": "退款",
                "nameEn": "refund"
            },
            {
                "value": "6",
                "nameCn": "转账",
                "nameEn": "transfer"
            },
            {
                "value": "5",
                "nameCn": "虚拟充值",
                "nameEn": "virtual_recharge"
            },
            {
                "value": "4",
                "nameCn": "资金补扣",
                "nameEn": "fund_additional_deduction"
            },
            {
                "value": "3",
                "nameCn": "消费扣款",
                "nameEn": "consumption_deduction"
            },
            {
                "value": "2",
                "nameCn": "返现",
                "nameEn": "cashback"
            },
            {
                "value": "1",
                "nameCn": "现金充值",
                "nameEn": "cash_recharge"
            }
        ]
    },
    {
        "category": "业务枚举值",
        "code": "delivery_period",
        "nameCn": "投放节奏",
        "nameEn": "delivery_period",
        "desc": "",
        "values": [
            {
                "value": "5",
                "nameCn": "延续期",
                "nameEn": "continuation_phase"
            },
            {
                "value": "4",
                "nameCn": "爆发期",
                "nameEn": "burst_phase"
            },
            {
                "value": "3",
                "nameCn": "预热期",
                "nameEn": "warm_up_phase"
            },
            {
                "value": "2",
                "nameCn": "蓄水期",
                "nameEn": "accumulation_phase"
            },
            {
                "value": "1",
                "nameCn": "测试期",
                "nameEn": "testing_phase"
            }
        ]
    },
    {
        "category": "业务枚举值",
        "code": "statistic_type",
        "nameCn": "统计类型",
        "nameEn": "statistic_type",
        "desc": "",
        "values": [
            {
                "value": "2",
                "nameCn": "广告投流",
                "nameEn": "paid_traffic"
            },
            {
                "value": "1",
                "nameCn": "自然流",
                "nameEn": "organic_traffic"
            },
            {
                "value": "0",
                "nameCn": "全站",
                "nameEn": "site_wide"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "task_auth_status",
        "nameCn": "授权状态",
        "nameEn": "task_auth_status",
        "desc": "",
        "values": [
            {
                "value": "4",
                "nameCn": "已取消授权",
                "nameEn": "authorization_cancelled"
            },
            {
                "value": "3",
                "nameCn": "已拒绝",
                "nameEn": "rejected"
            },
            {
                "value": "2",
                "nameCn": "已自动授权",
                "nameEn": "auto_authorized"
            },
            {
                "value": "1",
                "nameCn": "已授权",
                "nameEn": "authorized"
            },
            {
                "value": "0",
                "nameCn": "待接受",
                "nameEn": "pending"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "attribution_period",
        "nameCn": "归因口径",
        "nameEn": "attribution_period",
        "desc": "当天有发生站外行为且归因时间内有看过笔记",
        "values": [
            {
                "value": "30",
                "nameCn": "30天口径窗口",
                "nameEn": "attribution_window_30_days"
            },
            {
                "value": "15",
                "nameCn": "15天口径窗口",
                "nameEn": "attribution_window_15_days"
            }
        ]
    },
    {
        "category": "业务枚举值",
        "code": "grass_alliance",
        "nameCn": "种草联盟",
        "nameEn": "grass_alliance",
        "desc": "",
        "values": [
            {
                "value": "99",
                "nameCn": "其他渠道",
                "nameEn": "other"
            },
            {
                "value": "3",
                "nameCn": "唯品会",
                "nameEn": "vip"
            },
            {
                "value": "2",
                "nameCn": "京东",
                "nameEn": "jd"
            },
            {
                "value": "1",
                "nameCn": "淘宝",
                "nameEn": "taobao"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "intelligent_expansion",
        "nameCn": "智能扩量",
        "nameEn": "intelligent_expansion",
        "desc": "",
        "values": [
            {
                "value": "1",
                "nameCn": "开启",
                "nameEn": "on"
            },
            {
                "value": "0",
                "nameCn": "关闭",
                "nameEn": "off"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "target_type",
        "nameCn": "定向类型",
        "nameEn": "target_type",
        "desc": "",
        "values": [
            {
                "value": "3",
                "nameCn": "高级定向",
                "nameEn": "advanced_targeting"
            },
            {
                "value": "2",
                "nameCn": "智能定向",
                "nameEn": "smart_targeting"
            },
            {
                "value": "1",
                "nameCn": "通投",
                "nameEn": "broad_targeting"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "search_target_city_intent",
        "nameCn": "搜索意图城市定向",
        "nameEn": "search_target_city_intent",
        "desc": "",
        "values": [
            {
                "value": "2",
                "nameCn": "所有用户",
                "nameEn": "all_users"
            },
            {
                "value": "1",
                "nameCn": "居住或意图在该地区的用户",
                "nameEn": "users_living_or_interested_in_region"
            },
            {
                "value": "0",
                "nameCn": "居住在该地区内的用户",
                "nameEn": "users_living_in_region"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "target_gender",
        "nameCn": "性别定向",
        "nameEn": "target_gender",
        "desc": "",
        "values": [
            {
                "value": "all",
                "nameCn": "全部",
                "nameEn": "all"
            },
            {
                "value": "1",
                "nameCn": "女",
                "nameEn": "female"
            },
            {
                "value": "0",
                "nameCn": "男",
                "nameEn": "male"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "target_age",
        "nameCn": "年龄定向",
        "nameEn": "target_age",
        "desc": "",
        "values": [
            {
                "value": "all",
                "nameCn": "全部",
                "nameEn": "all"
            },
            {
                "value": "51-100",
                "nameCn": ">50",
                "nameEn": "age_above_50"
            },
            {
                "value": "41-50",
                "nameCn": "41-50",
                "nameEn": "age_41_50"
            },
            {
                "value": "33-40",
                "nameCn": "33-40",
                "nameEn": "age_33_40"
            },
            {
                "value": "28-32",
                "nameCn": "28-32",
                "nameEn": "age_28_32"
            },
            {
                "value": "23-27",
                "nameCn": "23-27",
                "nameEn": "age_23_27"
            },
            {
                "value": "18-22",
                "nameCn": "18-22",
                "nameEn": "age_18_22"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "target_device",
        "nameCn": "设备定向",
        "nameEn": "target_device",
        "desc": "",
        "values": [
            {
                "value": "unknown",
                "nameCn": "未知",
                "nameEn": "unknown"
            },
            {
                "value": "all",
                "nameCn": "全部设备",
                "nameEn": "all"
            },
            {
                "value": "ios",
                "nameCn": "iOS",
                "nameEn": "ios"
            },
            {
                "value": "android",
                "nameCn": "Android",
                "nameEn": "android"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "target_device_price",
        "nameCn": "手机价格",
        "nameEn": "target_device_price",
        "desc": "",
        "values": [
            {
                "value": "7000-9999",
                "nameCn": "7000-9999元",
                "nameEn": "range_7000_9999"
            },
            {
                "value": "5000-6999",
                "nameCn": "5000-6999元",
                "nameEn": "range_5000_6999"
            },
            {
                "value": "4000-4999",
                "nameCn": "4000-4999元",
                "nameEn": "range_4000_4999"
            },
            {
                "value": "3000-3999",
                "nameCn": "3000-3999元",
                "nameEn": "range_3000_3999"
            },
            {
                "value": "2000-2999",
                "nameCn": "2000-2999元",
                "nameEn": "range_2000_2999"
            },
            {
                "value": "0-1999",
                "nameCn": "1999元以下",
                "nameEn": "below_1999"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "note_source",
        "nameCn": "笔记来源",
        "nameEn": "note_source",
        "desc": "",
        "values": [
            {
                "value": "13",
                "nameCn": "合作码笔记",
                "nameEn": "cooperation_code_note"
            },
            {
                "value": "12",
                "nameCn": "素材笔记",
                "nameEn": "material_note"
            },
            {
                "value": "11",
                "nameCn": "授权笔记",
                "nameEn": "authorized_note"
            },
            {
                "value": "6",
                "nameCn": "员工笔记",
                "nameEn": "employee_note"
            },
            {
                "value": "4",
                "nameCn": "主理人笔记",
                "nameEn": "curator_note"
            },
            {
                "value": "2",
                "nameCn": "合作笔记",
                "nameEn": "cooperation_note"
            },
            {
                "value": "1",
                "nameCn": "我的笔记",
                "nameEn": "my_note"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "note_status",
        "nameCn": "笔记状态",
        "nameEn": "note_status",
        "desc": "",
        "values": [
            {
                "value": "37",
                "nameCn": "高展拒绝",
                "nameEn": "high_exposure_rejected"
            },
            {
                "value": "20",
                "nameCn": "笔记需要强绑spu",
                "nameEn": "note_requires_spu_binding"
            },
            {
                "value": "15",
                "nameCn": "反作弊处罚等级",
                "nameEn": "anti_fraud_penalty_level"
            },
            {
                "value": "11",
                "nameCn": "抽奖笔记",
                "nameEn": "lottery_note"
            },
            {
                "value": "10",
                "nameCn": "设置隐私",
                "nameEn": "privacy_set"
            },
            {
                "value": "9",
                "nameCn": "淘宝笔记",
                "nameEn": "taobao_note"
            },
            {
                "value": "8",
                "nameCn": "私信笔记",
                "nameEn": "private_message_note"
            },
            {
                "value": "6",
                "nameCn": "反作弊处罚等级三",
                "nameEn": "anti_fraud_penalty_level_3"
            },
            {
                "value": "5",
                "nameCn": "反作弊处罚等级二",
                "nameEn": "anti_fraud_penalty_level_2"
            },
            {
                "value": "4",
                "nameCn": "反作弊处罚等级一",
                "nameEn": "anti_fraud_penalty_level_1"
            },
            {
                "value": "3",
                "nameCn": "已删除",
                "nameEn": "deleted"
            },
            {
                "value": "2",
                "nameCn": "非法",
                "nameEn": "illegal"
            },
            {
                "value": "1",
                "nameCn": "不匹配",
                "nameEn": "mismatch"
            },
            {
                "value": "0",
                "nameCn": "正常",
                "nameEn": "normal"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "note_type",
        "nameCn": "笔记类型",
        "nameEn": "note_type",
        "desc": "",
        "values": [
            {
                "value": "2",
                "nameCn": "视频",
                "nameEn": "video"
            },
            {
                "value": "1",
                "nameCn": "图文",
                "nameEn": "image_text"
            },
            {
                "value": "0",
                "nameCn": "全部",
                "nameEn": "all"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "placement",
        "nameCn": "投放位置",
        "nameEn": "placement",
        "desc": "别名：广告类型",
        "values": [
            {
                "value": "99",
                "nameCn": "达人推广",
                "nameEn": "kol_promotion"
            },
            {
                "value": "7",
                "nameCn": "视频内流",
                "nameEn": "in_video_stream"
            },
            {
                "value": "4",
                "nameCn": "全站智投",
                "nameEn": "smart_site_wide_promotion"
            },
            {
                "value": "3",
                "nameCn": "开屏推广",
                "nameEn": "splash_screen_promotion"
            },
            {
                "value": "2",
                "nameCn": "搜索推广",
                "nameEn": "search_promotion"
            },
            {
                "value": "1",
                "nameCn": "信息流推广",
                "nameEn": "feed_promotion"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "marketing_target",
        "nameCn": "营销目标",
        "nameEn": "marketing_target",
        "desc": "",
        "values": [
            {
                "value": "23",
                "nameCn": "引流电商-种草直达",
                "nameEn": "ecommerce_traffic_seeding_direct"
            },
            {
                "value": "21",
                "nameCn": "应用推广-小程序推广",
                "nameEn": "app_promotion_mini_program"
            },
            {
                "value": "20",
                "nameCn": "应用下载",
                "nameEn": "app_download"
            },
            {
                "value": "17",
                "nameCn": "外溢种草",
                "nameEn": "spillover_seeding"
            },
            {
                "value": "16",
                "nameCn": "应用推广_应用唤起",
                "nameEn": "app_promotion_deep_link"
            },
            {
                "value": "15",
                "nameCn": "商品推广_店铺拉新",
                "nameEn": "product_promotion_store_acquisition"
            },
            {
                "value": "14",
                "nameCn": "直播推广_直播预告",
                "nameEn": "live_stream_promotion_preview"
            },
            {
                "value": "13",
                "nameCn": "种草直达",
                "nameEn": "seeding_direct"
            },
            {
                "value": "10",
                "nameCn": "抢占赛道",
                "nameEn": "category_domination"
            },
            {
                "value": "9",
                "nameCn": "客资收集",
                "nameEn": "lead_generation"
            },
            {
                "value": "8",
                "nameCn": "直播推广_日常推广",
                "nameEn": "live_stream_promotion_daily"
            },
            {
                "value": "4",
                "nameCn": "产品种草",
                "nameEn": "product_seeding"
            },
            {
                "value": "3",
                "nameCn": "商品推广_日常推广",
                "nameEn": "product_promotion_daily"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "promotion_target",
        "nameCn": "标的类型",
        "nameEn": "promotion_target",
        "desc": "",
        "values": [
            {
                "value": "19",
                "nameCn": "不限（同投直播间和笔记）",
                "nameEn": "unlimited"
            },
            {
                "value": "18",
                "nameCn": "直播间",
                "nameEn": "live_stream"
            },
            {
                "value": "9",
                "nameCn": "落地页",
                "nameEn": "landing_page"
            },
            {
                "value": "7",
                "nameCn": "外链落地页",
                "nameEn": "external_landing_page"
            },
            {
                "value": "2",
                "nameCn": "商品",
                "nameEn": "product"
            },
            {
                "value": "1",
                "nameCn": "笔记",
                "nameEn": "note"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "bidding_strategy",
        "nameCn": "竞价策略",
        "nameEn": "bidding_strategy",
        "desc": "有时候称“delivery_mode”",
        "values": [
            {
                "value": "101",
                "nameCn": "自动出价（新版）",
                "nameEn": "auto_bidding_new"
            },
            {
                "value": "7",
                "nameCn": "OCPX",
                "nameEn": "ocpx"
            },
            {
                "value": "4",
                "nameCn": "MCB",
                "nameEn": "mcb"
            },
            {
                "value": "3",
                "nameCn": "自动出价",
                "nameEn": "auto_bidding"
            },
            {
                "value": "2",
                "nameCn": "手动出价",
                "nameEn": "manual_bidding"
            }
        ]
    },
    {
        "category": "小红书枚举值",
        "code": "optimize_target",
        "nameCn": "优化目标",
        "nameEn": "optimize_target",
        "desc": "",
        "values": [
            {
                "value": "64",
                "nameCn": "APP付费",
                "nameEn": "app_purchases"
            },
            {
                "value": "63",
                "nameCn": "APP关键行为",
                "nameEn": "app_key_actions"
            },
            {
                "value": "62",
                "nameCn": "APP注册",
                "nameEn": "app_registrations"
            },
            {
                "value": "61",
                "nameCn": "APP激活",
                "nameEn": "app_activations"
            },
            {
                "value": "60",
                "nameCn": "APP下载按钮点击量",
                "nameEn": "app_download_button_clicks"
            },
            {
                "value": "50",
                "nameCn": "私信留资量",
                "nameEn": "dm_lead_generation"
            },
            {
                "value": "43",
                "nameCn": "APP打开按钮点击量",
                "nameEn": "app_open_button_clicks"
            },
            {
                "value": "42",
                "nameCn": "直播预约量",
                "nameEn": "live_stream_reservations"
            },
            {
                "value": "41",
                "nameCn": "商品1日下单ROI",
                "nameEn": "product_1day_order_roi"
            },
            {
                "value": "38",
                "nameCn": "APP成交-订单数（唤起）",
                "nameEn": "app_orders_deep_link"
            },
            {
                "value": "37",
                "nameCn": "APP互动（唤起）",
                "nameEn": "app_engagements_deep_link"
            },
            {
                "value": "36",
                "nameCn": "APP进店（唤起）",
                "nameEn": "app_store_visits_deep_link"
            },
            {
                "value": "35",
                "nameCn": "APP打开（唤起）",
                "nameEn": "app_opens_deep_link"
            },
            {
                "value": "34",
                "nameCn": "企微开口量",
                "nameEn": "wechat_work_initiations"
            },
            {
                "value": "33",
                "nameCn": "成功添加企微量",
                "nameEn": "wechat_work_successful_adds"
            },
            {
                "value": "32",
                "nameCn": "添加企微量",
                "nameEn": "wechat_work_add_requests"
            },
            {
                "value": "31",
                "nameCn": "深度种草人群规模",
                "nameEn": "deep_seeding_audience_size"
            },
            {
                "value": "30",
                "nameCn": "种草人群规模",
                "nameEn": "seeding_audience_size"
            },
            {
                "value": "29",
                "nameCn": "APP支付",
                "nameEn": "app_payments"
            },
            {
                "value": "28",
                "nameCn": "APP互动",
                "nameEn": "app_engagements"
            },
            {
                "value": "27",
                "nameCn": "APP进店",
                "nameEn": "app_store_visits"
            },
            {
                "value": "26",
                "nameCn": "APP打开",
                "nameEn": "app_opens"
            },
            {
                "value": "25",
                "nameCn": "直播间支付ROI",
                "nameEn": "live_stream_payment_roi"
            },
            {
                "value": "24",
                "nameCn": "直播间支付订单量",
                "nameEn": "live_stream_payment_orders"
            },
            {
                "value": "23",
                "nameCn": "预告笔记点击量",
                "nameEn": "preview_post_clicks"
            },
            {
                "value": "21",
                "nameCn": "行业商品成单",
                "nameEn": "industry_product_orders"
            },
            {
                "value": "20",
                "nameCn": "TI人群规模",
                "nameEn": "target_interest_audience_size"
            },
            {
                "value": "19",
                "nameCn": "行业商品访问",
                "nameEn": "industry_product_views"
            },
            {
                "value": "18",
                "nameCn": "站外转化量",
                "nameEn": "offsite_conversions"
            },
            {
                "value": "17",
                "nameCn": "商品7日下单ROI",
                "nameEn": "product_7day_order_roi"
            },
            {
                "value": "16",
                "nameCn": "种草值",
                "nameEn": "seeding_value"
            },
            {
                "value": "15",
                "nameCn": "消费意向量",
                "nameEn": "purchase_intent"
            },
            {
                "value": "14",
                "nameCn": "直播间有效观看量",
                "nameEn": "live_stream_effective_views"
            },
            {
                "value": "13",
                "nameCn": "私信开口量",
                "nameEn": "dm_initiations"
            },
            {
                "value": "12",
                "nameCn": "落地页访问量",
                "nameEn": "landing_page_views"
            },
            {
                "value": "11",
                "nameCn": "商品访客量",
                "nameEn": "product_visitors"
            },
            {
                "value": "6",
                "nameCn": "观看量",
                "nameEn": "views"
            },
            {
                "value": "5",
                "nameCn": "私信咨询量",
                "nameEn": "direct_message_inquiries"
            },
            {
                "value": "4",
                "nameCn": "商品下单量",
                "nameEn": "product_orders"
            },
            {
                "value": "3",
                "nameCn": "表单提交量",
                "nameEn": "form_submissions"
            },
            {
                "value": "1",
                "nameCn": "互动量",
                "nameEn": "engagements"
            }
        ]
    }
]
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = STANDARD_CODES;
}
