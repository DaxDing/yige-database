/**
 * 表定义加载器
 * 统一管理所有表的字段定义
 */

const TABLE_DEFINITIONS = {
    // ODS 层表定义
    'ods_xhs_account_flow_df': {
        name: 'ods_xhs_account_flow_df',
        nameCn: '投流账户每日流水',
        layer: 'ods',
        fields: [
            { seq: 1, cat: '基础字段', name: 'dt', nameCn: '数据日期', type: 'STRING', desc: '流水数据日期', example: '2026-01-06' },
            { seq: 2, cat: '业务字段', name: 'account_type', nameCn: '账户类型', type: 'STRING', desc: '投流账户类型', example: 'ad' },
            { seq: 3, cat: '业务字段', name: 'operate_type', nameCn: '操作类型', type: 'STRING', desc: '流水操作类型', example: 'recharge' },
            { seq: 4, cat: '业务字段', name: 'cash_amount', nameCn: '金额', type: 'DECIMAL', desc: '流水金额（元），原接口 order_amount', example: '1000.00' },
            { seq: 5, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 6, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ]
    },

    // DWD 层表定义
    'dwd_xhs_creative_hourly_di': {
        name: 'dwd_xhs_creative_hourly_di',
        nameCn: '创意层小时明细表',
        layer: 'dwd',
        fields: [
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
        // 转化指标 JSON 结构定义
        metricsSchema: {
            product_seeding_metrics: {
                nameCn: '产品种草',
                fields: [
                    { name: 'search_cmt_click', nameCn: '搜索组件点击量', type: 'BIGINT' },
                    { name: 'search_cmt_after_read', nameCn: '搜后阅读量', type: 'BIGINT' },
                    { name: 'i_user_num', nameCn: '新增种草人群', type: 'BIGINT' },
                    { name: 'ti_user_num', nameCn: '新增深度种草人群', type: 'BIGINT' }
                ]
            },
            lead_collection_metrics: {
                nameCn: '客资收集',
                fields: [
                    { name: 'leads', nameCn: '表单提交', type: 'BIGINT' },
                    { name: 'landing_page_visit', nameCn: '落地页访问量', type: 'BIGINT' },
                    { name: 'leads_button_impression', nameCn: '表单按钮曝光量', type: 'BIGINT' },
                    { name: 'message_user', nameCn: '私信进线人数', type: 'BIGINT' },
                    { name: 'message', nameCn: '私信开口条数', type: 'BIGINT' },
                    { name: 'message_consult', nameCn: '私信进线数', type: 'BIGINT' },
                    { name: 'initiative_message', nameCn: '私信开口数', type: 'BIGINT' },
                    { name: 'msg_leads_num', nameCn: '私信留资数', type: 'BIGINT' }
                ]
            },
            app_promotion_metrics: {
                nameCn: '应用推广',
                fields: [
                    { name: 'invoke_app_open_cnt', nameCn: 'APP打开量（唤起）', type: 'BIGINT' },
                    { name: 'invoke_app_enter_store_cnt', nameCn: 'APP进店量（唤起）', type: 'BIGINT' },
                    { name: 'invoke_app_engagement_cnt', nameCn: 'APP互动量（唤起）', type: 'BIGINT' },
                    { name: 'invoke_app_payment_cnt', nameCn: 'APP支付次数（唤起）', type: 'BIGINT' },
                    { name: 'search_invoke_button_click_cnt', nameCn: 'APP打开按钮点击量（唤起）', type: 'BIGINT' },
                    { name: 'invoke_app_payment_amount', nameCn: 'APP支付金额（唤起）', type: 'DECIMAL' },
                    { name: 'app_activate_cnt', nameCn: '激活数', type: 'BIGINT' },
                    { name: 'app_register_cnt', nameCn: '注册数', type: 'BIGINT' },
                    { name: 'first_app_pay_cnt', nameCn: '首次付费数', type: 'BIGINT' },
                    { name: 'current_app_pay_cnt', nameCn: '当日付费次数', type: 'BIGINT' },
                    { name: 'app_key_action_cnt', nameCn: '关键行为数', type: 'BIGINT' },
                    { name: 'app_pay_cnt_7d', nameCn: '7日付费次数', type: 'BIGINT' },
                    { name: 'app_pay_amount', nameCn: '付费金额', type: 'DECIMAL' },
                    { name: 'app_activate_amount_1d', nameCn: '当日LTV', type: 'DECIMAL' },
                    { name: 'app_activate_amount_3d', nameCn: '三日LTV', type: 'DECIMAL' },
                    { name: 'app_activate_amount_7d', nameCn: '七日LTV', type: 'DECIMAL' },
                    { name: 'retention_1d_cnt', nameCn: '次留', type: 'BIGINT' },
                    { name: 'retention_3d_cnt', nameCn: '3日留存', type: 'BIGINT' },
                    { name: 'retention_7d_cnt', nameCn: '7日留存', type: 'BIGINT' }
                ]
            },
            direct_seeding_metrics: {
                nameCn: '种草直达',
                fields: [
                    { name: 'external_goods_visit_7', nameCn: '行业商品点击量', type: 'BIGINT' },
                    { name: 'external_goods_order_7', nameCn: '行业商品成交订单量（7日）', type: 'BIGINT' },
                    { name: 'external_rgmv_7', nameCn: '行业商品GMV（7日）', type: 'DECIMAL' },
                    { name: 'external_goods_order_15', nameCn: '行业商品成交订单量（15日）', type: 'BIGINT' },
                    { name: 'external_rgmv_15', nameCn: '行业商品GMV（15日）', type: 'DECIMAL' },
                    { name: 'external_goods_order_price_15', nameCn: '行业商品成交订单成本（15日）', type: 'DECIMAL' },
                    { name: 'external_goods_order_30', nameCn: '行业商品成交订单量（30日）', type: 'BIGINT' },
                    { name: 'external_rgmv_30', nameCn: '行业商品GMV（30日）', type: 'DECIMAL' },
                    { name: 'external_goods_order_price_30', nameCn: '行业商品成交订单成本（30日）', type: 'DECIMAL' }
                ]
            }
        }
    },

    // DWD 实时效果表定义
    'dwd_xhs_creativity_realtime_hi': {
        name: 'dwd_xhs_creativity_realtime_hi',
        nameCn: '创意层小时实时明细表',
        layer: 'dwd',
        source: 'ods_xhs_jg_creativity_realtime_hi',
        fields: [
            { seq: 1, cat: '标识字段', name: 'advertiser_id', nameCn: '投放账号ID', type: 'STRING', desc: '聚光投放账户标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '标识字段', name: 'creativity_id', nameCn: '创意ID', type: 'STRING', desc: '创意标识', example: '3437479586', key: 'PK' },
            { seq: 3, cat: '标识字段', name: 'unit_id', nameCn: '单元ID', type: 'STRING', desc: '广告单元标识', example: '485522692' },
            { seq: 4, cat: '标识字段', name: 'campaign_id', nameCn: '计划ID', type: 'STRING', desc: '广告计划标识', example: '167978148' },
            { seq: 5, cat: '标识字段', name: 'note_id', nameCn: '笔记ID', type: 'STRING', desc: '投放的笔记标识', example: '695deca2000000000a03cdc7' },
            { seq: 6, cat: '属性字段', name: 'creativity_name', nameCn: '创意名称', type: 'STRING', desc: '创意显示名称', example: '善弈+信息流+互点' },
            { seq: 7, cat: '属性字段', name: 'creativity_type', nameCn: '创意类型', type: 'INT', desc: '创意类型编码', example: '12' },
            { seq: 8, cat: '属性字段', name: 'creativity_filter_state', nameCn: '创意状态', type: 'INT', desc: '创意过滤状态', example: '8' },
            { seq: 9, cat: '策略字段', name: 'placement', nameCn: '投放位置', type: 'INT', desc: '广告投放位置类型', example: '1' },
            { seq: 10, cat: '策略字段', name: 'marketing_target', nameCn: '营销目标', type: 'INT', desc: '营销目标类型编码', example: '4' },
            { seq: 11, cat: '策略字段', name: 'promotion_target', nameCn: '推广目标', type: 'INT', desc: '推广目标类型编码', example: '1' },
            { seq: 12, cat: '策略字段', name: 'optimize_target', nameCn: '优化目标', type: 'INT', desc: '出价优化目标类型', example: '1' },
            { seq: 13, cat: '策略字段', name: 'bidding_strategy', nameCn: '竞价策略', type: 'INT', desc: '竞价策略类型编码', example: '7' },
            { seq: 14, cat: '策略字段', name: 'event_bid', nameCn: '出价', type: 'DECIMAL', desc: '事件出价（元）', example: '75' },
            { seq: 15, cat: '时间字段', name: 'stat_date', nameCn: '统计日期', type: 'STRING', desc: '数据统计日期', example: '2026-01-13', key: 'PK' },
            { seq: 16, cat: '时间字段', name: 'stat_hour', nameCn: '统计小时', type: 'STRING', desc: '数据统计小时', example: '14', key: 'PK' },
            { seq: 17, cat: '展现指标', name: 'fee', nameCn: '消费', type: 'DECIMAL', desc: '广告消费金额（元）', example: '94.48' },
            { seq: 18, cat: '展现指标', name: 'impression', nameCn: '展现量', type: 'BIGINT', desc: '广告展现次数', example: '1450' },
            { seq: 19, cat: '展现指标', name: 'click', nameCn: '点击量', type: 'BIGINT', desc: '广告点击次数', example: '118' },
            { seq: 20, cat: '笔记指标', name: 'like', nameCn: '点赞', type: 'BIGINT', desc: '笔记点赞数', example: '6' },
            { seq: 21, cat: '笔记指标', name: 'comment', nameCn: '评论', type: 'BIGINT', desc: '笔记评论数', example: '0' },
            { seq: 22, cat: '笔记指标', name: 'collect', nameCn: '收藏', type: 'BIGINT', desc: '笔记收藏数', example: '6' },
            { seq: 23, cat: '笔记指标', name: 'share', nameCn: '分享', type: 'BIGINT', desc: '笔记分享数', example: '0' },
            { seq: 24, cat: '笔记指标', name: 'follow', nameCn: '关注', type: 'BIGINT', desc: '笔记带来的关注数', example: '0' },
            { seq: 25, cat: '笔记指标', name: 'interaction', nameCn: '互动量', type: 'BIGINT', desc: '笔记总互动量', example: '12' },
            { seq: 26, cat: '笔记指标', name: 'pic_save', nameCn: '保存图片', type: 'BIGINT', desc: '图片保存次数', example: '2' },
            { seq: 27, cat: '产品种草', name: 'search_cmt_click', nameCn: '搜索组件点击量', type: 'BIGINT', desc: '搜索组件点击次数', example: '3' },
            { seq: 28, cat: '产品种草', name: 'search_cmt_after_read', nameCn: '搜后阅读量', type: 'BIGINT', desc: '点击搜索组件后的阅读量', example: '1' },
            { seq: 29, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-13 14:05:00' },
            { seq: 30, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260113', key: 'PT' }
        ]
    },

    // DIM 层表定义
    'dim_xhs_advertiser_df': {
        name: 'dim_xhs_advertiser_df',
        nameCn: '广告主维度',
        layer: 'dim',
        fields: [
            { seq: 1, cat: '主键', name: 'advertiser_id', nameCn: '广告主ID', type: 'STRING', desc: '广告主唯一标识', example: '6823119876', key: 'PK' },
            { seq: 2, cat: '基础属性', name: 'advertiser_name', nameCn: '广告主名称', type: 'STRING', desc: '广告主显示名称', example: '品牌A官方账号' },
            { seq: 3, cat: '基础属性', name: 'industry', nameCn: '所属行业', type: 'STRING', desc: '广告主所属行业分类', example: '美妆护肤' },
            { seq: 4, cat: '基础属性', name: 'status', nameCn: '账户状态', type: 'STRING', desc: '广告主账户状态', example: 'active' },
            { seq: 5, cat: '系统字段', name: 'etl_time', nameCn: 'ETL时间', type: 'DATETIME', desc: '数据同步处理时间戳', example: '2026-01-07 11:30:00' },
            { seq: 6, cat: '系统字段', name: 'ds', nameCn: '分区日期', type: 'STRING', desc: '存储分区日期，格式 YYYYMMDD', example: '20260107', key: 'PT' }
        ]
    }
};

/**
 * 获取表字段定义
 * @param {string} tableName 表名
 * @returns {Array} 字段列表
 */
function getTableFields(tableName) {
    const tableDef = TABLE_DEFINITIONS[tableName];
    return tableDef ? tableDef.fields : null;
}

/**
 * 获取表定义
 * @param {string} tableName 表名
 * @returns {Object} 表定义对象
 */
function getTableDefinition(tableName) {
    return TABLE_DEFINITIONS[tableName] || null;
}

/**
 * 获取所有表名
 * @returns {Array} 表名列表
 */
function getAllTableNames() {
    return Object.keys(TABLE_DEFINITIONS);
}

// 导出给其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TABLE_DEFINITIONS, getTableFields, getTableDefinition, getAllTableNames };
}
