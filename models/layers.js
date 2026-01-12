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
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '标识字段', name: 'campaign_id', nameCn: '计划ID', type: 'STRING', desc: '广告计划标识', example: '123456789' },
            { seq: 3, cat: '标识字段', name: 'unit_id', nameCn: '单元ID', type: 'STRING', desc: '广告单元标识', example: '987654321' },
            { seq: 4, cat: '标识字段', name: 'creative_id', nameCn: '创意ID', type: 'STRING', desc: '广告创意标识', example: '111222333', key: 'PK' },
            { seq: 5, cat: '标识字段', name: 'note_id', nameCn: '笔记ID', type: 'STRING', desc: '关联笔记标识', example: '65a1b2c3d4' },
            { seq: 7, cat: '时间字段', name: 'stat_date', nameCn: '统计日期', type: 'STRING', desc: '数据统计日期', example: '2026-01-06', key: 'PK' },
            { seq: 8, cat: '时间字段', name: 'stat_hour', nameCn: '统计小时', type: 'STRING', desc: '数据统计小时', example: '14', key: 'PK' },
            { seq: 9, cat: '效果指标', name: 'impression', nameCn: '曝光数', type: 'BIGINT', desc: '广告曝光次数', example: '10000' },
            { seq: 10, cat: '效果指标', name: 'click', nameCn: '点击数', type: 'BIGINT', desc: '广告点击次数', example: '500' },
            { seq: 11, cat: '效果指标', name: 'cost', nameCn: '消耗', type: 'DECIMAL(18,2)', desc: '广告消耗金额（元）', example: '1234.56' },
            { seq: 12, cat: '互动指标', name: 'note_click', nameCn: '笔记点击', type: 'BIGINT', desc: '笔记点击次数', example: '800' },
            { seq: 13, cat: '互动指标', name: 'note_like', nameCn: '笔记点赞', type: 'BIGINT', desc: '笔记点赞次数', example: '200' },
            { seq: 14, cat: '互动指标', name: 'note_collect', nameCn: '笔记收藏', type: 'BIGINT', desc: '笔记收藏次数', example: '100' },
            { seq: 15, cat: '互动指标', name: 'note_comment', nameCn: '笔记评论', type: 'BIGINT', desc: '笔记评论次数', example: '50' },
            { seq: 16, cat: '互动指标', name: 'note_share', nameCn: '笔记分享', type: 'BIGINT', desc: '笔记分享次数', example: '30' },
            { seq: 17, cat: '互动指标', name: 'note_follow', nameCn: '笔记关注', type: 'BIGINT', desc: '通过笔记关注次数', example: '20' },
            { seq: 18, cat: '转化指标', name: 'form_submit', nameCn: '表单提交', type: 'BIGINT', desc: '表单提交次数', example: '10' },
            { seq: 19, cat: '转化指标', name: 'consult', nameCn: '私信咨询', type: 'BIGINT', desc: '私信咨询次数', example: '15' },
            { seq: 20, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 21, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
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
