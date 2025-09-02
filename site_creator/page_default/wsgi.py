#!/usr/bin/env python3
"""
WSGI entry point for Flask application
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flaskapp import app

if __name__ == "__main__":
    app.run()
