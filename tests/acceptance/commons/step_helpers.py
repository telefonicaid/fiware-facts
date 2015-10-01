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


from qautils.dataset.dataset_utils import DatasetUtils
import uuid

_dataset_utils = DatasetUtils()


def send_context_notification_step_helper(context, tenant_id, server_id):
    """
    STEP HELPER. This method sends a context notification to FACTS service using the given parameters.
       Behave's 'context' will have a table with the attribute values to be used in the notification.
       If they are not specified, default ones are used.
       Each row of the table is a single request (context notification) to be sent to FACTS service.
    :param context (Behave 'Context'): Behave step context
    :param tenant_id (String): TenantID
    :param server_id (String): ServierID
    :return: None
    """

    # Prepare table data and send the context notifications.
    for element in context.table.rows:
        testdata = dict()

        auxdata = element.as_dict()
        auxdata = _dataset_utils.generate_fixed_length_params(auxdata)
        auxdata = _dataset_utils.remove_missing_params(auxdata)
        testdata.update(auxdata)

        attribute_list = list()
        for data in testdata:
            attribute_list.append({"name": data, "type": "string", "value": testdata[data]})

        type = context.context_elements['type'] if 'type' in context.context_elements else None
        is_pattern = context.context_elements['isPattern'] if 'isPattern' in context.context_elements else None
        id = context.context_elements['id'] if 'id' in context.context_elements else None

        print("> Send a context notification to FIWARE-FACTS. TenantID: %s, ServerID: %s" % (tenant_id, server_id))
        context.response = context.facts_client.send_monitored_data(subscription_id = str(uuid.uuid1()),
                                                                    originator=server_id,
                                                                    status_code="200",
                                                                    details="OK",
                                                                    type=type,
                                                                    is_pattern=is_pattern,
                                                                    id=id,
                                                                    attribute_list=attribute_list,
                                                                    tenant_id=tenant_id,
                                                                    server_id=server_id)
