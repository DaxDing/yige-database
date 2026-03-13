# YICE Studio

小红书营销数仓的 Web 前端 + API 服务。纯 Python HTTP 服务，无框架依赖；前端原生 HTML/JS，无构建步骤。

## 启动

```bash
set -a && source .env && set +a
python3 yice-studio/server.py          # 默认 :8080
python3 yice-studio/server.py 3000     # 自定义端口
```

## 架构

```
浏览器 ──> server.py (路由 shell, 365 行)
              │
              ├── lib/auth.py      认证会话 (91)
              ├── lib/cache.py     内存缓存 (45)
              ├── lib/mc.py        MaxCompute 查询 (125)
              ├── lib/pg.py        PostgreSQL 查询 (176)
              ├── lib/feishu.py    飞书 API + OAuth (256)
              ├── lib/chat.py      Claude CLI + ASR (293)
              └── lib/utils.py     序列化/校验/配置读写 (38)

settings.py  所有配置（端口、AK、DB、飞书、ASR）(149)
```

### 数据流

```
.env → settings.py → lib/* → server.py → 浏览器
                        ↕
           MaxCompute / PostgreSQL / 飞书 API / Claude CLI / 火山 ASR
```

### 模块依赖

```
settings ← utils ← cache
                      ↑
        auth ─────────┘
        mc ───────────┘  (mc → pg: 延迟导入 query_project_names)
        pg ───────────┘
        feishu ───────┘  (feishu → auth: OAuth 用户创建)
        chat ─────────── (chat → auth: 获取当前用户)
```

禁止 cache → 任何业务模块（避免循环）。预热逻辑在 server.py 编排。

## 前端

| 页面 | 文件 | 功能 |
|------|------|------|
| 业务看板 | `ads-report.html` (2065) | ADS 报表、KPI、多看板 Tab |
| 投流工作台 | `ad-studio.html` (1646) | 投流策略、素材管理 |
| 一致性检查 | `consistency-check.html` (1466) | 数据质量校验 |
| 项目管理 | `project-management.html` (1689) | 项目/账号配置 |
| 登录 | `login.html` (292) | 账密 + 飞书 OAuth |

### 组件 (widgets/)

每个 widget 是独立 JS 模块，通过 `<script src="widgets/xxx/index.js">` 注入到页面。

| Widget | 行数 | 功能 |
|--------|------|------|
| `auth/` | 73 | 登录态检查、跳转 login.html |
| `chat/` | 665 | AI 聊天面板（Claude CLI 代理、语音输入、历史记录） |
| `refresh/` | 48 | 缓存刷新按钮 |
| `settings-menu/` | 34 | 设置菜单 |

### 看板 (dashboards/)

注册式看板系统。`_shared.js` 提供 `registerDashboard()` 注册机制。

| 目录 | 看板 |
|------|------|
| `fixed/` | project, note, content_theme, content_selection, cross_project, kpi_progress, task_group |
| `free/` | free_spend |
| `scheduled_tasks/` | 定时任务监控 |

## API

### 公开端点

| Method | Path | 功能 |
|--------|------|------|
| POST | `/api/login` | 账密登录 |
| GET | `/api/me` | 当前用户 |
| GET | `/api/auth/feishu` | 飞书 OAuth 跳转 |
| GET | `/api/auth/feishu/callback` | 飞书 OAuth 回调 |

### 认证端点

| Method | Path | 处理模块 | 功能 |
|--------|------|----------|------|
| POST | `/api/logout` | auth | 登出 |
| GET | `/api/ads?start=&end=&table=&refresh=&counts=` | mc | ADS 报表查询 |
| GET | `/api/project_names` | pg | 项目名称映射 |
| GET | `/api/cherk` | pg | 一致性检查数据 |
| GET | `/api/dim-stats` | pg | 维度基准统计 |
| GET | `/api/feishu/departments` | feishu | 飞书部门 |
| GET | `/api/feishu/employees` | feishu | 飞书员工 |
| GET | `/api/feishu/config` | feishu | 飞书配置 |
| GET | `/api/refresh` | server | 清空缓存+预热 |
| GET | `/api/chat/history?session_id=` | chat | 聊天历史 |
| POST | `/api/chat` | chat | Claude CLI SSE 流式对话 |
| POST | `/api/chat/reset` | chat | 重置会话 |
| POST | `/api/chat/upload` | chat | 文件上传 |
| POST | `/api/chat/asr` | chat | 语音转文字 |
| POST | `/api/projects/save` | utils | 保存项目配置 |
| POST | `/api/accounts/save` | utils | 保存账号配置 |

## 配置文件

| 文件 | 格式 | 功能 |
|------|------|------|
| `config/projects.json` | `[{id, name, ...}]` | 项目列表 |
| `config/accounts.json` | `[{id, name, ...}]` | 投放账号 |
| `config/users.json` | `[{id, username, password_hash, role, feishu_open_id, ...}]` | 用户表 |

首次启动自动创建 admin/yice2026。

## 运行时目录

```
out/
├── .chat_users/{username}/sessions/{session_id}.json   聊天记录
└── .chat_uploads/{timestamp}_{filename}                上传文件
```

## 缓存机制

- 内存字典，TTL 24h，上限 64 条
- 启动后台线程预热（MC + PG + 飞书）
- 每天 03:00 自动刷新
- `GET /api/refresh` 手动刷新
- 大 JSON 预压缩 gzip，`send_cached()` 跳过序列化

## 认证机制

- Cookie-based session（`yice_sid`），服务端内存存储，TTL 7 天
- 密码 SHA256(salt + password) 哈希
- 飞书 OAuth: 自动创建用户，role=member
- 静态文件不拦截，前端 auth widget 自行检查

## 关键约定

- 新增 API：在 `settings.py` 的 `API_ROUTES` 注册路由，在 `server.py` 添加分发
- 新增查询：在对应 `lib/` 模块添加函数，用 `cache.get/put` 管理缓存
- 新增页面：创建 HTML，引入需要的 widgets，数据通过 fetch API 获取
- 新增看板：在 `dashboards/` 下创建 JS，调用 `registerDashboard()` 注册
- 前端无构建：直接编辑 HTML/JS，刷新浏览器即可
- 后端改动：改 `lib/*.py` 或 `server.py` 后需重启 Python 进程
