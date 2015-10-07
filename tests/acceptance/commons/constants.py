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
#

__author__ = "@jframos"


# Custom config properties
# Common properties are defined in qautils lib: qautils.configuration.configuration_properties
PROPERTIES_CONFIG_FACTS_SERVICE = "facts_service"
PROPERTIES_CONFIG_CLOTO_SERVICE = "cloto_service"
PROPERTIES_CONFIG_RABBITMQ_SERVICE = "rabbitmq_service"

# FACTS attributes
PROPERTIES_CONFIG_FACTS_SERVICE_GRACE_PERIOD = "facts_grace_period"
PROPERTIES_CONFIG_FACTS_SERVICE_OS_SECONDARY_TENANT_ID = "os_secondary_tenant_id"


# RabbitMQ attributes
PROPERTIES_CONFIG_RABBITMQ_SERVICE_FACTS_MESSAGES = "facts_messages"
PROPERTIES_CONFIG_RABBITMQ_SERVICE_WINDOW_SIZE = "facts_window_size"
PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_NAME = "exchange_name"
PROPERTIES_CONFIG_RABBITMQ_SERVICE_EXCHANGE_TYPE = "exchange_type"
PROPERTIES_CONFIG_RABBITMQ_SERVICE_QUEUE = "queue"
PROPERTIES_CONFIG_RABBITMQ_SERVICE_ROUTING_KEY = "routing_key"

# Context Requests
ATTRIBUTES_NAME = u'name'
ATTRIBUTES_TYPE = u'type'
ATTRIBUTES_VALUE = u'contextValue'

# Configuration constants
FACTS_DEFAULT_WINDOW_SIZE = 2

# Test constants
IMPLICIT_WAIT_AFTER_NOTIFICATION = 1  # Seconds.
