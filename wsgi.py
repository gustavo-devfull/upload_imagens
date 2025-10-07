#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI entry point for Render deployment
"""

from app_render import app

if __name__ == "__main__":
    app.run()
