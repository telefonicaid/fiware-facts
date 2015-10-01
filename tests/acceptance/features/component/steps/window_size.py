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
from commons.custom_asserts import is_message_in_consumer_list
from qautils.dataset.dataset_utils import DatasetUtils
import time

_dataset_utils = DatasetUtils()
behave.use_step_matcher("re")


@step(u'RabbitMQ consumer is looking into the configured message bus')
def init_rabbitmq_consumer(context):

    print("> Initiating RabbitMQ consumer")

    context.rabbitmq_consumer.routing_key = context.tenant_id
    context.rabbitmq_consumer.run_as_thread()


@step(u'no messages have been received by RabbitMQ consumer')
@step(u'no messages have been received by the main RabbitMQ consumer')
def no_messages_received(context):

    assert_that(context.rabbitmq_consumer.message_list, has_length(0),
                "RabbitMQ consumer has retrieved messages from the bus, and it should NOT")

@step(u'"(?P<number_of_notifications>.*)" notification is sent to RabbitMQ')
@step(u'"(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ')
@step(u'"(?P<number_of_notifications>.*)" notification is sent to RabbitMQ with the main tenant')
@step(u'"(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ with the main tenant')
def notifications_are_received(context, number_of_notifications):

    assert_that(context.rabbitmq_consumer.message_list, has_length(int(number_of_notifications)),
                "RabbitMQ consumer has NOT retrieved the expected number of messages from the bus")


@step(u'the message sent to RabbitMQ has got the following monitoring attributes')
@step(u'the messages sent to RabbitMQ have got the following monitoring attributes')
@step(u'the message sent to RabbitMQ with the main tenant has got the following monitoring attributes')
@step(u'the messages sent to RabbitMQ with the main tenant have got the following monitoring attributes')
def following_messages_are_sent(context):

    for element in context.table.rows:
        expected_message = dict(element.as_dict())
        expected_message = _dataset_utils.prepare_data(expected_message)

        assert_that(expected_message, is_message_in_consumer_list(context.rabbitmq_consumer.message_list),
                    "A message with the expected content has not been received by RabbitMQ consumer")


@step(u'window size is set to "(?P<window_size>.*)"')
@step(u'window size is set to "(?P<window_size>.*)" for the main tenant')
def window_size_is_set(context, window_size):

    message = get_window_size_rabbitmq_message(context.tenant_id, window_size)
    context.rabbitmq_publisher.send_message(message)


@step(u'I wait "(?P<seconds>\d*)" seconds')
def explicit_wait(context, seconds):

    print ("> Explicit wait: %s seconds" % seconds)
    time.sleep(int(seconds))
