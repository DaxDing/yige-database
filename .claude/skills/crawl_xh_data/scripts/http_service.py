#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP 服务：任务列表 + 接收浏览器采集结果 + 保存/合并 JSON (stdlib版)"""
import json
import sys
import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, str(Path(__file__).parent))
from config import HTTP_HOST, HTTP_PORT, OUT_DIR, TASKS_FILE, PROJECT_ROOT

PROGRESS_FILE = OUT_DIR / 'progress.json'
CRAWL_LOG = OUT_DIR / 'crawl.log'


# --- 进度管理 ---

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {'history': {}, 'today': '', 'completed': []}


def save_progress(progress):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False))


# --- 数据合并 ---

def merge_data(existing, new_data, dtype):
    if dtype.startswith('content_'):
        key_fn = lambda r: (r.get('contentId', ''), r.get('theDate', ''))
    else:
        key_fn = lambda r: r.get('theDate', '')
    lookup = {key_fn(r): r for r in existing}
    for r in new_data:
        lookup[key_fn(r)] = r
    merged = list(lookup.values())
    merged.sort(key=lambda r: r.get('theDate', ''))
    return merged


# --- 扫描已有数据 ---

def scan_data_dates():
    result = {}
    if not OUT_DIR.exists():
        return result
    for task_dir in OUT_DIR.iterdir():
        if not task_dir.is_dir():
            continue
        eid = task_dir.name
        dates = {}
        for dtype in ['event_15', 'event_30', 'content_15', 'content_30']:
            fp = task_dir / f'{dtype}.json'
            if not fp.exists():
                continue
            try:
                data = json.loads(fp.read_text())
                if isinstance(data, list) and data:
                    td = [r.get('theDate', '') for r in data if isinstance(r, dict)]
                    td = [d for d in td if d]
                    if td:
                        dates[dtype] = max(td)
            except Exception:
                pass
        if dates:
            result[eid] = dates
    return result


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress default logging

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]

        if path == '/health':
            self._send_json({'status': 'ok'})

        elif path == '/api/tasks':
            if not TASKS_FILE.exists():
                self._send_json({'code': 1, 'message': 'tasks.json not found'})
                return
            tasks = json.loads(TASKS_FILE.read_text())
            progress = load_progress()
            today = datetime.date.today().isoformat()
            if progress.get('today') != today:
                progress['today'] = today
                progress['completed'] = []
                save_progress(progress)
            self._send_json({
                'code': 0,
                'tasks': tasks,
                'completed': progress['completed'],
                'history': progress.get('history', {}),
                'data_dates': scan_data_dates()
            })

        elif path == '/api/progress':
            progress = load_progress()
            total = len(json.loads(TASKS_FILE.read_text())) if TASKS_FILE.exists() else 0
            self._send_json({
                'code': 0,
                'completed': progress['completed'],
                'done': len(progress['completed']),
                'total': total,
                'history': progress.get('history', {})
            })

        else:
            self._send_json({'code': 404, 'message': 'not found'}, 404)

    def do_POST(self):
        path = self.path.split('?')[0]

        if path == '/api/save':
            d = self._read_body()
            eid = d.get('eventId')
            dtype = d.get('type')
            payload = d.get('data')
            do_merge = d.get('merge', False)

            if not eid or not dtype or payload is None:
                self._send_json({'code': 1, 'message': 'missing eventId/type/data'})
                return

            event_dir = OUT_DIR / str(eid)
            event_dir.mkdir(parents=True, exist_ok=True)
            filepath = event_dir / f'{dtype}.json'

            if do_merge and isinstance(payload, list) and filepath.exists():
                existing = json.loads(filepath.read_text())
                if isinstance(existing, list):
                    old_len = len(existing)
                    payload = merge_data(existing, payload, dtype)
                    print(f"  [MERGE] {eid}/{dtype}.json ({old_len} + {len(payload) - old_len} new → {len(payload)})")
                else:
                    print(f"  [SAVE] {eid}/{dtype}.json (overwrite)")
            else:
                size = len(payload) if isinstance(payload, list) else 'obj'
                print(f"  [SAVE] {eid}/{dtype}.json ({size})")

            filepath.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
            self._send_json({'code': 0})

        elif path == '/api/complete':
            d = self._read_body()
            eid = d.get('eventId')
            if not eid:
                self._send_json({'code': 1, 'message': 'missing eventId'})
                return

            progress = load_progress()
            today = datetime.date.today().isoformat()

            if eid not in progress['completed']:
                progress['completed'].append(eid)

            history = progress.get('history', {})
            history[str(eid)] = {'last_crawl': today}
            progress['history'] = history
            save_progress(progress)

            total = len(json.loads(TASKS_FILE.read_text())) if TASKS_FILE.exists() else 0
            done = len(progress['completed'])
            print(f"  [DONE] {eid} ({done}/{total})")

            if done == total and total > 0:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(CRAWL_LOG, 'a') as f:
                    f.write(f"{now}  DONE     {done}/{total} tasks\n")

            self._send_json({'code': 0, 'done': done, 'total': total})

        elif path == '/api/reset':
            progress = load_progress()
            cleared = len(progress['completed'])
            progress['completed'] = []
            save_progress(progress)
            print(f"  [RESET] cleared {cleared} completed tasks")
            self._send_json({'code': 0, 'cleared': cleared})

        else:
            self._send_json({'code': 404, 'message': 'not found'}, 404)


if __name__ == '__main__':
    print(f"服务启动: http://{HTTP_HOST}:{HTTP_PORT}")
    server = HTTPServer((HTTP_HOST, HTTP_PORT), Handler)
    server.serve_forever()
