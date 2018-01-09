import os
from os import path, environ

from app import app

if __name__ == '__main__':
    debug = "DEBUG" in environ
    app.debug = debug

    # template auto-reload
    extra_dirs = ['./app/templates', ]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    app.run(host='0.0.0.0', port=app.config['PORT'], extra_files=extra_files)
