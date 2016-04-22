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

__description__ = 'Facts Listener'
__author__ = 'fla'

from flask import Flask, request, Response, json
from facts.myredis import myredis
from facts.queue import myqueue
from facts.jsoncheck import jsoncheck
from gevent.pywsgi import WSGIServer
from keystoneclient.exceptions import NotFound
from facts.config import fact_attributes, __version__
from facts import cloto_db_client
from facts.constants import CONTENT_HEADER, JSON_TYPE, REMOTE_ADDR, REMOTE_PORT, CONTEXT_ATTRIBUTES, \
    CONTEXT_RESPONSES, CONTEXT_ATTRIBUTES_NAME, CONTEXT_ATTRIBUTES_VALUE, CONTEXT_ELEMENT
import logging.config
import sys
import datetime
import gevent.monkey
import os
import httplib
import gevent

__version_info__ = tuple([int(num) for num in __version__.split('.')])


gevent.monkey.patch_all()

content_type = JSON_TYPE

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
Initialize the mysql connection library
"""

myClotoDBClient = cloto_db_client.cloto_db_client()

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
    if request.headers[CONTENT_HEADER] == content_type:
        try:
            # Ensure that received data is a valid JSON
            user_submission = json.loads(request.data)  # @UnusedVariable
        except ValueError:
            # Data is not a well-formed json
            message = "[{}] received {} from ip {}:{}"\
                .format("-", json, request.environ[REMOTE_ADDR], request.environ[REMOTE_PORT])

            logging.warning(message)

            return Response(response="{\"error\":\"Bad request. The payload is not well-defined json format\"}\n",
                            status=httplib.BAD_REQUEST,
                            content_type=content_type)

        # It is a valid payload and we start to process it
        try:
            result = process_request(request, tenantid, serverid)
        except NotFound as ex:
            return Response(response=ex.message, status=ex.http_status, content_type=content_type)
        except UnboundLocalError as ex:
            return Response(response="{\"error\":\"Some attribute is missing: " + ex.message + "\"}\n",
                            status=httplib.BAD_REQUEST, content_type=content_type)
        except ValueError as ex:
            return Response(response="{\"error\":\""+ ex.message + "\"}\n",
                            status=httplib.BAD_REQUEST, content_type=content_type)
        except Exception as ex:
            return Response(response="{\"error\": \"" + ex.message + "\"}\n",
                            status=httplib.BAD_REQUEST, content_type=content_type)

        if result == True:
            return Response(status=httplib.OK)
        else:
            return Response(response="{\"error\":\"Internal Server Error. "
                                     "Unable to contact with RabbitMQ process\"}\n",
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
    if request.remote_addr:
        message = "[{}] received {} from ip {}:{}"\
            .format("-", json, request.environ[REMOTE_ADDR], request.environ[REMOTE_PORT])
    else:
        message = "[{}] received {} from test client"\
            .format("-", json)
    logging.info(message)

    key = ['contextResponses', 'contextElement', 'attributes']

    # Check that it contains the previous keys
    try:
        jsoncheck.checkit(json, key, 0)
    except NotFound as err:
        logging.error(err)
        raise err

    # Extract the list of attributes from the NGSI message
    attrlist = request.json[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_ATTRIBUTES]

    data = list()

    for item in attrlist:
        name = item[CONTEXT_ATTRIBUTES_NAME]
        value = item[CONTEXT_ATTRIBUTES_VALUE]

        # Obtain the information of used memory and cpu
        if name == 'usedMemPct':
            verify_values(name, value)
            mem = float(value)
        elif name == 'cpuLoadPct':
            verify_values(name, value)
            cpu = float(value)
        elif name == 'netLoadPct':
            verify_values(name, value)
            net = float(value)
        elif name == 'freeSpacePct':
            verify_values(name, value)
            hdd = float(value)

    data.insert(len(data), cpu)
    data.insert(len(data), mem)
    data.insert(len(data), hdd)
    data.insert(len(data), net)

    # fix the first value of the list with the server identity
    data.insert(0, str(serverid))

    # fix the last value with the current date and time
    data.insert(len(fact_attributes) - 1, datetime.datetime.today().isoformat())

    # Check data coherency of time stamps
    # +1 is needed because the fact is not already added to the queue.
    # It checks that queue will have at least 2 facts.
    if len(mredis.range(tenantid, serverid)) + 1 >= 2:
        mredis.check_time_stamps(tenantid, serverid, mredis.range(tenantid, serverid), data)

    # Get the windowsize for the tenant from a redis queue
    windowsize = mredis.get_windowsize(tenantid)
    if windowsize == []:
        windowsize = myClotoDBClient.get_window_size(tenantid)
        mredis.insert_window_size(tenantid, windowsize)

     # Insert the result into the queue system
    mredis.insert(tenantid, serverid, data)
    logging.info(data)

    # If the queue has the number of facts defined by the windows size, it returns the
    # last window-size values (range) and calculates the media of them (in terms of memory and cpu)
    lo = mredis.media(mredis.range(tenantid, serverid), windowsize)

    # If the number of facts is lt window size, the previous operation returns a null lists
    if len(lo) != 0:
        try:
            rabbit = myqueue()
            if len(lo) == 1:
                lo.data = lo.data[0]
            message = "{\"serverId\": \"%s\", \"cpu\": %s, \"mem\": %s, \"hdd\": %s, \"net\": %s, \"time\": \"%s\"}" \
                      % (lo.data[0][1:-1], lo.data[1], lo.data[2], lo.data[3], lo.data[4], lo.data[5])

            logging_message = "[{}] sending message {}".format("-", message)

            logging.info(logging_message)

            # Send the message to the RabbitMQ components.
            result = rabbit.publish_message(tenantid, message)  # @UnusedVariable

        except Exception as ex:
            raise ex

    return True


def verify_values(name, value):
        """Checks if rule operands are expected strings and values are valid floats

        :param str name:        The name
        :param str value:       The value
        """

        myfloat = float(value)
        if myfloat < 0.0 or myfloat > 100.0:
            raise ValueError("Invalid value received for %s" % name)


def info(port):
    """Show some information about the execution of the process.
    """

    data = config.get('common', 'name')
    pid = os.getpid()

    logging.info("{} {}\n".format(data, __version__))
    logging.info("Running in stand alone mode")
    logging.info("Port: {}".format(port))
    logging.info("PID: {}\n".format(pid))
    logging.info("https://github.com/telefonicaid/fiware-facts\n\n\n")


def check_config_file():
    """Checks if configuration has mysql user with a user. If user parameter is empty, shows an error
    providing information about how to provide a valid settings file.
    The original Settings file could be found in facts_conf and it could be copied to the required folder.
    """
    if config.get('mysql', 'user') == '':
        logging.error("Cloto's Mysql data is empty. You should provide this information in the configuration file")
        logging.error("Please create a configuration file and add cloto MySql data to %s",
                      config.get('common', 'cfg_file_path'))
        logging.error("You can provide a Settings file in other locations using an environment variable called"
                      " FACTS_SETTINGS_FILE")

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
check_config_file()


def windowsize_updater():
    try:
        import pika
        connection = None
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=config.get('common', 'rabbitMQ')))
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
                logging.info("received windowsize: %s" % body)
                tenantid = body.split(" ")[0]
                windowsize = body.split(" ")[1]
                mredis.insert_window_size(tenantid, int(windowsize))

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
        if connection == None:
            logging.error("There is no connection with RabbitMQ. Please, check if it is alive")
        else:
            connection.close()

gevent.spawn(windowsize_updater)


def start_server():
    http.serve_forever()

if __name__ == '__main__':
    start_server()
