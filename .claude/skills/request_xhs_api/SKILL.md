---
name: request_xhs_api
description: "请求小红书聚光/蒲公英 API。Use when user mentions 请求小红书API、拉取聚光数据、调蒲公英接口、获取报表数据, or needs to call any XHS advertising API (聚光/蒲公英). Also trigger when user wants to test an API endpoint, check API response, or fetch raw data from 小红书 ad platform."
allowed-tools: ["Bash", "Read", "Glob"]
---

# 小红书 API 请求

通过 OpenAPI 规范自动构造请求，支持聚光（jg）和蒲公英（pgy）两个平台。

## Workflow

```
1. get_token.sh → 获取 Access Token
2. 选择 OpenAPI spec → 确定接口
3. request_api.py → 构造请求 + 发送 + 分页
```

## Step 1: 获取 Token

```bash
SKILL_DIR=".claude/skills/request_xhs_api"

# 聚光 token（默认 advertiser_id=7152346）
TOKEN=$(bash $SKILL_DIR/scripts/get_token.sh jg)

# 蒲公英 token（默认 user_id=5cf89d080000000018003029）
TOKEN=$(bash $SKILL_DIR/scripts/get_token.sh pgy)

# 指定 ID
TOKEN=$(bash $SKILL_DIR/scripts/get_token.sh jg 12345678)
```

## Step 2: 选择接口

查看 `specs/README.md` 获取完整 API 列表。按平台和类型组织：

```
specs/
├── jg/     # 聚光 (26 个接口)
│   ├── report_offline   → 离线报表（账户/计划/创意/关键词/搜索词/笔记/SPU/人群包）
│   ├── report_realtime  → 实时报表（账户/计划/计划组/单元/创意/关键词/定向）
│   └── 数据查询          → 笔记列表/SPU/资质/人群包/定向详情
└── pgy/    # 蒲公英 (8 个接口)
    ├── oauth            → token 获取/刷新
    └── 数据查询          → 品牌/项目/订单/达人报价/SPU/投后数据
```

## Step 3: 发送请求

```bash
# 基础请求
python3 $SKILL_DIR/scripts/request_api.py \
    $SKILL_DIR/specs/jg/xhs_jg_report_offline_creativity_v1.openapi.yml \
    --token $TOKEN \
    --params advertiser_id=7152346 start_date=2026-03-01 end_date=2026-03-08

# 全量分页
python3 $SKILL_DIR/scripts/request_api.py \
    $SKILL_DIR/specs/pgy/xhs_pgy_note_post_invest_v1.openapi.yml \
    --token $TOKEN \
    --params user_id=xxx start_time=2026-03-01 end_time=2026-03-08 \
    --all-pages

# 输出到文件
python3 $SKILL_DIR/scripts/request_api.py \
    $SKILL_DIR/specs/jg/xhs_jg_note_list_v1.openapi.yml \
    --token $TOKEN \
    --params advertiser_id=7152346 \
    --all-pages --output out/data/notes.json
```

## Parameters

`--params` 接受 `KEY=VALUE` 格式，覆盖 spec 中的 default 值。

常用参数：

| Platform | Param | Description |
|----------|-------|-------------|
| jg | `advertiser_id` | 投放账号 ID（默认 7152346）|
| jg | `start_date` / `end_date` | 日期范围 YYYY-MM-DD |
| jg | `time_unit` | DAY / HOUR / SUMMARY |
| jg | `split_columns` | 维度拆分（JSON 数组）|
| pgy | `user_id` | 蒲公英用户 ID |
| pgy | `start_time` / `end_time` | 日期范围 YYYY-MM-DD |
| pgy | `date_type` | 1=自然日 2=累计 |

## Dependencies

- Python 3 + PyYAML（`pip install pyyaml`）
- curl（token 获取）
- 内网 token 服务 `121.41.12.184` 可达

## Troubleshooting

| Issue | Fix |
|-------|-----|
| token 获取失败 | 检查内网连通性，确认 advertiser_id/user_id 有效 |
| API 返回空数据 | 检查日期范围，确认账户有数据 |
| 分页中断 | 检查 rate limit，增加 sleep 间隔 |
