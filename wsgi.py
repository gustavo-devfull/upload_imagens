#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI entry point for Render deployment
"""

import os
from app_simple_render import app

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
