# -*- coding: utf-8 -*-

# Copyright 2015 Telefonica Investigación y Desarrollo, S.A.U
#
# This file is part of FIWARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
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


from qautils.http.rest_client_utils import RestClient, API_ROOT_URL_ARG_NAME
from qautils.http.body_model_utils import model_to_request_body
from qautils.http.headers_utils import HEADER_REPRESENTATION_JSON, HEADER_CONTENT_TYPE
from fiwarefacts_client.context_notification_model_utils import create_context_notification_model

ROOT_PATTER = "{"+API_ROOT_URL_ARG_NAME+"}"
FACTS_PATTER = ROOT_PATTER + "/{tenant_id}/servers/{server_id}"


class FactsClient(RestClient):

    def __init__(self, protocol, host, port, resource):
        """
        Inits a REST Client for FIWARE-FACTS component
        :param protocol (string): API Protocol
        :param host (string): API Host
        :param port (string): API Port
        :param resource (string): API base Resource
        :return: None
        """
        super(FactsClient, self).__init__(protocol, host, port, resource)

        self.headers = dict({HEADER_CONTENT_TYPE: HEADER_REPRESENTATION_JSON})

    def get_server_info(self):
        """
        Request the FACTS' server info via API
        :return (Request response): Request with the server info
        """
        return super(FactsClient, self).get(ROOT_PATTER)

    def send_monitored_data(self, subscription_id=None, originator=None,
                            status_code=None, details=None, reason=None,
                            type=None, is_pattern=None, id=None, attribute_list=None,
                            tenant_id=None, server_id=None):
        """
        This method send a notification to Facts service emulating a context request from Context Broker.
        :param context_responses: List with all context responses from server
        :param originator: String with the originator identifier
        :param subscription_id: OpenStack subscription unique identifier
        :param status_code: Numerical status code generated from context server
        :param details: Details regarding the context
        :param reason: Information about the context
        :param type (string): Context type
        :param is_pattern (Bool): Value of 'isPattern' attribute
        :param id (string): The id of the entity.
        :param attribute_list (list of dicts): All atribute values
                [{"name": "temperature", "type": "float", "value": "23"}, ...]
        :param tenant_id (string): TenantID
        :param server_id (string): ServerID
        :return: None
        """

        context_notification_model = create_context_notification_model(subscription_id, originator,
                                                                       status_code, details, reason,
                                                                       type, is_pattern, id, attribute_list)

        body = model_to_request_body(context_notification_model, HEADER_REPRESENTATION_JSON)
        return super(FactsClient, self).post(FACTS_PATTER, body, self.headers,
                                             tenant_id=tenant_id, server_id=server_id)
