# -*- coding: utf-8 -*-
#
# Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U
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

__author__ = "@jframos"

import behave
from behave import step
from hamcrest import assert_that, has_entries, has_length
from fiwarefacts_client.window_size_model_utils import get_window_size_rabbitmq_message
import json
from commons.custom_asserts import is_message_in_consumer_list
from qautils.dataset.dataset_utils import DatasetUtils

_dataset_utils = DatasetUtils()
behave.use_step_matcher("re")


def _assert_that_message_in_consumer_list(consumer_list, expected_message):
    """
    This method checks if the expected message is in the RAW consumer list.
    :param consumer_list (list): List of messages retrieved from RabbitMQ consumer.
        Format: [{'id': 'message_id_as_string', 'body': 'body_message_as_string'}, ...]
    :param expected_message (dict): Expected body message as DICT
    :return: None
    """

    found = False
    for message in consumer_list:
        body_model = json.loads(message['body'])

        if body_model == expected_message:
            found = True
            break

    assert_that(found,
                "A message with the expected content has not been received by RabbitMQ consumer. "
                "Expected content: %s; RabbitMQ consumer list content: %s",
                expected_message, consumer_list)


@step(u'RabbitMQ consumer is looking into the configured message bus')
def init_rabbitmq_consumer(context):

    print("> Initiating RabbitMQ consumer")
    context.rabbitmq_consumer.routing_key = context.tenant_id
    context.rabbitmq_consumer.run_as_thread()


@step(u'no messages have been received by RabbitMQ consumer')
def no_messages_received(context):

    assert_that(context.rabbitmq_consumer.message_list, has_length(0),
                "RabbitMQ consumer has retrieved messages from the bus, and it should NOT")

@step(u'"(?P<number_of_notifications>.*)" notification is sent to RabbitMQ')
@step(u'"(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ')
def notifications_are_received(context, number_of_notifications):

    assert_that(context.rabbitmq_consumer.message_list, has_length(int(number_of_notifications)),
                "RabbitMQ consumer has NOT retrieved the expected number of messages from the bus")


@step(u'the message sent to RabbitMQ has got the following monitoring attributes')
@step(u'the messages sent to RabbitMQ have got the following monitoring attributes')
def following_message_are_sent(context):

    for element in context.table.rows:
        expected_message = dict(element.as_dict())
        expected_message = _dataset_utils.prepare_data(expected_message)

        assert_that(expected_message, is_message_in_consumer_list(context.rabbitmq_consumer.message_list),
                    "A message with the expected content has not been received by RabbitMQ consumer")


@step(u'window size is set to "(?P<window_size>.*)"')
def window_size_is_set(context, window_size):

    message = get_window_size_rabbitmq_message(context.tenant_id, window_size)
    context.rabbitmq_publisher.send_message(message)
