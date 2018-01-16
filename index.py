from os import environ

from app import app

if __name__ == '__main__':
    debug = "DEBUG" in environ
    app.debug = debug

    app.run(host='0.0.0.0', port=app.config['PORT'], threaded=True)
