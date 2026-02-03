-- ============================================================
-- ETL: ODS → DWD 人群包层日离线明细
-- 源表: ods_xhs_audience_report_di
-- 目标表: dwd_xhs_audience_report_di
-- 说明: 源数据为 camelCase，DWD 列名统一 snake_case
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_audience_report_di PARTITION (ds='${bizdate}')
SELECT
    -- 标识字段
    a.advertiser_id,                                                                              -- 投放账号ID
    GET_JSON_OBJECT(a.raw_data, '$.groupId')                             AS group_id,              -- 人群包ID
    GET_JSON_OBJECT(a.raw_data, '$.groupName')                           AS group_name,            -- 人群包名称
    GET_JSON_OBJECT(a.raw_data, '$.campaignId')                          AS campaign_id,           -- 计划ID
    GET_JSON_OBJECT(a.raw_data, '$.unitId')                              AS unit_id,               -- 单元ID
    GET_JSON_OBJECT(a.raw_data, '$.creativityId')                        AS creativity_id,         -- 创意ID
    GET_JSON_OBJECT(a.raw_data, '$.noteId')                              AS note_id,               -- 笔记ID
    -- 时间字段
    a.dt,                                                                                         -- 数据时间
    -- 核心指标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.fee') AS DECIMAL(18,2))          AS fee,                   -- 消费
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.impNum') AS BIGINT), 0)           AS impression,            -- 展现量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.clickNum') AS BIGINT), 0)         AS click,                 -- 点击量
    -- 互动指标
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.engageNum') AS BIGINT), 0)        AS interaction,           -- 互动量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.favNum') AS BIGINT), 0)           AS `like`,                -- 点赞
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.collectNum') AS BIGINT), 0)       AS collect,               -- 收藏
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.cmtNum') AS BIGINT), 0)           AS `comment`,             -- 评论
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.followNum') AS BIGINT), 0)        AS follow,                -- 关注
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.shareNum') AS BIGINT), 0)         AS share,                 -- 分享
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.actionButtonClickNum') AS BIGINT), 0) AS action_button_click, -- 行动按钮点击量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.screenshotNum') AS BIGINT), 0)    AS screenshot,            -- 截图
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.saveNum') AS BIGINT), 0)          AS pic_save,              -- 保存图片
    -- 视频指标
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.videoPlayCnt') AS BIGINT), 0)     AS video_play_cnt,        -- 视频播放量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.videoPlay5sCnt') AS BIGINT), 0)   AS video_play_5s_cnt,     -- 5s播放量
    -- 转化指标: 产品种草（清理零值，含小红星/小红盟）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"searchComponentClickNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.searchComponentClickNum'), '0'), ',',
            '"searchAfterReadNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.searchAfterReadNum'), '0'), ',',
            '"iPeopleNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.iPeopleNum'), '0'), ',',
            '"tiPeopleNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.tiPeopleNum'), '0'), ',',
            '"outsideSellerPv":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outsideSellerPv'), '0'), ',',
            '"tbTaskFee":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.tbTaskFee'), '0'), ',',
            '"tbTaskClickNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.tbTaskClickNum'), '0'), ',',
            '"tbTaskReadUserCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.tbTaskReadUserCnt'), '0'), ',',
            '"jdActiveUserNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.jdActiveUserNum'), '0'), ',',
            '"jdTaskFee":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.jdTaskFee'), '0'), ',',
            '"jdTaskClickNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.jdTaskClickNum'), '0'), ',',
            '"jdTaskReadUserCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.jdTaskReadUserCnt'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS product_seeding_metrics,
    -- 转化指标: 客资收集（清理零值，含私信/企微/多转化/外链）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"leadsSuccess":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.leadsSuccess'), '0'), ',',
            '"validLeadsNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.validLeadsNum'), '0'), ',',
            '"msgLeadsFormSubmitNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msgLeadsFormSubmitNum'), '0'), ',',
            '"landingFormImpNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.landingFormImpNum'), '0'), ',',
            '"landingPagePv":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.landingPagePv'), '0'), ',',
            '"phoneCallCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.phoneCallCnt'), '0'), ',',
            '"phoneCallSuccCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.phoneCallSuccCnt'), '0'), ',',
            '"wechatCopyCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatCopyCnt'), '0'), ',',
            '"wechatCopySuccCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatCopySuccCnt'), '0'), ',',
            '"identityCertiCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.identityCertiCnt'), '0'), ',',
            '"commodityBuyCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.commodityBuyCnt'), '0'), ',',
            '"messageOpenCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.messageOpenCnt'), '0'), ',',
            '"messageDrivingOpenCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.messageDrivingOpenCnt'), '0'), ',',
            '"msgLeadsNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msgLeadsNum'), '0'), ',',
            '"messageUserCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.messageUserCnt'), '0'), ',',
            '"msgChatUserCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msgChatUserCnt'), '0'), ',',
            '"msgChatMsgCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msgChatMsgCnt'), '0'), ',',
            '"msgLeadsUserCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msgLeadsUserCnt'), '0'), ',',
            '"friendAddCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.friendAddCnt'), '0'), ',',
            '"friendAddSuccessCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.friendAddSuccessCnt'), '0'), ',',
            '"chatOpenCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.chatOpenCnt'), '0'), ',',
            '"wechatAddConsultCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAddConsultCnt'), '0'), ',',
            '"wechatAddConsultLeadsSuccessCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAddConsultLeadsSuccessCnt'), '0'), ',',
            '"extLeadsSuccNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.extLeadsSuccNum'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS lead_collection_metrics,
    -- 转化指标: 应用推广（清理零值，含APP/微信小程序/小程序/应用下载/安卓）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            -- APP内转化
            '"eventAppOpenCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.eventAppOpenCnt'), '0'), ',',
            '"eventAppEnterStoreCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.eventAppEnterStoreCnt'), '0'), ',',
            '"eventAppEngagementCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.eventAppEngagementCnt'), '0'), ',',
            '"eventAppPaymentCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.eventAppPaymentCnt'), '0'), ',',
            '"eventAppPaymentAmount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.eventAppPaymentAmount'), '0'), ',',
            '"searchInvokeButtonClickCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.searchInvokeButtonClickCnt'), '0'), ',',
            -- 微信小程序
            '"wechatAppletsOpenCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsOpenCnt'), '0'), ',',
            '"wechatAppletsActivateCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsActivateCnt'), '0'), ',',
            '"wechatAppletsPayCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsPayCnt'), '0'), ',',
            '"wechatAppletsPayAmount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsPayAmount'), '0'), ',',
            '"currentWechatAppletsActivateCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentWechatAppletsActivateCnt'), '0'), ',',
            '"currentWechatAppletsPayCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentWechatAppletsPayCnt'), '0'), ',',
            '"currentWechatAppletsPayAmount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentWechatAppletsPayAmount'), '0'), ',',
            '"currentWechatAppletsFirstPayCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentWechatAppletsFirstPayCnt'), '0'), ',',
            '"currentWechatAppletsFirstPayAmount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentWechatAppletsFirstPayAmount'), '0'), ',',
            '"wechatAppletsPayCnt3d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsPayCnt3d'), '0'), ',',
            '"wechatAppletsPayAmount3d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsPayAmount3d'), '0'), ',',
            '"wechatAppletsPayCnt7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsPayCnt7d'), '0'), ',',
            '"wechatAppletsPayAmount7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatAppletsPayAmount7d'), '0'), ',',
            '"wechatRetention1dCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatRetention1dCnt'), '0'), ',',
            '"wechatRetention3dCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatRetention3dCnt'), '0'), ',',
            '"wechatRetention7dCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechatRetention7dCnt'), '0'), ',',
            -- 小程序
            '"appletsOpenCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appletsOpenCnt'), '0'), ',',
            '"appletsPayCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appletsPayCnt'), '0'), ',',
            '"appletsPayAmount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appletsPayAmount'), '0'), ',',
            -- 应用下载
            '"appDownloadButtonClickCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appDownloadButtonClickCnt'), '0'), ',',
            '"appRegisterCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appRegisterCnt'), '0'), ',',
            '"appActivateCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appActivateCnt'), '0'), ',',
            '"currentAppActivateCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentAppActivateCnt'), '0'), ',',
            '"appKeyActionCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appKeyActionCnt'), '0'), ',',
            '"firstAppPayCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.firstAppPayCnt'), '0'), ',',
            '"currentAppPayCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentAppPayCnt'), '0'), ',',
            '"currentAppPayAmount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.currentAppPayAmount'), '0'), ',',
            '"appPayCnt7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appPayCnt7d'), '0'), ',',
            '"appPayAmount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appPayAmount'), '0'), ',',
            '"appActivateAmount1d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appActivateAmount1d'), '0'), ',',
            '"appActivateAmount3d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appActivateAmount3d'), '0'), ',',
            '"appActivateAmount7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appActivateAmount7d'), '0'), ',',
            '"retention1dCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention1dCnt'), '0'), ',',
            '"retention3dCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention3dCnt'), '0'), ',',
            '"retention7dCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention7dCnt'), '0'), ',',
            '"appBookDownloadClickCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appBookDownloadClickCnt'), '0'), ',',
            '"appBookFormSubmitCnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.appBookFormSubmitCnt'), '0'), ',',
            -- 安卓
            '"androidDownloadStarts":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.androidDownloadStarts'), '0'), ',',
            '"androidDownloadCompletions":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.androidDownloadCompletions'), '0'), ',',
            '"androidInstallCompletions":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.androidInstallCompletions'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS app_promotion_metrics,
    -- 转化指标: 种草直达（清理零值，含行业商品/微信）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"poiComponentClickNum":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.poiComponentClickNum'), '0'), ',',
            '"outClickSellerDealOrder30d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerDealOrder30d'), '0'), ',',
            '"outClickSellerDealOrder15d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerDealOrder15d'), '0'), ',',
            '"outClickSellerDealOrder7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerDealOrder7d'), '0'), ',',
            '"outClickSellerDealRgmv30d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerDealRgmv30d'), '0'), ',',
            '"outClickSellerDealRgmv15d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerDealRgmv15d'), '0'), ',',
            '"outClickSellerDealRgmv7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerDealRgmv7d'), '0'), ',',
            '"outClickSellerAddCnt30d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerAddCnt30d'), '0'), ',',
            '"outClickSellerAddCnt15d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerAddCnt15d'), '0'), ',',
            '"outClickSellerAddCnt7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickSellerAddCnt7d'), '0'), ',',
            '"outClickEnterStoreCnt30d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickEnterStoreCnt30d'), '0'), ',',
            '"outClickEnterStoreCnt15d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickEnterStoreCnt15d'), '0'), ',',
            '"outClickEnterStoreCnt7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickEnterStoreCnt7d'), '0'), ',',
            '"outClickWechatAddFriendCnt30d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickWechatAddFriendCnt30d'), '0'), ',',
            '"outClickWechatRegisterCnt30d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickWechatRegisterCnt30d'), '0'), ',',
            '"outClickWechatAccessCnt30d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.outClickWechatAccessCnt30d'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS direct_seeding_metrics,
    -- 系统字段
    GETDATE() AS etl_time
FROM ods_xhs_audience_report_di a
WHERE a.ds = '${bizdate}'
;
