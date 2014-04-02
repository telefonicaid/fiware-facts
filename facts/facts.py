#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
__version__         = '1.0.0'
__version_info__    = tuple([int(num) for num in __version__.split('.')])
__description__     = 'Facts Listener'
__author__ = 'fla'

from flask import Flask, request, Response, json
import logging.config
from ConfigParser import SafeConfigParser
import os.path
import sys
from myredis import myredis

import datetime

app = Flask(__name__)
mredis = myredis()

import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

"""Default configuration.

The configuration `cfg_defaults` can be superseded with that read from `cfg_filename` (at path `conf/<progname>.cfg`),
if file exists.
"""
name = os.path.splitext(os.path.basename(__file__))[0]
cfg_filename = os.path.join(os.path.dirname(__file__), 'conf', '%s.cfg' % name)
cfg_defaults = {
    'brokerPort':           5000,                      # Port of our facts broker
    'LOGGING_PATH':         'u"/var/log/facts/"',      # place where it puts the log file
    'retries':              2,                         # number of retries (exponential backoff)
    'factor':               2,                         # factor for exponential backoff
    'randomize':            False,                     # enable randomization for exponential backoff
    'minRetryTime':         1000,                      # minimum time for exponential backoff (millis)
    'maxRetryTime':         sys.maxint,                # maximum time for exponential backoff (millis)
    'logLevel':             'INFO',
    'logFormat':            '%(asctime)s %(levelname)s policymanager.facts %(message)s'
}


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

            logging.warning(message)


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

    logging.info(message)

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
    # process configuration file (if exists) and setup logging
    config = SafeConfigParser(cfg_defaults)
    config.add_section('common')
    for key, value in cfg_defaults.items(): config.set('common', key, str(value))
    if config.read(cfg_filename):
        logging.config.fileConfig(cfg_filename)
    else:
        logging.basicConfig(stream=sys.stdout, level=cfg_defaults['logLevel'], format=cfg_defaults['logFormat'])


    http = WSGIServer(('', int(config.get('common', 'brokerPort'))), app)
    http.serve_forever()
