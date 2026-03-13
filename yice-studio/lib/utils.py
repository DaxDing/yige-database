"""通用工具函数"""

import json
import os
import re
from datetime import datetime
from decimal import Decimal

from settings import CONFIG_DIR

_DS_RE = re.compile(r'^\d{8}$')


def serialize(val):
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    return val


def validate_ds(ds):
    if not _DS_RE.match(ds):
        raise ValueError(f'日期格式错误: {ds}，需要 YYYYMMDD')


def read_config(name):
    path = os.path.join(CONFIG_DIR, name)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_config(name, data):
    path = os.path.join(CONFIG_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
