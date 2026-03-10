# 星河 API Reference

## 重要：请求方式

效果数据 API 有 TLS 指纹检测（bxpunish），Python requests 会被拦截。
**所有 API 请求必须在浏览器内发起**（通过 Claude javascript_tool 注入 JS）。

## 认证

浏览器已登录 adstar.alimama.com 即可，cookie 由浏览器自动携带。
JS 中需从 `document.cookie` 提取 `_tb_token_` 放入 header 和 URL 参数。

## API 端点

### 1. 任务基础信息

```
GET /api/cpa/event/info/detail?bizCode=adstar&_tb_token_={token}&eventId={eventId}
```

响应：`model.basicInfo` 含 `eventName`, `statusDesc`, `startTime`(yyyy-MM-dd), `endTime`。

### 2. 效果数据明细

```
GET /openapi/param2/1/gateway.unionpub/union.adstar.effect.data.detail.json
```

| 参数 | 值 | 说明 |
|------|-----|------|
| bizCode | adstar | |
| _tb_token_ | {token} | |
| eventId | {eventId} | |
| mediaType | RED_BOOK | 小红书 |
| startTime | URL编码 | yyyy-MM-dd HH:mm:ss |
| endTime | URL编码 | endDate + 23:59:59 |
| dataBatch | EVENT / EVENT_CONTENT | 任务/内容维度 |
| cycle | 15 / 30 | 聚合周期（天） |
| pageNo | 1 | |
| pageSize | 50 | |

响应：`data.result`(数组), `data.totalCount`, `data.totalPages`

### 3. 错误码

| code | 含义 |
|------|------|
| 601 | 未登录（cookie 失效） |
| bxpunish:1 | 反爬拦截（非浏览器请求） |

## 频率控制

- 任务内 API：无延迟
- 翻页间隔：2s
- 任务间隔：1-10s 随机
