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
import qautils.configuration.configuration_utils as configuration_utils
from qautils.configuration.configuration_properties import PROPERTIES_CONFIG_SERVICE_PROTOCOL, \
    PROPERTIES_CONFIG_SERVICE_RESOURCE, PROPERTIES_CONFIG_SERVICE_PORT, PROPERTIES_CONFIG_SERVICE_HOST, \
    PROPERTIES_CONFIG_SERVICE_OS_USERNAME, PROPERTIES_CONFIG_SERVICE_OS_PASSWORD, \
    PROPERTIES_CONFIG_SERVICE_OS_TENANT_ID, PROPERTIES_CONFIG_SERVICE_OS_AUTH_URL
from commons.constants import PROPERTIES_CONFIG_FACTS_SERVICE, PROPERTIES_CONFIG_CLOTO_SERVICE


__logger__ = get_logger(__name__)


def before_all(context):

    __logger__.info("START ...")
    __logger__.info("Setting UP acceptance test project ")

    set_up_project()  # Load setting using 'qautils.configuration.configuration_utils'

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


def after_scenario(context, scenario):

    __logger__.info("********** END SCENARIO **********")


def after_feature(context, feature):

    __logger__.info("=========== END FEATURE =========== ")


def after_all(context):

    __logger__.info("... END  :)")
