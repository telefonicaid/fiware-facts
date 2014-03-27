__author__ = 'fla'

from flask import Flask, request, jsonify, abort
import datetime

app = Flask(__name__)

import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

# need to send {'serverId': 'serverId', 'cpu': 80, 'mem': 80, 'time': '2014-03-24 16:21:29.384631'}
# to the topic
@app.route('/<tenantId>/servers/<serverId>', methods=['POST'])
def hello_world(tenantId, serverId):
    if not request.json:
        abort(400)

    # Get the parsed contents of the form data
    json = request.json
    print(json)

    attrlist = request.json['contextResponses'][0]['contextElement']['attributes']

    print(len(attrlist))

    time = datetime.datetime.today()

    print(time)

    return 'Hello World, tenantId: {}     serverId: {}    json: {}!!!'.format(tenantId, serverId, attrlist)





if __name__ == '__main__':
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
