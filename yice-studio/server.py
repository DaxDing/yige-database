#!/usr/bin/env python3
"""YICE 数据服务

路由层：接收 HTTP 请求，分发到 lib/ 模块处理。

启动:
    export $(cat .env | xargs) && python3 yice-studio/server.py [port]
"""

import gzip as gzip_mod
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

from settings import (
    STUDIO_DIR, SERVER, ADS_TABLES, FEISHU, API_ROUTES, check_env,
)
from lib import cache, auth, mc, pg, feishu, chat
from lib.utils import read_config, write_config, validate_ds

R = API_ROUTES


# ── 缓存预热 ──

def _fill_cache():
    print(f'[{datetime.now():%H:%M}] 开始缓存预热…')
    today = datetime.now()
    end_ds = (today - timedelta(days=1)).strftime('%Y%m%d')
    start_ds = (today - timedelta(days=9)).strftime('%Y%m%d')
    tasks = [
        ('ads', lambda: mc.query_ads(start_ds, end_ds)),
        ('project_names', lambda: pg.query_project_names()),
        ('cherk', lambda: pg.query_cherk()),
        ('dim_stats', lambda: pg.query_dim_stats()),
        ('feishu_depts', lambda: feishu.query_departments('0', recursive=True)),
        ('feishu_emps', lambda: feishu.query_employees()),
    ]
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = {executor.submit(fn): name for name, fn in tasks}
        for future in futures:
            name = futures[future]
            try:
                future.result()
                print(f'  ✓ {name}')
            except Exception as e:
                print(f'  ✗ {name}: {e}')
    print(f'[{datetime.now():%H:%M}] 缓存预热完成')


def _warm_cache():
    cache.clear()
    _fill_cache()


def _schedule_nightly_refresh():
    import time as _time

    def _run():
        while True:
            now = datetime.now()
            target = now.replace(hour=3, minute=0, second=0, microsecond=0)
            if target <= now:
                target += timedelta(days=1)
            _time.sleep((target - now).total_seconds())
            _warm_cache()
    t = threading.Thread(target=_run, daemon=True)
    t.start()


# ── HTTP Handler ──

