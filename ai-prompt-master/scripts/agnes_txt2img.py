#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向后兼容包装器 — 委托给 agnes_image.py (纯文生图模式)。
"""
import sys
import os
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_new_script = _SCRIPT_DIR / "agnes_image.py"

if not _new_script.exists():
    print("Error: agnes_image.py not found in same directory", file=sys.stderr)
    sys.exit(1)

# 将所有参数透传给新脚本（不带 --image 即为纯文生图）
args = [str(_new_script)] + sys.argv[1:]
os.execv(sys.executable, [sys.executable] + args)
