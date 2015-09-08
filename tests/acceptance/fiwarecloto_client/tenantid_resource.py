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
from qautils.http.body_model_utils import response_body_to_dict
from qautils.http.headers_utils import HEADER_ACCEPT
from qautils.logger.logger_utils import get_logger

__logger__ = get_logger(__name__)

CLOTO_BASE_URI = "{"+API_ROOT_URL_ARG_NAME+"}"
CLOTO_TENANT_URI = CLOTO_BASE_URI + '/{tenant_id}/'


class TenantIdResourceClient(RestClient):

    def __init__(self, protocol, host, port, resource, headers):
        """
        Class constructor. Inits default attributes.
        :param protocol: Connection protocol (HTTP | HTTPS)
        :param host: Host
        :param port: Port
        :param tenant_id: TenantID
        :param resource: Base URI resource
        :param headers: HTTP Headers
        :return: None
        """

        __logger__.debug("Init CLOTO-TenantId resource client")
        self.headers = headers
        super(TenantIdResourceClient, self).__init__(protocol, host, port, resource=resource)

    def get_tenant_id(self, tenant_id):
        """
        This method gets the tenant data from CLOTO component.
        :param tenant_id: The tenant ID.
        :return: A duple : The data of the tenant as a dict (response body), and the 'Request' response
        """

        __logger__.info("Get TenantID data of: %s", tenant_id)
        response = self.get(CLOTO_TENANT_URI, headers=self.headers, parameters=None, tenant_id=tenant_id)
        response_body_model = response_body_to_dict(response, self.headers[HEADER_ACCEPT])

        return response_body_model, response
