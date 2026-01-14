# API Specifications

小红书平台 OpenAPI 规范定义。

## Structure

```
specs/
└── xhs/
    ├── jg/     # 聚光平台 (26)
    └── pgy/    # 蒲公英平台 (8)
```

## Naming

```
xhs_{platform}_{module}_{action}_v{version}.openapi.yml
```

## 聚光平台 (jg)

### OAuth
| API | Description |
|-----|-------------|
| `xhs_jg_oauth_access_token_v1` | 获取访问令牌 |
| `xhs_jg_oauth_refresh_token_v1` | 刷新访问令牌 |

### 离线报表 (report_offline)
| API | Description |
|-----|-------------|
| `xhs_jg_report_offline_account_v1` | 账户层报表 |
| `xhs_jg_report_offline_campaign_v1` | 计划层报表 |
| `xhs_jg_report_offline_unit_v1` | 单元层报表 |
| `xhs_jg_report_offline_creativity_v1` | 创意层报表 |
| `xhs_jg_report_offline_keyword_v1` | 关键词报表 |
| `xhs_jg_report_offline_searchword_v1` | 搜索词报表 |
| `xhs_jg_report_offline_spu_v1` | SPU报表 |
| `xhs_jg_report_offline_note_v1` | 笔记报表 |
| `xhs_jg_report_offline_audience_group_v2` | 人群包报表 |

### 实时报表 (report_realtime)
| API | Description |
|-----|-------------|
| `xhs_jg_report_realtime_account_v1` | 账户实时报表 |
| `xhs_jg_report_realtime_campaign_v1` | 计划实时报表 |
| `xhs_jg_report_realtime_campaign_group_v1` | 计划组实时报表 |
| `xhs_jg_report_realtime_unit_v1` | 单元实时报表 |
| `xhs_jg_report_realtime_creativity_v1` | 创意实时报表 |
| `xhs_jg_report_realtime_keyword_v1` | 关键词实时报表 |
| `xhs_jg_report_realtime_targeting_v1` | 定向实时报表 |

### 数据查询
| API | Description |
|-----|-------------|
| `xhs_jg_account_order_info_v1` | 账户订单信息 |
| `xhs_jg_agency_subaccounts_list_v1` | 代理商子账户列表 |
| `xhs_jg_note_list_v1` | 笔记列表 |
| `xhs_jg_spu_list_v1` | SPU列表 |
| `xhs_jg_keyword_recommend_v1` | 关键词推荐 |
| `xhs_jg_qualification_list_v1` | 资质列表 |
| `xhs_jg_target_group_list_v1` | 人群包列表 |
| `xhs_jg_targeting_detail_v1` | 定向详情 |

## 蒲公英平台 (pgy)

### OAuth
| API | Description |
|-----|-------------|
| `xhs_pgy_oauth_access_token_v1` | 获取访问令牌 |
| `xhs_pgy_oauth_refresh_token_v1` | 刷新访问令牌 |

### 数据查询
| API | Description |
|-----|-------------|
| `xhs_pgy_brand_search_v1` | 品牌搜索 |
| `xhs_pgy_project_search_v1` | 项目搜索 |
| `xhs_pgy_order_list_v1` | 订单列表 |
| `xhs_pgy_kol_quote_v1` | 达人报价 |
| `xhs_pgy_spu_query_v1` | SPU查询 |
| `xhs_pgy_note_post_invest_v1` | 笔记投后数据 |
