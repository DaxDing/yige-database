#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配置：路径 + HTTP"""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
OUT_DIR = PROJECT_ROOT / 'out' / 'xh_data'
TASKS_FILE = OUT_DIR / 'tasks.json'

# HTTP
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 18008