class APIHandler(SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _read_body(self, max_size=SERVER['max_body']):
        length = int(self.headers.get('Content-Length', 0))
        if length > max_size:
            raise ValueError(f'请求体过大: {length} > {max_size}')
        return self.rfile.read(length)

    def _require_auth(self):
        user = auth.get_session(self)
        if not user:
            self.send_json(401, {'error': '未登录'})
        return user

    # ── POST ──

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path == R['login']:
                self._handle_login()
            elif parsed.path == R['logout']:
                self._handle_logout()
            elif not self._require_auth():
                return
            elif parsed.path == R['chat']:
                chat.handle_chat(self)
            elif parsed.path == '/api/chat/reset':
                user = auth.get_session(self)
                user_key = user if isinstance(user, str) else user.get('username', 'anonymous')
                chat.reset_session(user_key)
                self.send_json(200, {'ok': True})
            elif parsed.path == '/api/chat/rename':
                user = auth.get_session(self)
                user_key = user if isinstance(user, str) else user.get('username', 'anonymous')
                body = json.loads(self._read_body())
                sid = body.get('session_id', '')
                name = body.get('name', '')
                if not sid or not name:
                    self.send_json(400, {'error': 'session_id and name required'})
                else:
                    chat.rename_session(user_key, sid, name)
                    self.send_json(200, {'ok': True})
            elif parsed.path == '/api/chat/upload':
                chat.handle_upload(self)
            elif parsed.path == '/api/chat/asr':
                chat.handle_asr(self)
            elif parsed.path == R['projects_save']:
                data = json.loads(self._read_body())
                write_config('projects.json', data)
                self.send_json(200, {'ok': True})
            elif parsed.path == R['accounts_save']:
                data = json.loads(self._read_body())
                write_config('accounts.json', data)
                self.send_json(200, {'ok': True})
            else:
                self.send_error(404)
        except ValueError as e:
            self.send_json(400, {'error': str(e)})
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def _handle_login(self):
        body = json.loads(self._read_body())
        username = body.get('username', '').strip()
        password = body.get('password', '')
        if not username or not password:
            self.send_json(400, {'error': '请输入用户名和密码'})
            return
        users = auth.load_users()
        user = next((u for u in users if u['username'] == username), None)
        if not user or user['password_hash'] != auth.hash_pw(password):
            self.send_json(401, {'error': '用户名或密码错误'})
            return
        sid = auth.create_session(user)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        auth.set_session_cookie(self, sid)
        self.end_headers()
        resp = json.dumps({'ok': True, 'user': {k: user.get(k, '') for k in ('id', 'name', 'role', 'avatar', 'department')}}, ensure_ascii=False).encode()
        self.wfile.write(resp)

    def _handle_logout(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        auth.clear_session_cookie(self)
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    # ── GET ──

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == R['me']:
            user = auth.get_session(self)
            self.send_json(200, user) if user else self.send_json(401, {'error': '未登录'})
            return
        if path == R['auth_feishu']:
            feishu.handle_redirect(self)
            return
        if path == R['auth_feishu_cb']:
            feishu.handle_callback(self, parsed)
            return
        if path == '/':
            self.send_response(302)
            self.send_header('Location', SERVER['default_redirect'])
            self.end_headers()
            return
        if not path.startswith('/api/'):
            super().do_GET()
            return

        if not self._require_auth():
            return

        if path == '/api/chat/history':
            user = auth.get_session(self)
            user_key = user if isinstance(user, str) else user.get('username', 'anonymous')
            sid = parse_qs(parsed.query).get('session_id', [None])[0]
            if sid:
                self.send_json(200, {'messages': chat.load_session(user_key, sid)})
            else:
                self.send_json(200, {'sessions': chat.list_sessions(user_key)})
        elif path == R['ads']:
            self._handle_ads(parsed)
        elif path == R['project_names']:
            try:
                refresh = parse_qs(parsed.query).get('refresh', ['0'])[0] == '1'
                self.send_json(200, pg.query_project_names(refresh))
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == R['cherk']:
            self._handle_cherk(parsed)
        elif path == R['feishu_departments']:
            params = parse_qs(parsed.query)
            try:
                depts = feishu.query_departments(
                    params.get('parent_id', ['0'])[0],
                    recursive=params.get('recursive', ['0'])[0] == '1',
                    refresh=params.get('refresh', ['0'])[0] == '1',
                )
                self.send_json(200, {'departments': depts})
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == R['feishu_employees']:
            params = parse_qs(parsed.query)
            try:
                emps = feishu.query_employees(
                    params.get('department_id', [None])[0],
                    refresh=params.get('refresh', ['0'])[0] == '1',
                )
                self.send_json(200, {'employees': emps})
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == R['feishu_config']:
            secret = FEISHU['app_secret']
            masked = secret[:4] + '****' + secret[-4:] if len(secret) > 8 else '****'
            self.send_json(200, {'app_id': FEISHU['app_id'], 'secret_masked': masked, 'secret': secret})
        elif path == R['dim_stats']:
            try:
                refresh = 'refresh' in parse_qs(parsed.query)
                self.send_json(200, pg.query_dim_stats(refresh))
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        elif path == '/api/refresh':
            cache.clear()
            threading.Thread(target=_fill_cache, daemon=True).start()
            self.send_json(200, {'status': 'ok'})
        elif path in ('/projects.json', '/accounts.json'):
            try:
                self.send_json(200, read_config(os.path.basename(path)))
            except Exception as e:
                self.send_json(500, {'error': str(e)})
        else:
            self.send_error(404)

    def _handle_ads(self, parsed):
        params = parse_qs(parsed.query)
        today = datetime.now()
        default_end = today - timedelta(days=1)
        default_start = default_end - timedelta(days=8)
        start = params.get('start', [default_start.strftime('%Y%m%d')])[0].replace('-', '')
        end = params.get('end', [default_end.strftime('%Y%m%d')])[0].replace('-', '')
        refresh = params.get('refresh', ['0'])[0] == '1'
        table = params.get('table', [None])[0]
        counts_only = params.get('counts', ['0'])[0] == '1'
        try:
            validate_ds(start)
            validate_ds(end)
            if counts_only:
                entity_keys = {
                    'project': 'project_id', 'task_group': 'task_group_name',
                    'content_theme': 'content_theme', 'note': 'note_id',
                }
                counts = {}
                for key in ADS_TABLES:
                    cached = cache.get(f'ads_{key}_{start}_{end}')
                    if cached and cached.get('rows'):
                        ek = entity_keys.get(key)
                        counts[key] = len({r[ek] for r in cached['rows'] if r.get(ek)}) if ek else cached['count']
                    else:
                        counts[key] = 0
                self.send_json(200, {'counts': counts})
                return
            if table and table in ADS_TABLES:
                cache_key = f'ads_{table}_{start}_{end}'
                if not refresh and self._send_cached(200, cache_key):
                    return
                data = mc.query_ads_table(table, start, end, refresh)
            else:
                cache_key = f'ads_{start}_{end}'
                if not refresh and self._send_cached(200, cache_key):
                    return
                data = mc.query_ads(start, end, refresh)
            if not self._send_cached(200, cache_key):
                self.send_json(200, data)
        except ValueError as e:
            self.send_json(400, {'error': str(e)})
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def _handle_cherk(self, parsed):
        params = parse_qs(parsed.query)
        refresh = params.get('refresh', ['0'])[0] == '1'
        try:
            self.send_json(200, pg.query_cherk(refresh))
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    # ── 响应工具 ──

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        is_gz = False
        if 'gzip' in self.headers.get('Accept-Encoding', '') and len(body) > 1024:
            body = gzip_mod.compress(body, compresslevel=6)
            is_gz = True
        self._write_response(code, body, is_gz)

    def _send_cached(self, code, cache_key):
        accept_gz = 'gzip' in self.headers.get('Accept-Encoding', '')
        body, is_gz = cache.get_bytes(cache_key, accept_gz)
        if body:
            self._write_response(code, body, is_gz)
            return True
        return False

    def _write_response(self, code, body, is_gzip=False):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        if is_gzip:
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        if '/api/' in str(args[0]):
            super().log_message(fmt, *args)


class ThreadedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


# ── Startup ──

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else SERVER['port']

    os.chdir(STUDIO_DIR)

    print(f'YICE Data Studio: http://localhost:{port}')
    for key, route in API_ROUTES.items():
        print(f'  {route}')
    warns = check_env()
    for w in warns:
        print(f'  ⚠ {w}')

    auth.seed_users()
    _schedule_nightly_refresh()
    threading.Thread(target=_warm_cache, daemon=True).start()
    server = ThreadedServer((SERVER['host'], port), APIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止')
