#!/usr/bin/env python3
import os
from app import create_app

if os.environ.get('VERCEL'):
    os.environ.setdefault('FLASK_ENV', 'production')

app = create_app(os.environ.get('FLASK_ENV', 'development'))
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
