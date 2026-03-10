---
name: deploy_server
description: 部署和管理阿里云 ECS 服务器（yice-studio）。Use when user mentions 部署、发布、上线、更新服务器、重启服务、查看日志、SSH、deploy、server status, or any operation related to the ECS server at 114.55.242.136. Also trigger when user asks about yice.dax.cool or yice-studio service health.
---

# Deploy Server

通过 SSH 管理阿里云 ECS 服务器，支持部署 yice-studio、服务控制、Nginx 配置等操作。

## 连接信息

凭证从 `.env` 文件的 `ECS_*` 前缀变量读取：

```bash
ECS_SSH_HOST=114.55.242.136
ECS_SSH_PORT=22
ECS_SSH_USER=root
ECS_SSH_PASSWORD=<from .env>
```

**重要**：ECS 凭证与 DataWorks/MaxCompute 的 `ALIYUN_ACCESS_KEY_*` 是不同账号，勿混用。

## SSH 连接模式

所有远程操作使用 `sshpass` + `SSHPASS` 环境变量方式连接，避免密码中特殊字符的转义问题：

```bash
SSHPASS='<password>' sshpass -e ssh -o StrictHostKeyChecking=no root@114.55.242.136 "<command>"
```

文件上传使用 `scp`：

```bash
SSHPASS='<password>' sshpass -e scp -o StrictHostKeyChecking=no <local_file> root@114.55.242.136:<remote_path>
```

批量同步使用 `rsync`（需注意 sshpass 与 rsync 的 -e 参数配合）：

```bash
SSHPASS='<password>' rsync -avz --exclude='__pycache__' \
  -e "sshpass -e ssh -o StrictHostKeyChecking=no" \
  <local_dir>/ root@114.55.242.136:<remote_dir>/
```

## 服务器环境

| Key | Value |
|-----|-------|
| OS | Ubuntu 22.04 |
| Python | 3.10 |
| Nginx | 1.18.0 |
| Docker | 已安装 |

## 操作手册

### 1. 部署 yice-studio

完整部署流程：

```bash
# 1. 同步文件（排除缓存和 .env）
rsync -avz --exclude='__pycache__' --exclude='.env' \
  yice-studio/ root@ECS:/opt/yice-studio/

# 2. 同步 .env
scp .env root@ECS:/opt/yice-studio/.env

# 3. 安装依赖（首次或依赖变更时）
ssh root@ECS "pip3 install psycopg2-binary pyodps"

# 4. 重启服务
ssh root@ECS "systemctl restart yice-studio"

# 5. 验证
ssh root@ECS "systemctl is-active yice-studio"
curl -s -o /dev/null -w '%{http_code}' http://114.55.242.136:8080/
```

增量更新（仅改了前端文件）只需步骤 1，无需重启服务。
改了 server.py 或 .env 需要步骤 1+2+4。

### 2. 服务管理

yice-studio 已配置为 systemd 服务，开机自动启动：

```bash
systemctl start yice-studio     # 启动
systemctl stop yice-studio      # 停止
systemctl restart yice-studio   # 重启
systemctl status yice-studio    # 状态
journalctl -u yice-studio -n 50 # 最近 50 行日志
journalctl -u yice-studio -f    # 实时日志
```

服务配置文件位于 `/etc/systemd/system/yice-studio.service`，修改后需 `systemctl daemon-reload`。

### 3. Nginx 管理

配置文件：`/etc/nginx/sites-available/yice.dax.cool`

```bash
nginx -t                  # 测试配置
systemctl reload nginx    # 重载
systemctl restart nginx   # 重启
```

当前反向代理：`yice.dax.cool:80` → `127.0.0.1:8080`

### 4. 状态检查

```bash
# 服务状态
systemctl is-active yice-studio

# 端口检查
curl -s -o /dev/null -w '%{http_code}' http://114.55.242.136:8080/

# 域名检查
curl -s -o /dev/null -w '%{http_code}' http://yice.dax.cool/

# 系统资源
df -h && free -h && uptime
```

### 5. 日志查看

```bash
# yice-studio 服务日志
journalctl -u yice-studio -n 100

# Nginx 访问日志
tail -100 /var/log/nginx/access.log

# Nginx 错误日志
tail -100 /var/log/nginx/error.log
```

## 文件路径

| 位置 | 路径 |
|------|------|
| 本地项目 | `yice-studio/` |
| 远程部署 | `/opt/yice-studio/` |
| 远程 .env | `/opt/yice-studio/.env` |
| systemd 服务 | `/etc/systemd/system/yice-studio.service` |
| Nginx 配置 | `/etc/nginx/sites-available/yice.dax.cool` |
| Nginx 日志 | `/var/log/nginx/` |

## 安全组

ECS 安全组需手动在阿里云控制台管理（ECS 归属不同账号）。当前已开放：

| 端口 | 用途 |
|------|------|
| 22 | SSH |
| 80 | Nginx (yice.dax.cool) |
| 8080 | yice-studio 直连 |

## 注意事项

- `.env` 中的注释行会导致 `export $(cat .env | xargs)` 报错，systemd 的 `EnvironmentFile` 可正常处理
- SSH 长命令用分号 `;` 连接多条命令，避免 `&&` 导致 sshpass 连接中断
- 上传脚本文件再远程执行，比内联复杂命令更可靠
