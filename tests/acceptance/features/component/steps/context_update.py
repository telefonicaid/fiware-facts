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
from hamcrest import assert_that, is_
import uuid
from qautils.dataset.dataset_utils import DatasetUtils

behave.use_step_matcher("re")
dataset_utils = DatasetUtils()


@step(u'the tenant-id registered in CLOTO component')
def tenant_id_is_registered_in_cloto(context):

    context.tenant_id_facts = context.tenant_id

    print ("> A GET request is executed to CLOTO component, to init all data about that tenant in its system.")
    _, response = context.cloto_client.get_tenant_id_resource_client().get_tenant_id(context.tenant_id_facts)

    print ("> Assert: The tenant is registered in CLOTO component (response is OK)")
    assert_that(response.ok,
                "TenantId '{}' for testing cannot be retrieved from CLOTO: Message: {}".format(context.tenant_id_facts,
                                                                                               response.text))


@step(u'a no registered Tentand-Id in CLOTO component "(?P<tenant_id>.*)"')
def tenant_id_is_not_registered_in_cloto(context, tenant_id):

    context.tenant_id_facts = tenant_id


@step(u'the context notification has default context elements')
def the_context_notification_has_default_context_elements(context):

    # Default parameter for the Context Notification request.
    context.context_elements.update({'isPattern': 'false'})
    context.context_elements.update({'type': 'vm'})
    context.context_elements.update({'id': 'myServerId'})


@step(u'the context notification has these context elements')
def the_context_notification_has_these_context_elements(context):

    # Prepare table data
    context.context_elements = dict()
    for element in context.table.rows:
        data = element.as_dict()
        data = dataset_utils.generate_fixed_length_params(data)
        data = dataset_utils.remove_missing_params(data)
        context.context_elements.update(data)


@step(u'the following notifications are received for "(?P<server_id>.*)" with values')
@step(u'a context notification is received for "(?P<server_id>.*)" with values')
def a_context_update_is_received(context, server_id):

    # Prepare table data. Each element is a single request (context notification) to FACTS.
    for element in context.table.rows:
        testdata = dict()

        auxdata = element.as_dict()
        auxdata = dataset_utils.generate_fixed_length_params(auxdata)
        auxdata = dataset_utils.remove_missing_params(auxdata)
        testdata.update(auxdata)

        attribute_list = list()
        for data in testdata:
            attribute_list.append({"name": data, "type": "string", "value": testdata[data]})

        type = context.context_elements['type'] if 'type' in context.context_elements else None
        is_pattern = context.context_elements['isPattern'] if 'isPattern' in context.context_elements else None
        id = context.context_elements['id'] if 'id' in context.context_elements else None

        print("> Send a context notification to FIWARE-FACTS.")
        context.response = context.facts_client.send_monitored_data(subscription_id = str(uuid.uuid1()),
                                                                    originator=server_id,
                                                                    status_code="200",
                                                                    details="OK",
                                                                    type=type,
                                                                    is_pattern=is_pattern,
                                                                    id=id,
                                                                    attribute_list=attribute_list,
                                                                    tenant_id=context.tenant_id_facts,
                                                                    server_id=server_id)


@step(u'the context is updated')
def the_context_is_updated(context):

    assert_that(context.response.ok,
                "Response to CB notification is not the expected one: Message: {}".format(context.response.text))
