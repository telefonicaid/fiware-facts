__author__ = 'fla'

from flask import Flask

app = Flask(__name__)

import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

@app.route('/<tenantId>/servers/<serverId>')
def hello_world(tenantId, serverId):
    import time;
    return 'Hello World, tenantId: {}     serverId: {}!!!'.format(tenantId, serverId)


if __name__ == '__main__':
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
