# -*- coding: utf-8 -*-
#
# Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is parpt of FI-WARE project.
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

__author__ = "@jframos"


from qautils.logger.logger_utils import get_logger
from qautils.configuration.configuration_utils import set_up_project
from fiwarefacts_client.client import FactsClient
from fiwarecloto_client.client import ClotoClient
from commons.rabbit_utils import RabbitMQConsumer, RabbitMQPublisher
import qautils.configuration.configuration_utils as configuration_utils
from fiwarefacts_client.window_size_model_utils import get_window_size_rabbitmq_message
from qautils.configuration.configuration_properties import PROPERTIES_CONFIG_SERVICE_PROTOCOL, \
    PROPERTIES_CONFIG_SERVICE_RESOURCE, PROPERTIES_CONFIG_SERVICE_PORT, PROPERTIES_CONFIG_SERVICE_HOST, \
    PROPERTIES_CONFIG_SERVICE_OS_USERNAME, PROPERTIES_CONFIG_SERVICE_OS_PASSWORD, \
    PROPERTIES_CONFIG_SERVICE_OS_TENANT_ID, PROPERTIES_CONFIG_SERVICE_OS_AUTH_URL, PROPERTIES_CONFIG_SERVICE_USER, \
    PROPERTIES_CONFIG_SERVICE_PASSWORD
from commons.constants import *  # All custom constants are used in this file.
import time


__logger__ = get_logger(__name__)


def before_all(context):

    __logger__.info("START ...")
    __logger__.info("Setting UP acceptance test project ")

    set_up_project()  # Load setting using 'qautils.configuration.configuration_utils'

    # Save tenantId
    context.tenant_id = \
        configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_TENANT_ID]

    # Create REST Clients
    context.facts_client = FactsClient(
        protocol=configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_PROTOCOL],
        host=configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_HOST],
        port=configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_PORT],
        resource=configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_RESOURCE])

    context.cloto_client = ClotoClient(
        username=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_USERNAME],
        password=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_PASSWORD],
        tenant_id=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_TENANT_ID],
        auth_url=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_AUTH_URL],
        api_protocol=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_PROTOCOL],
        api_host=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_HOST],
        api_port=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_PORT],
        api_resource=configuration_utils.config[PROPERTIES_CONFIG_CLOTO_SERVICE][PROPERTIES_CONFIG_SERVICE_RESOURCE])


def before_feature(context, feature):

    __logger__.info("=========== START FEATURE =========== ")
    __logger__.info("Feature name: %s", feature.name)


def before_scenario(context, scenario):

    __logger__.info("********** START SCENARIO **********")
    __logger__.info("Scenario name: %s", scenario.name)

    # Clean scenario variables
    context.context_elements = dict()
    context.response = None

    # List of RabbitMQ Consumers for testing purposes. This list is necessary to be used as Multi-Tenancy test cases.
    # By default, this list only will have information for the main tenant used in test cases. Additional RabbitMQ
    # consumers should be added by each test case if they are needed.
    context.rabbitmq_consumer_list = list()

    # Init RabbitMQ consumer and append it on the list - Main tenantId
    context.rabbitmq_consumer = RabbitMQConsumer(
        amqp_host=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_HOST],
        amqp_port=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_PORT],
        amqp_user=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_USER],
        amqp_password=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_PASSWORD])

    facts_message_config = \
        configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_RABBITMQ_SERVICE_FACTS_MESSAGES]

    context.rabbitmq_consumer.exchange = \
        facts_message_config[PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_NAME]

    context.rabbitmq_consumer.exchange_type = \
        facts_message_config[PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_TYPE]

    context.rabbitmq_consumer_list.append(context.rabbitmq_consumer)

    # Init RabbitMQ publisher
    context.rabbitmq_publisher = RabbitMQPublisher(
        amqp_host=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_HOST],
        amqp_port=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_PORT],
        amqp_user=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_USER],
        amqp_password=configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_SERVICE_PASSWORD])

    facts_window_size_config = \
        configuration_utils.config[PROPERTIES_CONFIG_RABBITMQ_SERVICE][PROPERTIES_CONFIG_RABBITMQ_SERVICE_WINDOW_SIZE]

    context.rabbitmq_publisher.exchange = \
        facts_window_size_config[PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_NAME]

    context.rabbitmq_publisher.routing_key = \
        facts_window_size_config[PROPERTIES_CONFIG_RABBITMQ_SERVICE_ROUTING_KEY]

    # Set default window size to 2 (FACTS), for the main tenantId configured
    message = get_window_size_rabbitmq_message(context.tenant_id, FACTS_DEFAULT_WINDOW_SIZE)
    context.rabbitmq_publisher.send_message(message)


def after_scenario(context, scenario):

    __logger__.info("********** END SCENARIO **********")

    # Close all RabbitMQ consumers (if initiated)
    for consumer in context.rabbitmq_consumer_list:
        consumer.stop()
        consumer.close_connection()

    # Close RabbitMQ publisher (if initiated)
    context.rabbitmq_publisher.close()

    # Wait for grace period defined (FACTS component) to delete all stored facts.
    grace_period = \
        configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_FACTS_SERVICE_GRACE_PERIOD]

    __logger__.info("Explicit wait for FACTS grace period: %d seconds", grace_period)
    time.sleep(grace_period)


def after_feature(context, feature):

    __logger__.info("=========== END FEATURE =========== ")


def after_all(context):

    __logger__.info("... END  :)")
