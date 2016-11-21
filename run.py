from app import app
import os
import logging

port = int(os.environ.get('PORT', 5000))
logging.basicConfig(filename='/var/www/html/Alfred-WebApp/flask_error.log', level=logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)


