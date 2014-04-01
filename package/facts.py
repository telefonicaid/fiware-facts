__author__ = 'fla'

from flask import Flask, request, abort, Response, json
from package.myredis import myredis

import datetime
from package.log import logger

app = Flask(__name__)
mredis = myredis()

import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

# need to send {'serverId': 'serverId', 'cpu': 80, 'mem': 80, 'time': '2014-03-24 16:21:29.384631'}
# to the topic


@app.route('/v1.0/<tenantid>/servers/<serverid>', methods=['POST'])
def facts(tenantid, serverid):
    """API endpoint for submitting data to

    :return: status code 405 - invalid JSON or invalid request type
    :return: status code 400 - unsupported Content-Type or invalid publisher
    :return: status code 200 - successful submission
    """
    # Ensure post's Content-Type is supported
    if request.headers['content-type'] == 'application/json':
        # Ensure data is a valid JSON
        try:
            user_submission = json.loads(request.data)
        except ValueError:
            message = "[{}] received {} from ip {}:{}"\
                .format("-", json, request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'])

            logger.warning(message)


            return Response(response="{\"error\":\"The payload is not well-defined json format\"}",
                            status=405,
                            content_type="application/json")

        result = process_request(request, serverid)

        if result == True:
            return Response(status=200)
        else:
            return Response(status=405)

    # User submitted an unsupported Content-Type
    else:
        return Response(response="{\"error\":\"Bad request. Content-type is not application/json\"}",
                        status=400,
                        content_type="application/json")

def process_request(request, serverid):
    # Get the parsed contents of the form data
    json = request.json
    message = "[{}] received {} from ip {}:{}"\
        .format("-", json, request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'])

    logger.info(message)

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

    print "media: ", lo.data

    if len(lo) != 0:
        #message = "\{'serverId': {}, 'cpu': {}, 'mem': {}, 'time': {}\}".format(lo.data[0], lo.data[1], lo.data[2], lo.data[3])
        message = "{\"serverId\": \"%s\", \"cpu\": %d, \"mem\": %d, \"time\": \"%s\"}" % (lo.data[0], lo.data[1], lo.data[2], lo.data[3])
        print message

    return True

if __name__ == '__main__':
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
