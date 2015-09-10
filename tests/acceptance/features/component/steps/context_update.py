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
from hamcrest import assert_that
import uuid
from qautils.dataset.dataset_utils import DatasetUtils
import qautils.configuration.configuration_utils as config_utils
from qautils.configuration.configuration_properties import PROPERTIES_CONFIG_SERVICE_OS_TENANT_ID
from commons.constants import PROPERTIES_CONFIG_FACTS_SERVICE

behave.use_step_matcher("re")
dataset_utils = DatasetUtils()


@step(u'the tenant-id registered in CLOTO component')
def tenant_id_is_registered_in_cloto(context):

    # A GET request is executed to CLOTO component, to init all data about that tenant in its system.
    context.tenant_id_facts = config_utils.config[PROPERTIES_CONFIG_FACTS_SERVICE][PROPERTIES_CONFIG_SERVICE_OS_TENANT_ID]
    _, response = context.cloto_client.get_tenant_id_resource_client().get_tenant_id(context.tenant_id_facts)

    assert_that(response.ok,
                "TenantId '{}' for testing cannot be retrieved from CLOTO: Message: {}".format(context.tenant_id_facts,
                                                                                               response.text))


@step(u'a context notification is received for "(?P<server_id>.*)" with values')
def a_context_update_is_received(context, server_id):

    testdata = dataset_utils.prepare_data(context.table)
    attribute_list = list()
    for header in context.table.headings:
        attribute_list.append({"name": header, "type": "string", "value": testdata.rows[0][header]})


    context.response = context.facts_client.send_monitored_data(subscription_id = str(uuid.uuid1()),
                                                                originator=server_id,
                                                                status_code="200",
                                                                details="OK", type="vm",
                                                                is_pattern="false",
                                                                id=server_id,
                                                                attribute_list=attribute_list,
                                                                tenant_id=context.tenant_id_facts,
                                                                server_id=server_id)

@step(u'the context is updated')
def the_context_is_updated(context):

    assert_that(context.response.ok,
                "Response to CB notification is not the expected one: Message: {}".format(context.response.text))

