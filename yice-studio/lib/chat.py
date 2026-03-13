"""Claude CLI 聊天、文件上传、语音识别"""

import json
import os
import re
import subprocess
import time

from settings import CLAUDE_CLI, VOLC_ASR, PROJECT_ROOT
from lib import auth

_sessions = {}  # user -> { 'session_id': str, 'last_active': float }
_IDLE_TIMEOUT = 1800  # 30 分钟
_USERS_DIR = os.path.join(PROJECT_ROOT, 'out', '.chat_users')
_UPLOAD_DIR = os.path.join(PROJECT_ROOT, 'out', '.chat_uploads')


def _meta_path(user_key):
    return os.path.join(_user_dir(user_key), 'meta.json')


def _load_meta(user_key):
    p = _meta_path(user_key)
    if os.path.exists(p):
        try:
            with open(p, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_meta(user_key, meta):
    with open(_meta_path(user_key), 'w') as f:
        json.dump(meta, f, ensure_ascii=False)


def _user_dir(user_key):
    d = os.path.join(_USERS_DIR, re.sub(r'[^\w.\-]', '_', user_key))
    os.makedirs(os.path.join(d, 'sessions'), exist_ok=True)
    return d


def _save_msg(user_key, session_id, role, text):
    d = _user_dir(user_key)
    fpath = os.path.join(d, 'sessions', f'{session_id}.json')
    msgs = []
    if os.path.exists(fpath):
        try:
            with open(fpath, 'r') as f:
                msgs = json.load(f)
        except Exception:
            msgs = []
    msgs.append({'role': role, 'text': text, 'ts': time.time()})
    with open(fpath, 'w') as f:
        json.dump(msgs, f, ensure_ascii=False)


def list_sessions(user_key):
    d = os.path.join(_user_dir(user_key), 'sessions')
    meta = _load_meta(user_key)
    sessions = []
    for fname in os.listdir(d):
        if not fname.endswith('.json'):
            continue
        fpath = os.path.join(d, fname)
        try:
            with open(fpath, 'r') as f:
                msgs = json.load(f)
            if not msgs:
                continue
            sid = fname[:-5]
            first_user = next((m['text'] for m in msgs if m['role'] == 'user'), '')
            sessions.append({
                'session_id': sid,
                'name': meta.get(sid, {}).get('name', ''),
                'preview': first_user[:60],
                'msg_count': len(msgs),
                'last_ts': msgs[-1].get('ts', 0),
            })
        except Exception:
            continue
    sessions.sort(key=lambda s: s['last_ts'], reverse=True)
    return sessions


def load_session(user_key, session_id):
    fpath = os.path.join(_user_dir(user_key), 'sessions', f'{session_id}.json')
    if not os.path.exists(fpath):
        return []
    try:
        with open(fpath, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def rename_session(user_key, session_id, name):
    meta = _load_meta(user_key)
    if session_id not in meta:
        meta[session_id] = {}
    meta[session_id]['name'] = name.strip()[:60]
    _save_meta(user_key, meta)


def reset_session(user_key):
    """重置会话，写入结束标记"""
    sess = _sessions.pop(user_key, None)
    if sess and sess.get('session_id'):
        _save_msg(user_key, sess['session_id'], 'system', '会话结束')


def handle_chat(handler):
    """流式代理本地 Claude Code CLI"""
    try:
        body = json.loads(handler._read_body(100 * 1024))
        message = body.get('message', '')
        resume_id = body.get('session_id', '')
        if not message:
            handler.send_json(400, {'error': 'message required'})
            return

        user = auth.get_session(handler) or 'anonymous'
        user_key = user if isinstance(user, str) else user.get('username', 'anonymous')
        now = time.time()
        sess = _sessions.get(user_key)
        timed_out = sess and now - sess['last_active'] > _IDLE_TIMEOUT
        if timed_out:
            sess = None
        if resume_id:
            session_id = resume_id
        else:
            session_id = sess['session_id'] if sess else None

        cmd = [
            CLAUDE_CLI['command'], '-p', message,
            '--output-format', 'stream-json', '--verbose',
            '--include-partial-messages',
            '--system-prompt', '你是 YICE 1.0 模型，由伊阁团队开发的营销数据助手。当用户问你是什么模型、什么AI时，回答"我是 YICE 1.0 模型"。用中文回复，简洁专业。回复中适当添加少许 emoji 增强情绪互动。',
        ]
        if session_id:
            cmd.extend(['--resume', session_id])

        env = dict(os.environ)
        env.pop('CLAUDECODE', None)

        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=env, cwd=PROJECT_ROOT,
        )

        handler.send_response(200)
        handler.send_header('Content-Type', 'text/event-stream; charset=utf-8')
        handler.send_header('Cache-Control', 'no-cache')
        handler.send_header('X-Accel-Buffering', 'no')
        handler.end_headers()

        def _sse(payload):
            handler.wfile.write(f'data: {payload}\n\n'.encode())
            handler.wfile.flush()

        if timed_out:
            _sse(json.dumps({'type': 'timeout'}, ensure_ascii=False))

        full_text = ''
        cur_sid = session_id or ''
        try:
            for raw in proc.stdout:
                line = raw.decode('utf-8').strip()
                if not line:
                    continue
                try:
                    evt = json.loads(line)
                except json.JSONDecodeError:
                    continue

                t = evt.get('type')
                if t == 'system' and evt.get('subtype') == 'init':
                    cur_sid = evt.get('session_id', '')
                    _sessions[user_key] = {'session_id': cur_sid, 'last_active': time.time()}
                    _sse(json.dumps({'type': 'init', 'session_id': cur_sid}, ensure_ascii=False))
                elif t == 'stream_event':
                    inner = evt.get('event', {})
                    if inner.get('type') == 'content_block_delta':
                        delta = inner.get('delta', {})
                        dt = delta.get('type')
                        if dt == 'text_delta':
                            txt = delta.get('text', '')
                            full_text += txt
                            _sse(json.dumps({'type': 'delta', 'text': txt}, ensure_ascii=False))
                        elif dt == 'thinking_delta':
                            _sse(json.dumps({'type': 'thinking', 'text': delta.get('thinking', '')}, ensure_ascii=False))
                elif t == 'result':
                    res_sid = evt.get('session_id', '')
                    if res_sid:
                        cur_sid = res_sid
                        _sessions[user_key] = {'session_id': cur_sid, 'last_active': time.time()}
                    _sse(json.dumps({
                        'type': 'done',
                        'session_id': cur_sid,
                        'cost_usd': evt.get('total_cost_usd', 0),
                        'is_error': evt.get('is_error', False),
                    }, ensure_ascii=False))
            _sse('[DONE]')
        except BrokenPipeError:
            proc.kill()
        finally:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

        if cur_sid:
            _save_msg(user_key, cur_sid, 'user', message)
            if full_text:
                _save_msg(user_key, cur_sid, 'bot', full_text)
    except Exception as e:
        try:
            handler.send_json(500, {'error': str(e)})
        except Exception:
            pass


def handle_upload(handler):
    """接收上传文件，存到临时目录，返回路径供 Claude 读取"""
    import base64 as b64
    try:
        body = json.loads(handler._read_body(10 * 1024 * 1024))
        name = body.get('name', 'file')
        data = body.get('data', '')
        if not data:
            handler.send_json(400, {'error': 'data required'})
            return
        if ',' in data:
            data = data.split(',', 1)[1]
        raw = b64.b64decode(data)
        os.makedirs(_UPLOAD_DIR, exist_ok=True)
        safe_name = re.sub(r'[^\w.\-]', '_', name)
        fpath = os.path.join(_UPLOAD_DIR, f'{int(time.time())}_{safe_name}')
        with open(fpath, 'wb') as f:
            f.write(raw)
        handler.send_json(200, {'path': fpath})
    except Exception as e:
        handler.send_json(500, {'error': str(e)})


def handle_asr(handler):
    """火山引擎豆包语音识别"""
    import base64 as b64
    import ssl
    import struct
    import uuid
    try:
        import websocket
    except ImportError:
        handler.send_json(500, {'error': 'pip install websocket-client'})
        return
    try:
        body = json.loads(handler._read_body(10 * 1024 * 1024))
        audio_b64 = body.get('audio', '')
        if not audio_b64:
            handler.send_json(400, {'error': 'audio required'})
            return
        pcm_data = b64.b64decode(audio_b64)
        print(f'  [ASR] PCM: {len(pcm_data)} bytes ({len(pcm_data)/32000:.1f}s)', flush=True)
        if not VOLC_ASR.get('access_token'):
            handler.send_json(500, {'error': 'VOLC_ASR_ACCESS_TOKEN 未配置'})
            return

        connect_id = str(uuid.uuid4())
        ws = websocket.create_connection(
            VOLC_ASR['ws_url'],
            header={
                'X-Api-App-Key': VOLC_ASR['app_id'],
                'X-Api-Access-Key': VOLC_ASR['access_token'],
                'X-Api-Resource-Id': 'volc.bigasr.sauc.duration',
                'X-Api-Connect-Id': connect_id,
            },
            sslopt={'cert_reqs': ssl.CERT_NONE},
            timeout=15,
        )

        def _pack(msg_type, flags, serial, payload):
            header = bytes([0x11, (msg_type << 4) | flags, (serial << 4), 0x00])
            size = struct.pack('>I', len(payload))
            return header + size + payload

        config = json.dumps({
            'user': {'uid': VOLC_ASR.get('uid', 'yice')},
            'audio': {'format': 'pcm', 'rate': 16000, 'bits': 16, 'channel': 1, 'codec': 'raw'},
            'request': {'model_name': 'bigmodel', 'language': 'zh-CN', 'enable_punc': True, 'enable_itn': True},
        }).encode()
        ws.send(_pack(0x1, 0x0, 0x1, config), opcode=0x2)

        chunk_size = 3200
        for i in range(0, len(pcm_data), chunk_size):
            chunk = pcm_data[i:i + chunk_size]
            ws.send(_pack(0x2, 0x0, 0x0, chunk), opcode=0x2)

        ws.send(_pack(0x2, 0x2, 0x0, b''), opcode=0x2)

        final_text = ''
        while True:
            try:
                resp = ws.recv()
                if not resp or len(resp) < 12:
                    break
                serial = (resp[2] >> 4) & 0xf
                payload_size = struct.unpack('>I', resp[8:12])[0]
                if payload_size == 0:
                    continue
                payload = resp[12:12 + payload_size]
                print(f'  [ASR] frame: serial={serial} payload_size={payload_size}', flush=True)
                if serial == 1:
                    data = json.loads(payload)
                    print(f'  [ASR] data: {json.dumps(data, ensure_ascii=False)[:200]}', flush=True)
                    result = data.get('result', {})
                    text = result.get('text', '') if isinstance(result, dict) else ''
                    if text:
                        final_text = text
                    if data.get('is_final'):
                        break
            except Exception as ex:
                print(f'  [ASR] recv error: {ex}', flush=True)
                break
        ws.close()
        print(f'  [ASR] raw: "{final_text}"', flush=True)

        # 清理口语化表达，结构化语音输入
        if final_text:
            import re as _re
            # 去掉语气词
            cleaned = _re.sub(r'[嗯啊呃额哦哈嘛呢吧了呀哎唉emmm]+[，、。\s]*', '', final_text)
            # 去掉首尾标点和空白
            cleaned = _re.sub(r'^[，。、\s]+|[，\s]+$', '', cleaned)
            if cleaned:
                final_text = cleaned
        print(f'  [ASR] final: "{final_text}"', flush=True)
        handler.send_json(200, {'text': final_text})
    except Exception as e:
        handler.send_json(500, {'error': str(e)})
