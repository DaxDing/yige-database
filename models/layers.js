/**
 * 小红书投流数据仓库 - 数据定义
 *
 * 添加新表只需要在对应层级的 tables 数组中添加即可
 * 格式: { name: '表名', desc: '描述', tags: ['标签1', '标签2'] }
 */

const DATA_WAREHOUSE = {
    // 版本信息
    version: '2.0',
    updateDate: '2026年1月',

    // ODS 层通用字段定义
    odsFields: [
        { name: 'dt', nameCn: '数据时间段', type: 'STRING', desc: '数据统计的时间段范围', example: '2026-01-06 14:00 - 14:59' },
        { name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
        { name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
        { name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
    ],

    // ODS 层分组特有字段
    odsGroupFields: {
        '投流效果': [
            { name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876' }
        ],
        '转化效果': [
            { name: 'grass_alliance', nameCn: '种草联盟', type: 'STRING', desc: '种草联盟标识', example: 'starriver' }
        ],
        '其他数据': [
            { name: 'account_type', nameCn: '账户类型', type: 'STRING', desc: '投流账户类型', example: 'ad' },
            { name: 'operate_type', nameCn: '操作类型', type: 'STRING', desc: '流水操作类型', example: 'recharge' },
            { name: 'cash_amount', nameCn: '金额', type: 'DECIMAL', desc: '流水金额（元）', example: '1000.00' }
        ]
    },

    // ODS 层表字段定义（覆盖通用字段）
    odsTableFields: {
        // ========== 实时效果 ==========
        'ods_xhs_jg_creativity_realtime_hi': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '标识字段', name: 'creativity_id', nameCn: '创意ID', type: 'STRING', desc: '创意标识', example: '3437479586', key: 'PK' },
            { seq: 3, cat: '时间字段', name: 'dt', nameCn: '数据时间段', type: 'STRING', desc: '数据统计的时间段范围', example: '2026-01-13 14:00 - 14:59', key: 'PK' },
            { seq: 4, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 5, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-13 14:05:00' },
            { seq: 6, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260113', key: 'PT' }
        ],

        // ========== 种草效果 ==========
        'ods_xhs_post_note_report_di': [
            { seq: 1, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 2, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 3, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 4, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        // ========== 投流效果 ==========
        'ods_xhs_creative_report_hi': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据时间段', type: 'STRING', desc: '数据统计的时间段范围', example: '2026-01-06 14:00 - 14:59', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'ods_xhs_audience_report_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'ods_xhs_spu_report_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'ods_xhs_search_term_report_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'ods_xhs_keyword_report_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        // ========== 转化效果 ==========
        'ods_xhs_grass_ad_conversion_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'ods_xhs_grass_task_conversion_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'ods_xhs_grass_content_conversion_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 3, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 4, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 5, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        // ========== 项目规划 ==========
        'ods_xhs_budget_plan_df': [
            { seq: 1, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '预算日期', example: '2026-01-06', key: 'PK' },
            { seq: 2, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 3, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 4, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'ods_xhs_kpi_plan_df': [
            { seq: 1, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: 'KPI目标日期', example: '2026-01-06', key: 'PK' },
            { seq: 2, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 3, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 4, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        // ========== 其他数据 ==========
        'ods_xhs_account_flow_df': [
            { seq: 1, cat: '时间字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '流水数据日期', example: '2026-01-06', key: 'PK' },
            { seq: 2, cat: '原始数据', name: 'raw_data', nameCn: '原始数据', type: 'STRING', desc: 'API返回的原始JSON数据', example: '{"id":123,...}' },
            { seq: 3, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 4, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ]
    },

    // 各层通用尾部字段（etl_time + ds）
    commonTailFields: [
        { name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
        { name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
    ],

    // DWD 层字段定义（示例，具体字段根据表不同）
    dwdFields: [
        { name: 'dt', nameCn: '数据时间段', type: 'STRING', desc: '数据统计的时间段范围', example: '2026-01-06 14:00 - 14:59' },
        { name: '...', nameCn: '业务字段', type: '-', desc: '根据具体表定义', example: '-' }
    ],


    // DWD 层表字段定义
    dwdTableFields: {
        'dwd_xhs_creative_hourly_di': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '投放账号ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '标识字段', name: 'note_id', nameCn: '笔记ID', type: 'STRING', desc: '投放的笔记标识', example: '6789012345' },
            { seq: 3, cat: '标识字段', name: 'unit_id', nameCn: '单元ID', type: 'STRING', desc: '广告单元标识', example: '1234567890' },
            { seq: 4, cat: '标识字段', name: 'campaign_id', nameCn: '计划ID', type: 'STRING', desc: '广告计划标识', example: '9876543210' },
            { seq: 5, cat: '标识字段', name: 'creativity_id', nameCn: '创意ID', type: 'STRING', desc: '创意标识', example: '1122334455', key: 'PK' },
            { seq: 6, cat: '策略字段', name: 'placement', nameCn: '投放位置', type: 'INT', desc: '广告投放位置类型', example: '1' },
            { seq: 7, cat: '策略字段', name: 'marketing_target', nameCn: '营销目标', type: 'INT', desc: '营销目标类型编码', example: '2' },
            { seq: 8, cat: '策略字段', name: 'promotion_target', nameCn: '推广目标', type: 'INT', desc: '推广目标类型编码', example: '1' },
            { seq: 9, cat: '策略字段', name: 'optimize_target', nameCn: '优化目标', type: 'INT', desc: '出价优化目标类型', example: '3' },
            { seq: 10, cat: '策略字段', name: 'bidding_strategy', nameCn: '竞价策略', type: 'INT', desc: '竞价策略类型编码', example: '1' },
            { seq: 11, cat: '时间字段', name: 'dt', nameCn: '数据时间段', type: 'STRING', desc: '数据统计的时间段范围', example: '2026-01-06 14:00 - 14:59', key: 'PK' },
            { seq: 12, cat: '展现指标', name: 'fee', nameCn: '消费', type: 'DECIMAL', desc: '广告消费金额（元）', example: '1234.56' },
            { seq: 13, cat: '展现指标', name: 'impression', nameCn: '展现量', type: 'BIGINT', desc: '广告展现次数', example: '10000' },
            { seq: 14, cat: '展现指标', name: 'click', nameCn: '点击量', type: 'BIGINT', desc: '广告点击次数', example: '500' },
            { seq: 15, cat: '笔记指标', name: 'like', nameCn: '点赞', type: 'BIGINT', desc: '笔记点赞数', example: '200' },
            { seq: 16, cat: '笔记指标', name: 'comment', nameCn: '评论', type: 'BIGINT', desc: '笔记评论数', example: '50' },
            { seq: 17, cat: '笔记指标', name: 'collect', nameCn: '收藏', type: 'BIGINT', desc: '笔记收藏数', example: '100' },
            { seq: 18, cat: '笔记指标', name: 'follow', nameCn: '关注', type: 'BIGINT', desc: '笔记带来的关注数', example: '30' },
            { seq: 19, cat: '笔记指标', name: 'share', nameCn: '分享', type: 'BIGINT', desc: '笔记分享数', example: '20' },
            { seq: 20, cat: '笔记指标', name: 'interaction', nameCn: '互动量', type: 'BIGINT', desc: '笔记总互动量', example: '400' },
            { seq: 21, cat: '笔记指标', name: 'action_button_click', nameCn: '行动按钮点击量', type: 'BIGINT', desc: '组件点击量', example: '80' },
            { seq: 22, cat: '笔记指标', name: 'screenshot', nameCn: '截图', type: 'BIGINT', desc: '截图次数', example: '15' },
            { seq: 23, cat: '笔记指标', name: 'pic_save', nameCn: '保存图片', type: 'BIGINT', desc: '图片保存次数', example: '25' },
            { seq: 24, cat: '笔记指标', name: 'reserve_pv', nameCn: '预告组件点击', type: 'BIGINT', desc: '预告组件点击量', example: '10' },
            { seq: 25, cat: '视频指标', name: 'video_play_5s_cnt', nameCn: '5秒播放量', type: 'BIGINT', desc: '视频播放超过5秒的次数', example: '3000' },
            { seq: 26, cat: '转化指标', name: 'product_seeding_metrics', nameCn: '产品种草指标', type: 'JSON', desc: '产品种草转化指标', example: '{"search_cmt_click":120,...}' },
            { seq: 27, cat: '转化指标', name: 'lead_collection_metrics', nameCn: '客资收集指标', type: 'JSON', desc: '客资收集转化指标', example: '{"leads":30,...}' },
            { seq: 28, cat: '转化指标', name: 'app_promotion_metrics', nameCn: '应用推广指标', type: 'JSON', desc: '应用推广转化指标', example: '{"invoke_app_open_cnt":100,...}' },
            { seq: 29, cat: '转化指标', name: 'direct_seeding_metrics', nameCn: '种草直达指标', type: 'JSON', desc: '种草直达转化指标', example: '{"external_goods_visit_7":300,...}' },
            { seq: 30, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 31, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ],

        'dwd_xhs_creativity_realtime_hi': [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '投放账号ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '标识字段', name: 'creativity_id', nameCn: '创意ID', type: 'STRING', desc: '创意标识', example: '3437479586', key: 'PK' },
            { seq: 3, cat: '标识字段', name: 'campaign_id', nameCn: '计划ID', type: 'STRING', desc: '广告计划标识', example: '68230001' },
            { seq: 4, cat: '标识字段', name: 'unit_id', nameCn: '单元ID', type: 'STRING', desc: '广告单元标识', example: '68230002' },
            { seq: 5, cat: '标识字段', name: 'note_id', nameCn: '笔记ID', type: 'STRING', desc: '关联笔记标识', example: '67830d6c000000001d031e34' },
            { seq: 6, cat: '属性字段', name: 'campaign_name', nameCn: '计划名称', type: 'STRING', desc: '广告计划名称', example: '品牌推广计划A' },
            { seq: 7, cat: '属性字段', name: 'unit_name', nameCn: '单元名称', type: 'STRING', desc: '广告单元名称', example: '单元001' },
            { seq: 8, cat: '属性字段', name: 'creativity_name', nameCn: '创意名称', type: 'STRING', desc: '创意名称', example: '创意A' },
            { seq: 9, cat: '策略字段', name: 'marketing_target', nameCn: '营销诉求', type: 'STRING', desc: '营销目标类型', example: '3' },
            { seq: 10, cat: '策略字段', name: 'promote_target', nameCn: '推广标的', type: 'STRING', desc: '推广目标类型', example: '5' },
            { seq: 11, cat: '策略字段', name: 'placement', nameCn: '推广类型', type: 'STRING', desc: '广告投放类型', example: '1' },
            { seq: 12, cat: '策略字段', name: 'build_type', nameCn: '搭建方式', type: 'STRING', desc: '计划搭建方式', example: '1' },
            { seq: 13, cat: '策略字段', name: 'optimization_target', nameCn: '优化目标', type: 'STRING', desc: '投放优化目标', example: '1' },
            { seq: 14, cat: '时间字段', name: 'stat_date', nameCn: '统计日期', type: 'STRING', desc: '数据统计日期 YYYY-MM-DD', example: '2026-01-13', key: 'PK' },
            { seq: 15, cat: '时间字段', name: 'stat_hour', nameCn: '统计小时', type: 'STRING', desc: '数据统计小时 HH', example: '14', key: 'PK' },
            { seq: 16, cat: '展现指标', name: 'impression', nameCn: '曝光数', type: 'BIGINT', desc: '广告曝光次数', example: '10000' },
            { seq: 17, cat: '展现指标', name: 'click', nameCn: '点击数', type: 'BIGINT', desc: '广告点击次数', example: '500' },
            { seq: 18, cat: '展现指标', name: 'cost', nameCn: '消耗', type: 'DECIMAL(18,2)', desc: '广告消耗金额（元）', example: '1234.56' },
            { seq: 19, cat: '笔记指标', name: 'note_click', nameCn: '笔记点击', type: 'BIGINT', desc: '笔记点击次数', example: '800' },
            { seq: 20, cat: '笔记指标', name: 'note_like', nameCn: '笔记点赞', type: 'BIGINT', desc: '笔记点赞次数', example: '200' },
            { seq: 21, cat: '笔记指标', name: 'note_collect', nameCn: '笔记收藏', type: 'BIGINT', desc: '笔记收藏次数', example: '100' },
            { seq: 22, cat: '笔记指标', name: 'note_comment', nameCn: '笔记评论', type: 'BIGINT', desc: '笔记评论次数', example: '50' },
            { seq: 23, cat: '笔记指标', name: 'note_share', nameCn: '笔记分享', type: 'BIGINT', desc: '笔记分享次数', example: '30' },
            { seq: 24, cat: '笔记指标', name: 'note_follow', nameCn: '笔记关注', type: 'BIGINT', desc: '通过笔记关注次数', example: '20' },
            { seq: 25, cat: '产品种草', name: 'goods_click', nameCn: '商品点击', type: 'BIGINT', desc: '商品点击次数', example: '150' },
            { seq: 26, cat: '产品种草', name: 'order_cnt', nameCn: '订单数', type: 'BIGINT', desc: '订单数量', example: '10' },
            { seq: 27, cat: '产品种草', name: 'order_amt', nameCn: '订单金额', type: 'DECIMAL(18,2)', desc: '订单金额（元）', example: '2580.00' },
            { seq: 28, cat: '系统字段', name: 'dt', nameCn: '数据时间段', type: 'STRING', desc: '数据统计的时间段范围', example: '2026-01-13 14:00 - 14:59' },
            { seq: 29, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-13 15:30:00' },
            { seq: 30, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260113', key: 'PT' }
        ]
    },

    // DIM 层表字段定义（待定义）
    dimTableFields: {},

    // Bridge 层表字段定义（待定义）
    bridgeTableFields: {},

    // DWS 层表字段定义（待定义）
    dwsTableFields: {},

    // DIM 层字段定义
    dimFields: [
        { name: '{dim}_id', nameCn: '维度主键', type: 'STRING', desc: '维度表主键', example: '-', key: 'PK' },
        { name: '...', nameCn: '维度属性', type: '-', desc: '根据具体维度定义', example: '-' }
    ],

    // DWS 层字段定义
    dwsFields: [
        { name: 'stat_date', nameCn: '统计日期', type: 'STRING', desc: '汇总统计日期', example: '2026-01-06' },
        { name: '...', nameCn: '汇总指标', type: '-', desc: '根据具体表定义', example: '-' }
    ],

    layers: [
        {
            id: 'ods',
            name: 'ODS',
            fullName: '原始数据层',
            description: '存储从小红书聚光平台 API 同步的原始数据，保持数据原貌，不做任何业务处理。',
            groups: [
                {
                    name: '实时效果',
                    tables: [
                        { name: 'ods_xhs_jg_creativity_realtime_hi', desc: '创意层小时实时报表', tags: ['小红书API', '实时数据'] }
                    ]
                },
                {
                    name: '种草效果',
                    tables: [
                        { name: 'ods_xhs_post_note_report_di', desc: '投后数据笔记层每日报表', tags: ['小红书API', '日增量'] }
                    ]
                },
                {
                    name: '投流效果',
                    tables: [
                        { name: 'ods_xhs_creative_report_hi', desc: '创意层小时离线报表', tags: ['小红书API', '小时增量'] },
                        { name: 'ods_xhs_audience_report_di', desc: '人群包每日离线报表', tags: ['小红书API', '日增量'] },
                        { name: 'ods_xhs_spu_report_di', desc: 'SPU层每日离线报表', tags: ['小红书API', '日增量'] },
                        { name: 'ods_xhs_search_term_report_di', desc: '搜索词每日离线报表', tags: ['小红书API', '日增量'] },
                        { name: 'ods_xhs_keyword_report_di', desc: '关键词每日离线报表', tags: ['小红书API', '日增量'] }
                    ]
                },
                {
                    name: '转化效果',
                    tables: [
                        { name: 'ods_xhs_grass_ad_conversion_di', desc: '种草联盟投流转化每日数据', tags: ['项目管理中心', '仅120天', 'T-2', '归因 15/30', '日增量'] },
                        { name: 'ods_xhs_grass_task_conversion_di', desc: '种草联盟转化每日数据-任务组', tags: ['项目管理中心', 'T-2', '仅120天', '归因 15/30', '日增量'] },
                        { name: 'ods_xhs_grass_content_conversion_di', desc: '种草联盟转化每日数据-内容组', tags: ['项目管理中心', 'T-2', '仅120天', '归因 15/30', '日增量'] }
                    ]
                },
                {
                    name: '项目规划',
                    tables: [
                        { name: 'ods_xhs_budget_plan_df', desc: '预算规划', tags: ['项目管理中心', '日全量'] },
                        { name: 'ods_xhs_kpi_plan_df', desc: 'KPI规划', tags: ['项目管理中心', '日全量'] }
                    ]
                },
                {
                    name: '其他数据',
                    tables: [
                        { name: 'ods_xhs_account_flow_df', desc: '投流账户每日流水', tags: ['项目管理中心', '日全量'] }
                    ]
                }
            ],
            tables: [] // 保留兼容性
        },
        {
            id: 'dwd',
            name: 'DWD',
            fullName: '明细数据层',
            description: '对 ODS 层数据进行清洗、标准化、维度关联，形成一致性的明细事实表。',
            groups: [
                {
                    name: '实时效果',
                    tables: [
                        { name: 'dwd_xhs_creativity_realtime_hi', desc: '创意层小时实时明细表', tags: ['实时数据', '小时增量'] }
                    ]
                },
                {
                    name: '种草效果',
                    tables: [
                        { name: 'dwd_xhs_note_daily_di', desc: '笔记层每日明细表', tags: ['数据清洗', '日增量'] }
                    ]
                },
                {
                    name: '投流效果',
                    tables: [
                        { name: 'dwd_xhs_creative_hourly_di', desc: '创意层小时明细表', tags: ['数据清洗', '小时增量'] },
                        { name: 'dwd_xhs_campaign_daily_di', desc: '计划层每日明细表', tags: ['数据清洗', '日增量'] },
                        { name: 'dwd_xhs_audience_detail_di', desc: '人群包每日明细表', tags: ['数据清洗', '日增量'] },
                        { name: 'dwd_xhs_spu_detail_di', desc: 'SPU每日明细表', tags: ['数据清洗', '日增量'] },
                        { name: 'dwd_xhs_search_term_detail_di', desc: '搜索词每日明细表', tags: ['数据清洗', '日增量'] },
                        { name: 'dwd_xhs_keyword_detail_di', desc: '关键词每日明细表', tags: ['数据清洗', '日增量'] }
                    ]
                },
                {
                    name: '其他数据',
                    tables: [
                        { name: 'dwd_xhs_budget_plan_detail_di', desc: '预算规划明细表', tags: ['数据清洗', '日增量'] }
                    ]
                }
            ],
            tables: []
        },
        {
            id: 'dim',
            name: 'DIM',
            fullName: '维度数据层',
            description: '存储维度表，包含业务实体的描述性属性，支持多维分析，与事实表关联使用。',
            groups: [
                {
                    name: '系统维度',
                    tables: [
                        { name: 'dim_xhs_date_df', desc: '时间维度', tags: ['维度表', '日全量'] }
                    ]
                },
                {
                    name: '项目维度',
                    tables: [
                        { name: 'dim_xhs_note_df', desc: '笔记维度', tags: ['维度表', '日全量'] },
                        { name: 'dim_xhs_project_df', desc: '项目维度', tags: ['维度表', '日全量'] },
                        { name: 'dim_xhs_task_group_df', desc: '任务组维度', tags: ['维度表', '日全量'] },
                        { name: 'dim_xhs_product_df', desc: '投放产品维度', tags: ['维度表', '日全量'] }
                    ]
                },
                {
                    name: '投流维度',
                    tables: [
                        { name: 'dim_xhs_spu_df', desc: 'SPU维度', tags: ['维度表', '日全量'] },
                        { name: 'dim_xhs_campaign_df', desc: '计划维度', tags: ['维度表', '日全量'] },
                        { name: 'dim_xhs_unit_df', desc: '单元维度', tags: ['维度表', '日全量'] },
                        { name: 'dim_xhs_creative_df', desc: '创意维度', tags: ['维度表', '日全量'] }
                    ]
                }
            ],
            tables: []
        },
        {
            id: 'bridge',
            name: 'BRG',
            fullName: '桥接数据层',
            description: '连接多对多关系的桥接表，用于关联事实表与维度表，支持复杂业务场景分析。',
            tables: [
                { name: 'brg_xhs_note_project_df', desc: '笔记与项目桥表', tags: ['桥表', '日全量'] }
            ]
        },
        {
            id: 'dws',
            name: 'DWS',
            fullName: '汇总数据层',
            description: '按业务主题域聚合数据，构建多维度汇总宽表，支持上层分析查询。',
            groups: [
                {
                    name: '种草效果',
                    tables: [
                        { name: 'dws_xhs_note_daily_agg', desc: '笔记层日累计表', tags: ['数据聚合', '日增量'] },
                        { name: 'dws_xhs_task_daily_agg', desc: '任务组日累计表', tags: ['数据聚合', '日增量'] },
                        { name: 'dws_xhs_project_daily_agg', desc: '项目层日累计表', tags: ['数据聚合', '日增量'] },
                        { name: 'dws_xhs_product_daily_agg', desc: '投放产品层日累计表', tags: ['数据聚合', '日增量'] }
                    ]
                },
                {
                    name: '投流效果',
                    tables: [
                        { name: 'dws_xhs_campaign_daily_agg', desc: '计划层日累计表', tags: ['数据聚合', '日增量'] },
                        { name: 'dws_xhs_audience_daily_agg', desc: '人群包日累计表', tags: ['数据聚合', '日增量'] },
                        { name: 'dws_xhs_spu_daily_agg', desc: 'SPU日累计表', tags: ['数据聚合', '日增量'] },
                        { name: 'dws_xhs_keyword_search_daily_agg', desc: '关键词&搜索词日累计表', tags: ['数据聚合', '日增量'] }
                    ]
                }
            ],
            tables: []
        },
        {
            id: 'ads',
            name: 'ADS',
            fullName: '应用数据层',
            description: '面向具体业务场景的应用数据，直接服务于报表、BI 看板、数据产品。',
            groups: [
                {
                    name: '内容互动',
                    tables: [
                        // 待设计
                    ]
                },
                {
                    name: '转化效果',
                    subgroups: [
                        {
                            name: '产品种草',
                            tables: [
                                // 待设计
                            ]
                        },
                        {
                            name: '客资收集',
                            tables: [
                                // 待设计
                            ]
                        },
                        {
                            name: '应用推广',
                            tables: [
                                // 待设计
                            ]
                        },
                        {
                            name: '种草直达',
                            tables: [
                                // 待设计
                            ]
                        }
                    ],
                    tables: []
                },
                {
                    name: '成本效益',
                    tables: [
                        // 待设计
                    ]
                },
                {
                    name: '投流效果',
                    subgroups: [
                        {
                            name: '项目',
                            tables: [
                                // 待设计
                            ]
                        },
                        {
                            name: '任务组',
                            tables: [
                                // 待设计
                            ]
                        },
                        {
                            name: '投放产品',
                            tables: [
                                // 待设计
                            ]
                        }
                    ],
                    tables: []
                }
            ],
            tables: []
        }
    ]
};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DATA_WAREHOUSE;
}
