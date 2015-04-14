#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
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

__version__ = '1.2.0'
__version_info__ = tuple([int(num) for num in __version__.split('.')])
__description__ = 'Facts Listener'
__author__ = 'fla'

from flask import Flask, request, Response, json
from facts.myredis import myredis
from facts.queue import myqueue
from facts.jsoncheck import jsoncheck
from gevent.pywsgi import WSGIServer
import logging.config
import sys
import datetime
import gevent.monkey
import os
import httplib


gevent.monkey.patch_all()

content_type = 'application/json'

from facts.config import config, cfg_filename, cfg_defaults

"""Flask server initialization.

Uses Redis server as a message queue and server exchange with the fiware-cloto.
"""
app = Flask(__name__)

"""
Initialize the redis connection library
"""
mredis = myredis()

"""
Initialize the pid of the process
"""
pid = 0

# Flask/Gevent server need to send {'serverId': 'serverId', 'cpu': 80, 'mem': 80, 'time': '2014-03-24 16:21:29.384631'}
# to the topic


@app.route('/v1.0', methods=['GET'])
def factsinfo():
    """API endpoint for receiving keep alive information
    """
    return Response(response="{\"fiware-facts\":\"Up and running...\"}\n",
                    status=httplib.OK,
                    content_type=content_type)


@app.route('/v1.0/<tenantid>/servers/<serverid>', methods=['POST'])
def facts(tenantid, serverid):
    """API endpoint for receiving data from Monitoring system

    :param string tenantid:    the id of the tenant
    :param string serverid:    the id of the monitored instance (server)

    :return: status code 405 - invalid JSON or invalid request type
    :return: status code 400 - unsupported Content-Type or invalid publisher
    :return: status code 200 - successful submission
    """
    # Ensure post's Content-Type is supported
    if request.headers['content-type'] == content_type:
        try:
            # Ensure that received data is a valid JSON
            user_submission = json.loads(request.data)  # @UnusedVariable
        except ValueError:
            # Data is not a well-formed json
            message = "[{}] received {} from ip {}:{}"\
                .format("-", json, request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'])

            logging.warning(message)

            return Response(response="{\"error\":\"Bad request. The payload is not well-defined json format\"}\n",
                            status=httplib.BAD_REQUEST,
                            content_type=content_type)

        # It is a valid payload and we start to process it
        result = process_request(request, tenantid, serverid)

        if result == True:
            return Response(status=httplib.OK)
        else:
            return Response(response="{\"error\":\"Internal Server Error. Unable to contact with RabbitMQ process\"}\n",
                            status=httplib.INTERNAL_SERVER_ERROR,
                            content_type=content_type)

    # User submitted an unsupported Content-Type (only is valid application/json)
    else:
        return Response(response="{\"error\":\"Bad request. Content-type is not application/json\"}\n",
                        status=httplib.BAD_REQUEST,
                        content_type=content_type)


def process_request(request, tenantid, serverid):
    """Get the parsed contents of the form data

    :param string request:     The information of the received request
    :param string serverid:    the id of the monitored instance (server)

    :return: True
    """
    json = request.json
    message = "[{}] received {} from ip {}:{}"\
        .format("-", json, request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'])

    logging.info(message)

    key = ['contextResponses', 'contextElement', 'attributes']

    # Check that it contains the previous keys
    try:
        jsoncheck.checkit(json, key, 0)
    except (Exception), err:
        logging.error(err)
        return Falsechmod

    # Extract the list of attributes from the NGSI message
    attrlist = request.json['contextResponses'][0]['contextElement']['attributes']

    data = list()

    for item in attrlist:
        name = item['name']
        value = item['contextValue']

        # Obtain the information of used memory and cpu
        if name == 'usedMemPct' or name == 'cpuLoadPct':
            data.insert(len(data), float(value))

    # fix the first value of the list with the server identity
    data.insert(0, str(serverid))

    # fix the last value with the current date and time
    data.insert(3, datetime.datetime.today().isoformat())

    # Check data coherency of time stamps
    if len(mredis.range(tenantid, serverid)) > 2:
        mredis.check_time_stamps(tenantid, serverid, mredis.range(tenantid, serverid), data)

    # Insert the result into the queue system
    mredis.insert(tenantid, serverid, data)
    logging.info(data)

    # Get the windowsize for the tenant from a redis queue
    windowsize = mredis.get_windowsize(tenantid)
    if windowsize is []:
        from facts import cloto_client
        windowsize = cloto_client.get_window_size(tenantid)
        mredis.insert_window_size(tenantid, windowsize)

    # If the queue has the number of facts defined by the windows size, it returns the
    # last window-size values (range) and calculates the media of them (in terms of memory and cpu)
    lo = mredis.media(mredis.range(tenantid, serverid), windowsize)

    # If the number of facts is lt window size, the previous operation returns a null lists
    if len(lo) != 0:
        try:
            rabbit = myqueue()

            message = "{\"serverId\": \"%s\", \"cpu\": %d, \"mem\": %d, \"time\": \"%s\"}" \
                      % (lo.data[0], lo.data[1], lo.data[2], lo.data[3])

            logging_message = "[{}] sending message {}".format("-", message)

            logging.info(logging_message)

            # Send the message to the RabbitMQ components.
            result = rabbit.publish_message(tenantid, message)  # @UnusedVariable

        except Exception:
            #logging.info(lo.get())
            return False

    return True


def info(port):
    """Show some information about the execution of the process.
    """

    data = config.get('common', 'name')
    pid = os.getpid()

    logging.info("{} {}\n".format(data, __version__))
    logging.info("Running in stand alone mode")
    logging.info("Port: {}".format(port))
    logging.info("PID: {}\n".format(pid))
    logging.info("https://github.hi.inet/telefonicaid/fiware-facts\n\n\n")


# process configuration file (if exists) and setup logging
if config.read(cfg_filename):
    logging.config.fileConfig(cfg_filename)
else:
    logging.basicConfig(stream=sys.stdout, level=cfg_defaults['logLevel'], format=cfg_defaults['logFormat'])

# Define the port of our server, by default 5000
port = config.getint('common', 'brokerPort')

# execute the flask server, WSGI server
http = WSGIServer(('', port), app)

# show general information about the execution of the process
info(port)


def windowsize_updater():
    try:
        import pika
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host="localhost"))
        channel = connection.channel()

        channel.exchange_declare(exchange="windowsizes",
                                 exchange_type='direct')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange="windowsizes",
                           queue=queue_name,
                           routing_key="windowsizes")

        logging.info('Waiting for windowsizes')

        def callback(ch, method, properties, body):
            try:
                logging.info("received fact: %s" % body)
                tenantid = body.split(" ")[0]
                windowsize = body.split(" ")[1]
                mredis.insert_window_size(tenantid, windowsize)

            except ValueError:
                logging.info("receiving an invalid body: " + body)

            except Exception as ex:
                logging.info("ERROR UPDATING WINDOWSIZE: " + ex.message)

        channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)

        channel.start_consuming()
    except Exception as ex:
        if ex.message:
            logging.error("Error %s:" % ex.message)
    finally:
        connection.close()

import gevent
gevent.spawn(windowsize_updater)
http.serve_forever()
