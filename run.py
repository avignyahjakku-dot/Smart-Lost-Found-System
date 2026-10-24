"""
CampusFind - Application Entry Point
====================================
Smart Lost & Found System
Individual BTech CSE Capstone Project
"""

import os
from app import create_app

env_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(env_name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    print(f"🚀 Starting CampusFind on http://127.0.0.1:{port} (Debug={debug})")
    app.run(host='127.0.0.1', port=port, debug=debug)
