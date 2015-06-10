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
__author__ = 'fla'

from config import config
from pika import exceptions
import pika
import logging
import time

"""Class to notify the facts to the RabbitMQ queue to be taken afterwards
by the cloto component.
"""


class myqueue(object):

    def __init__(self):
        """ Initialize the class and create a connection with a RabbitMQ server instance.
        """
        # Get the default IP address of the RabbitMQ server.
        rabbitmq = config.get('common', 'rabbitMQ')
        self.connection = None
        self.channel = None

        # Open a remote connection to RabbitMQ on specified IP address
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=rabbitmq))

            # Open the channel
            self.channel = self.connection.channel()
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError), error:
            logging.error('Exception while connecting to Rabbit %s' % error)
            raise Exception("Error with Rabbit connection")

    def publish_message(self, tenantid, message):
        """Publish a message related to a tenantid in the rabbitmq and
        close the connection

        :param str tenantid:      The id of the tenant
        :param str message:       The well-formatted message to send
        """
        if self.channel:
            self.channel.exchange_declare(exchange="facts",
                                 exchange_type='direct')

            try:
                # Send a message
                self.channel.basic_publish(exchange="facts",
                                           routing_key=tenantid,
                                           body=message)

                logging_message = "[{}] Sent message to RabbitMQ".format("-")

                logging.info(logging_message)
            except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError), error:
                logging.error('AMQP Connection failed. Trying again... %s' % error)
                raise Exception("AMQP Connection failed.")
        else:
            logging.error('AMQP channel not properly created...')
            raise Exception("AMQP channel not properly created...")

        if self.connection and self.connection.is_open:
            # Close the connection
            self.connection.close()
        else:
            logging.error('AMQP connection not properly created...')

            raise Exception("AMQP connection not properly created...")
