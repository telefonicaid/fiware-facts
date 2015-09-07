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


from qautils.configuration.configuration_utils import set_up_project
from fiwarefacts_client.client import FactsClient
import qautils.configuration.configuration_utils as configuration_utils
from qautils.configuration.configuration_utils import PROPERTIES_CONFIG_SERVICE_PROTOCOL, \
    PROPERTIES_CONFIG_SERVICE_RESOURCE, PROPERTIES_CONFIG_SERVICE_PORT, PROPERTIES_CONFIG_SERVICE_HOST
from commons.constants import PROPERTIES_CONFIG_FACTS_SERVICE


def set_up(context):
    """
    Setup project and init Behave Context.
    :param context: Behave Context.
    :return: None
    """

    set_up_project()
    context.facts_client = FactsClient(
        configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_PROTOCOL],
        configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_HOST],
        configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_PORT],
        configuration_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_RESOURCE])
