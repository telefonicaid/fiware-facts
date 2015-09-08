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


from qautils.http.headers_utils import set_representation_headers, HEADER_REPRESENTATION_JSON
from qautils.logger.logger_utils import get_logger
from keystoneclient.v2_0 import Client as KeystoneClient
from fiwarecloto_client.tenantid_resource import TenantIdResourceClient

__logger__ = get_logger(__name__)


# HEADERS
X_AUTH_TOKEN = "X-Auth-Token"
TENANT_ID = "Tenant-Id"


class ClotoClient():

    def __init__(self, username, password, tenant_id, auth_url, api_protocol, api_host, api_port, api_resource):
        """
        Init a new Client for CLOTO component.
        :param username (string): The username (OpenStack)
        :param password (string): The password
        :param tenant_id (string): TenantID
        :param auth_url (string): Keystone/IdM auth URL
        :param api_protocol (string): API protocol
        :param api_host (string): API host
        :param api_port (string): API port
        :param api_resource (string): API base resource
        :return: None
        """

        __logger__.info("Init CLOTO Client")
        __logger__.debug("Client parameters: Username: %s, Password: %s, TenantId: %s, API protocol: %s, API host: %s, "
                         "API port: %s, Base resource: %s", username, password, tenant_id, api_protocol, api_host,
                         api_port, api_resource)

        self.headers = dict()
        self.api_protocol = api_protocol
        self.api_host = api_host
        self.api_port = api_port
        self.api_resource = api_resource

        set_representation_headers(self.headers, content_type=HEADER_REPRESENTATION_JSON,
                                   accept=HEADER_REPRESENTATION_JSON)

        self._init_keystone_client(username, password, tenant_id, auth_url)
        self.token = self._get_auth_token()
        __logger__.debug("Token: %s", self.token)

        self.headers.update({X_AUTH_TOKEN: self.token})
        self.headers.update({TENANT_ID: tenant_id})
        __logger__.debug("Headers with OpenStack credentials: %s", self.headers)

    def _init_keystone_client(self, username, password, tenant_id, auth_url):
        """
        Init the keystone client to request token and endpoint data
        :param string username: Username for authentication.
        :param string password: Password for authentication.
        :param string tenant_id: Tenant id.
        :param string auth_url: Keystone service endpoint for authorization.
        :param string region_name: Name of a region to select when choosing an
                                   endpoint from the service catalog.
        :return None
        """

        __logger__.debug("Init Keystone Client")
        self.keystone_client = KeystoneClient(username=username, password=password, tenant_id=tenant_id,
                                              auth_url=auth_url)

    def _get_auth_token(self):
        """
        Get token from Keystone
        :return: Token (String)
        """

        __logger__.debug("Getting auth Token")
        return self.keystone_client.auth_ref['token']['id']

    def get_tenant_id_resource_client(self):
        """
        Create an API resource REST client
        :return: Rest client for 'TenantId' API resource
        """

        __logger__.info("Creating TenantIdResource")

        return TenantIdResourceClient(protocol=self.api_protocol, host=self.api_host,
                                      port=self.api_port, resource=self.api_resource, headers=self.headers)
