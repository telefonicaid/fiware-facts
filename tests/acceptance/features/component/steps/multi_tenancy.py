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
from hamcrest import assert_that, equal_to, is_, has_length

from commons.rabbit_utils import RabbitMQConsumer
import qautils.configuration.configuration_utils as configuration_utils
from fiwarefacts_client.window_size_model_utils import get_window_size_rabbitmq_message
from fiwarecloto_client.client import ClotoClient
from qautils.configuration.configuration_properties import PROPERTIES_CONFIG_SERVICE_PORT, \
    PROPERTIES_CONFIG_SERVICE_HOST, PROPERTIES_CONFIG_SERVICE_USER, PROPERTIES_CONFIG_SERVICE_PASSWORD
from commons.constants import PROPERTIES_CONFIG_RABBITMQ_SERVICE, PROPERTIES_CONFIG_RABBITMQ_SERVICE_FACTS_MESSAGES, \
    PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_NAME, PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_TYPE, \
    PROPERTIES_CONFIG_FACTS_SERVICE, PROPERTIES_CONFIG_FACTS_SERVICE_OS_SECONDARY_TENANT_ID, \
    FACTS_DEFAULT_WINDOW_SIZE, PROPERTIES_CONFIG_CLOTO_SERVICE
from qautils.configuration.configuration_properties import PROPERTIES_CONFIG_SERVICE_OS_USERNAME, \
    PROPERTIES_CONFIG_SERVICE_OS_PASSWORD, PROPERTIES_CONFIG_SERVICE_RESOURCE, \
    PROPERTIES_CONFIG_SERVICE_OS_AUTH_URL, PROPERTIES_CONFIG_SERVICE_PROTOCOL

from commons.step_helpers import send_context_notification_step_helper
from qautils.dataset.dataset_utils import DatasetUtils
from commons.custom_asserts import is_message_in_consumer_list

behave.use_step_matcher("re")
_dataset_utils = DatasetUtils()


@step(u'the secondary tenant-id configured is registered in CLOTO component')
def given_tenant_id_is_registered_in_cloto(context):

    context.secondary_tenant_id = \
        configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_FACTS_SERVICE_OS_SECONDARY_TENANT_ID]

    print ("> Initiating Cloto REST Client for the secondary Tenant")
    context.secondary_cloto_client = ClotoClient(
        username=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_USERNAME],
        password=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_PASSWORD],
        tenant_id=context.secondary_tenant_id,
        auth_url=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_AUTH_URL],
        api_protocol=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_PROTOCOL],
        api_host=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_HOST],
        api_port=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_PORT],
        api_resource=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_RESOURCE])

    print ("> A GET request is executed to CLOTO component, "
           "to init all data about that secondary tenant in its system.")
    _, response = context.secondary_cloto_client.\
        get_tenant_id_resource_client().get_tenant_id(context.secondary_tenant_id)

    assert_that(response.ok,
                "TenantId '{}' for testing cannot be "
                "retrieved from CLOTO: Message: {}".format(context.secondary_tenant_id, response.text))



@step(u'the following notifications are received for "(?P<server_id>.*)" and secondary tenant-id with values')
@step(u'a context notification is received for "(?P<server_id>.*)" and secondary tenant-id with values')
def a_context_update_is_received_for_secondary_tenant(context, server_id):

    send_context_notification_step_helper(context, context.secondary_tenant_id, server_id)


@step(u'a new secondary RabbitMQ consumer is looking into the configured message bus')
def new_secondaty_consumer_looking_for_messages(context):

    # Init RabbitMQ consumer
    context.secondaty_rabbitmq_consumer = RabbitMQConsumer(
        amqp_host=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_HOST],
        amqp_port=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_PORT],
        amqp_user=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_USER],
        amqp_password=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_PASSWORD])

    facts_message_config = \
        configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_RABBITMQ_SERVICE_FACTS_MESSAGES]

    context.secondaty_rabbitmq_consumer.exchange = \
        facts_message_config[PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_NAME]

    context.secondaty_rabbitmq_consumer.exchange_type = \
        facts_message_config[PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_TYPE]

    # Append consumer to the 'context' consumer list
    context.rabbitmq_consumer_list.append(context.secondaty_rabbitmq_consumer)

    # Set default window size to 2 (FACTS) - Secondary Tenant
    message = get_window_size_rabbitmq_message(context.secondary_tenant_id, FACTS_DEFAULT_WINDOW_SIZE)
    context.rabbitmq_publisher.send_message(message)

    # Run secondary consumer
    context.secondaty_rabbitmq_consumer.routing_key = context.secondary_tenant_id
    context.secondaty_rabbitmq_consumer.run_as_thread()


@step(u'the message sent to RabbitMQ with the secondary tenant has got the following monitoring attributes')
@step(u'the messages sent to RabbitMQ with the secondary tenant have got the following monitoring attributes')
def following_messages_are_sent_to_secondary_consumer(context):

    for element in context.table.rows:
        expected_message = dict(element.as_dict())
        expected_message = _dataset_utils.prepare_data(expected_message)

        assert_that(expected_message, is_message_in_consumer_list(context.secondaty_rabbitmq_consumer.message_list),
                    "A message with the expected content has not been received by the secondary RabbitMQ consumer")


@step(u'no messages have been received by the secondary RabbitMQ consumer')
def no_messages_received_for_secondary_tenant(context):
    print ("> Received main list: " + str(context.secondaty_rabbitmq_consumer.message_list))
    print ("> Received seconday list: " + str(context.rabbitmq_consumer.message_list))
    assert_that(context.secondaty_rabbitmq_consumer.message_list, has_length(0),
                "Secondary RabbitMQ consumer has retrieved messages from the bus, and it should NOT")


@step(u'"(?P<number_of_notifications>.*)" notification is sent to RabbitMQ with the secondary tenant')
@step(u'"(?P<number_of_notifications>.*)" notifications are sent to RabbitMQ with the secondary tenant')
def notifications_are_received_by_secondary_consumer(context, number_of_notifications):

    assert_that(context.secondaty_rabbitmq_consumer.message_list, has_length(int(number_of_notifications)),
                "Secondary RabbitMQ consumer has NOT retrieved the expected number of messages from the bus")


@step(u'window size is set to "(?P<window_size>.*)" for the secondary tenant')
def window_size_is_set(context, window_size):

    message = get_window_size_rabbitmq_message(context.secondary_tenant_id, window_size)
    context.rabbitmq_publisher.send_message(message)
