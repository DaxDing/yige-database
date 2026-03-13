"""缓存管理"""

import gzip as gzip_mod
import json
import threading
import time

from settings import CACHE

_store = {}
_lock = threading.Lock()


def get(key):
    with _lock:
        entry = _store.get(key)
        if entry and time.time() - entry['ts'] < CACHE['ttl']:
            return entry['data']
    return None


def get_bytes(key, accept_gzip=False):
    """返回预序列化 bytes，跳过 json.dumps"""
    with _lock:
        entry = _store.get(key)
        if entry and time.time() - entry['ts'] < CACHE['ttl']:
            if accept_gzip and entry.get('gz'):
                return entry['gz'], True
            return entry.get('jb'), False
    return None, False


def put(key, data):
    jb = json.dumps(data, ensure_ascii=False).encode('utf-8')
    gz = gzip_mod.compress(jb, compresslevel=1) if len(jb) > 1024 else None
    with _lock:
        if len(_store) >= CACHE['max_entries']:
            oldest = min(_store, key=lambda k: _store[k]['ts'])
            del _store[oldest]
        _store[key] = {'ts': time.time(), 'data': data, 'jb': jb, 'gz': gz}


def clear():
    with _lock:
        _store.clear()
