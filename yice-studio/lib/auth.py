"""认证与会话管理"""

import hashlib
import os
import secrets
import threading
import time
from http.cookies import SimpleCookie

from settings import AUTH, CONFIG_DIR
from lib.utils import read_config, write_config

_sessions = {}
_sessions_lock = threading.Lock()
PUBLIC_PATHS = {'/api/login', '/api/auth/feishu', '/api/auth/feishu/callback'}


def hash_pw(password):
    return hashlib.sha256((AUTH['salt'] + password).encode()).hexdigest()


def load_users():
    return read_config('users.json') if os.path.exists(os.path.join(CONFIG_DIR, 'users.json')) else []


def create_session(user):
    sid = secrets.token_hex(32)
    with _sessions_lock:
        _sessions[sid] = {
            'user': {k: user[k] for k in ('id', 'name', 'role', 'avatar', 'department') if k in user},
            'expires': time.time() + AUTH['session_ttl'],
        }
    return sid


def get_session(handler):
    cookie_str = handler.headers.get('Cookie', '')
    sc = SimpleCookie()
    try:
        sc.load(cookie_str)
    except Exception:
        return None
    morsel = sc.get(AUTH['cookie_name'])
    if not morsel:
        return None
    sid = morsel.value
    with _sessions_lock:
        s = _sessions.get(sid)
        if s and s['expires'] > time.time():
            return s['user']
        _sessions.pop(sid, None)
    return None


def set_session_cookie(handler, sid, max_age=None):
    if max_age is None:
        max_age = AUTH['session_ttl']
    handler.send_header('Set-Cookie', f"{AUTH['cookie_name']}={sid}; Path=/; HttpOnly; SameSite=Lax; Max-Age={max_age}")


def clear_session_cookie(handler):
    cookie_str = handler.headers.get('Cookie', '')
    sc = SimpleCookie()
    try:
        sc.load(cookie_str)
    except Exception:
        pass
    morsel = sc.get(AUTH['cookie_name'])
    if morsel:
        with _sessions_lock:
            _sessions.pop(morsel.value, None)
    handler.send_header('Set-Cookie', f"{AUTH['cookie_name']}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0")


def seed_users():
    """首次启动时创建默认管理员"""
    path = os.path.join(CONFIG_DIR, 'users.json')
    if os.path.exists(path):
        return
    default = [{
        'id': 'admin',
        'username': 'admin',
        'password_hash': hash_pw('yice2026'),
        'name': '管理员',
        'role': 'root',
        'avatar': '',
        'department': '',
        'feishu_open_id': '',
    }]
    write_config('users.json', default)
    print('  初始账号: admin / yice2026', flush=True)
