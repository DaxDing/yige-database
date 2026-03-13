"""飞书 API 与 OAuth"""

import json
import secrets
import urllib.error
import urllib.request
from urllib.parse import urlencode, quote, parse_qs

from settings import FEISHU, SERVER
from lib import cache, auth
from lib.utils import write_config


def tenant_token():
    """获取飞书 tenant_access_token"""
    cached = cache.get('feishu_token')
    if cached:
        return cached

    fs = FEISHU
    url = f"{fs['base_url']}/auth/v3/tenant_access_token/internal"
    body = json.dumps({
        'app_id': fs['app_id'],
        'app_secret': fs['app_secret'],
    }).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    if data.get('code') != 0:
        raise RuntimeError(f"飞书认证失败: {data.get('msg')}")
    token = data['tenant_access_token']
    cache.put('feishu_token', token)
    return token


def _get(path, params=None):
    """飞书 GET 请求"""
    token = tenant_token()
    url = f"{FEISHU['base_url']}{path}"
    if params:
        url += '?' + urlencode(params)
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        code = body.get('code', '')
        msg = body.get('msg', '')
        if code == 99991672:
            raise RuntimeError('飞书应用缺少通讯录权限，请到飞书开放平台开通 contact:contact:readonly_as_app')
        raise RuntimeError(f'飞书 API 错误 {code}: {msg}')


def _list_departments(parent_id='0'):
    all_depts = []
    page_token = None
    while True:
        params = {'department_id_type': 'open_department_id', 'parent_department_id': parent_id, 'page_size': '50'}
        if page_token:
            params['page_token'] = page_token
        data = _get('/contact/v3/departments', params)
        if data.get('code') != 0:
            raise RuntimeError(f"飞书部门查询失败: {data.get('msg')}")
        items = data.get('data', {}).get('items', [])
        all_depts.extend(items)
        if not data.get('data', {}).get('has_more'):
            break
        page_token = data['data'].get('page_token')
    return all_depts


def _format_dept(d):
    return {
        'department_id': d.get('open_department_id', ''),
        'name': d.get('name', ''),
        'parent_id': d.get('parent_department_id', ''),
        'leader_user_id': d.get('leader_user_id', ''),
        'member_count': d.get('member_count', 0),
        'status': d.get('status', {}),
    }


def query_departments(parent_id='0', recursive=False, refresh=False):
    cache_key = f'feishu_dept_{parent_id}_{"r" if recursive else "f"}'
    if not refresh:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    print(f'  查询飞书部门: parent={parent_id} recursive={recursive} ...', flush=True)
    top_depts = _list_departments(parent_id)
    result = [_format_dept(d) for d in top_depts]

    if recursive:
        queue = [d.get('open_department_id', '') for d in top_depts]
        while queue:
            pid = queue.pop(0)
            children = _list_departments(pid)
            for c in children:
                result.append(_format_dept(c))
                queue.append(c.get('open_department_id', ''))

    cache.put(cache_key, result)
    print(f'  完成: {len(result)} departments', flush=True)
    return result


def _list_users(department_id=None):
    all_users = []
    page_token = None
    while True:
        params = {'department_id_type': 'open_department_id', 'page_size': '50'}
        if department_id:
            params['department_id'] = department_id
        if page_token:
            params['page_token'] = page_token
        data = _get('/contact/v3/users', params)
        if data.get('code') != 0:
            raise RuntimeError(f"飞书员工查询失败: {data.get('msg')}")
        items = data.get('data', {}).get('items', [])
        all_users.extend(items)
        if not data.get('data', {}).get('has_more'):
            break
        page_token = data['data'].get('page_token')
    return all_users


def _format_user(u):
    return {
        'user_id': u.get('user_id', ''),
        'open_id': u.get('open_id', ''),
        'name': u.get('name', ''),
        'en_name': u.get('en_name', ''),
        'email': u.get('email', ''),
        'mobile': u.get('mobile', ''),
        'avatar': u.get('avatar', {}).get('avatar_72', ''),
        'department_ids': u.get('department_ids', []),
        'status': u.get('status', {}),
        'job_title': u.get('job_title', ''),
    }


def query_employees(department_id=None, refresh=False):
    cache_key = f'feishu_emp_{department_id or "all"}'
    if not refresh:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    print(f'  查询飞书员工: dept={department_id or "全部"} ...', flush=True)

    if department_id:
        raw = _list_users(department_id)
        result = [_format_user(u) for u in raw]
    else:
        depts = query_departments(parent_id='0', recursive=True)
        seen = set()
        result = []
        for u in _list_users():
            fu = _format_user(u)
            if fu['open_id'] not in seen:
                seen.add(fu['open_id'])
                result.append(fu)
        for dept in depts:
            for u in _list_users(dept['department_id']):
                fu = _format_user(u)
                if fu['open_id'] not in seen:
                    seen.add(fu['open_id'])
                    result.append(fu)

    cache.put(cache_key, result)
    print(f'  完成: {len(result)} employees', flush=True)
    return result


def handle_redirect(handler):
    """重定向到飞书 OAuth 登录页"""
    host = handler.headers.get('Host', 'localhost:8080')
    scheme = 'https' if host.startswith('yice.') else 'http'
    redirect_uri = quote(f'{scheme}://{host}/api/auth/feishu/callback', safe='')
    state = secrets.token_hex(16)
    url = f"https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={FEISHU['app_id']}&redirect_uri={redirect_uri}&state={state}"
    handler.send_response(302)
    handler.send_header('Location', url)
    handler.end_headers()


def handle_callback(handler, parsed):
    """飞书 OAuth 回调：用 code 换用户信息，创建会话"""
    params = parse_qs(parsed.query)
    code = params.get('code', [None])[0]
    if not code:
        handler.send_response(302)
        handler.send_header('Location', '/login.html?error=feishu_denied')
        handler.end_headers()
        return
    try:
        token = tenant_token()
        body = json.dumps({'grant_type': 'authorization_code', 'code': code}).encode()
        req = urllib.request.Request(
            f"{FEISHU['base_url']}/authen/v1/oidc/access_token",
            data=body,
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read()).get('data', {})

        user_token = data.get('access_token', '')
        if not user_token:
            raise ValueError('获取用户 token 失败')

        req2 = urllib.request.Request(
            f"{FEISHU['base_url']}/authen/v1/user_info",
            headers={'Authorization': f'Bearer {user_token}'},
        )
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            uinfo = json.loads(resp2.read()).get('data', {})

        open_id = uinfo.get('open_id', '')
        name = uinfo.get('name', uinfo.get('en_name', '飞书用户'))
        avatar = uinfo.get('avatar_thumb', uinfo.get('avatar_url', ''))

        users = auth.load_users()
        user = next((u for u in users if u.get('feishu_open_id') == open_id), None)
        if not user:
            user = {
                'id': f'feishu_{open_id}',
                'username': open_id,
                'password_hash': '',
                'name': name,
                'role': 'member',
                'avatar': avatar,
                'department': '',
                'feishu_open_id': open_id,
            }
            users.append(user)
            write_config('users.json', users)
        else:
            user['name'] = name
            user['avatar'] = avatar
            write_config('users.json', users)

        sid = auth.create_session(user)
        handler.send_response(302)
        auth.set_session_cookie(handler, sid)
        handler.send_header('Location', SERVER['default_redirect'])
        handler.end_headers()
    except Exception as e:
        print(f'飞书登录失败: {e}', flush=True)
        handler.send_response(302)
        handler.send_header('Location', '/login.html?error=feishu_fail')
        handler.end_headers()
