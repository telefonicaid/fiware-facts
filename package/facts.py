__author__ = 'fla'

from flask import Flask, request, abort
from package.myredis import myredis
from package.mylist import mylist

import datetime

app = Flask(__name__)
mredis = myredis()

import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

# need to send {'serverId': 'serverId', 'cpu': 80, 'mem': 80, 'time': '2014-03-24 16:21:29.384631'}
# to the topic


@app.route('/<tenantid>/servers/<serverid>', methods=['POST'])
def hello_world(tenantid, serverid):
    if not request.json:
        abort(400)

    # Get the parsed contents of the form data
    json = request.json

    attrlist = request.json['contextResponses'][0]['contextElement']['attributes']

    data = list()

    for item in attrlist:
        name = item['name']
        value = item['contextValue']

        if name == 'usedMemPct' or name == 'cpuLoadPct':
            data.insert(len(data), float(value))

    data.insert(0, serverid)
    data.insert(3, datetime.datetime.today().isoformat())

    data[0] = str(data[0])

    mredis.insert(data)

    lo = mredis.media(mredis.range())

    print "media: ",lo.data

    return 'Hello World, tenantId: {}     serverId: {}    json: {}!!!'.format(tenantid, serverid, attrlist)


if __name__ == '__main__':
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
