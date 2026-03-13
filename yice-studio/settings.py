"""YICE 集中配置

所有连接参数、API 路径、表定义统一在此管理。
密钥从环境变量读取（.env），结构化配置直接定义。

启动前加载 .env:
    export $(cat .env | xargs) && python3 yice-studio/server.py
"""

import os

# ── 路径 ──

STUDIO_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(STUDIO_DIR)
CONFIG_DIR = os.path.join(STUDIO_DIR, 'config')

# ── 服务 ──

SERVER = {
    'port': 8080,
    'host': '0.0.0.0',
    'max_body': 1 * 1024 * 1024,  # 1 MB
    'default_redirect': '/ads-report.html',
}

# ── 缓存 ──

CACHE = {
    'ttl': 86400,      # 24 小时
    'max_entries': 64,
}

# ── MaxCompute ──

MAXCOMPUTE = {
    'access_key_id': os.environ.get('ALIYUN_ACCESS_KEY_ID', ''),
    'access_key_secret': os.environ.get('ALIYUN_ACCESS_KEY_SECRET', ''),
    'project': 'df_ch_530486',
    'endpoint': 'http://service.cn-hangzhou.maxcompute.aliyun.com/api',
}

ADS_TABLES = {
    'project': {
        'name': 'ads_xhs_project_bycontent_daily_agg',
        'order': 'ds, project_id, attribution_period',
    },
    'note': {
        'name': 'ads_xhs_note_bycontent_daily_agg',
        'order': 'ds, project_id, attribution_period, note_id',
    },
    'content_theme': {
        'name': 'ads_xhs_content_theme_bycontent_daily_agg',
        'order': 'ds, project_id, attribution_period, content_theme',
    },
    'task_group': {
        'name': 'ads_xhs_task_group_bytask_daily_agg',
        'order': 'ds, attribution_period, ad_product_name, task_group_name',
    },
}

# ── PostgreSQL ──

_PG_COMMON = {
    'host': os.environ.get('DB_HOST', ''),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'user': os.environ.get('DB_USER', ''),
    'password': os.environ.get('DB_PASSWORD', ''),
}

POSTGRES = {
    'cherk': {**_PG_COMMON, 'dbname': 'data_cherk'},
    'dim': {**_PG_COMMON, 'dbname': 'sync_dim'},
}

# ── 飞书 ──

FEISHU = {
    'app_id': os.environ.get('FEISHU_APP_ID', ''),
    'app_secret': os.environ.get('FEISHU_APP_SECRET', ''),
    'base_url': 'https://open.feishu.cn/open-apis',
}

# ── Claude Code CLI ──

CLAUDE_CLI = {
    'command': 'claude',
    'timeout': 120,  # 秒
}

# ── 火山引擎 ASR ──

VOLC_ASR = {
    'app_id': os.environ.get('VOLC_ASR_APP_ID', ''),
    'access_token': os.environ.get('VOLC_ASR_ACCESS_TOKEN', ''),
    'ws_url': 'wss://openspeech.bytedance.com/api/v3/sauc/bigmodel',
    'uid': 'yice_chat',
}

# ── ECS ──

ECS = {
    'access_key_id': os.environ.get('ECS_ALIYUN_ACCESS_KEY_ID', ''),
    'access_key_secret': os.environ.get('ECS_ALIYUN_ACCESS_KEY_SECRET', ''),
    'region_id': os.environ.get('ECS_REGION_ID', 'cn-hangzhou'),
    'instance_id': os.environ.get('ECS_INSTANCE_ID', ''),
    'ssh_host': os.environ.get('ECS_SSH_HOST', ''),
    'ssh_port': int(os.environ.get('ECS_SSH_PORT', 22)),
    'ssh_user': os.environ.get('ECS_SSH_USER', 'root'),
    'ssh_password': os.environ.get('ECS_SSH_PASSWORD', ''),
}

# ── API 路由 ──

AUTH = {
    'salt': 'yice_studio_2026',
    'session_ttl': 7 * 86400,   # 7 天
    'cookie_name': 'yice_sid',
}

API_ROUTES = {
    'login': '/api/login',
    'logout': '/api/logout',
    'me': '/api/me',
    'auth_feishu': '/api/auth/feishu',
    'auth_feishu_cb': '/api/auth/feishu/callback',
    'ads': '/api/ads',
    'project_names': '/api/project_names',
    'cherk': '/api/cherk',
    'dim_stats': '/api/dim-stats',
    'chat': '/api/chat',
    'projects_save': '/api/projects/save',
    'accounts_save': '/api/accounts/save',
    'feishu_departments': '/api/feishu/departments',
    'feishu_employees': '/api/feishu/employees',
    'feishu_config': '/api/feishu/config',
}


def check_env():
    """启动时检查关键环境变量，返回警告列表"""
    warns = []
    if not MAXCOMPUTE['access_key_id']:
        warns.append('ALIYUN_ACCESS_KEY_ID 未设置 → MaxCompute API 不可用')
    if not _PG_COMMON['host']:
        warns.append('DB_HOST 未设置 → PostgreSQL API 不可用')
    if not FEISHU['app_id']:
        warns.append('FEISHU_APP_ID 未设置 → 飞书 API 不可用')
    return warns
