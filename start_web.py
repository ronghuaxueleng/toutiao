# -*- coding: utf-8 -*
from flask import Flask

from app import app
from liblibart.tasks import liblibTasks

if __name__ == '__main__':
    liblibTasks.init().start()
    app.run(host='0.0.0.0', threaded=True, debug=False)
