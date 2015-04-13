#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
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
__author__ = 'gjp'
from unittest import TestCase
from mockito import *
from mock import patch
from requests import Response
from facts.config import config


class cloto_client_tests(TestCase):
    def setUp(self):

        self.tenantId = "tenantId"
        self.fake_tenantId = "fakeTenantId"
        self.mockedClient = mock()
        response = Response()
        response.status_code = 200
        response._content = '{"owner": "Telefonica I+D", ' \
            '"doc": "https://forge.fi-ware.org/plugins/mediawiki/wiki/fiware/' \
            'index.php/Policy_Manager_Open_RESTful_API_Specification",' \
            ' "runningfrom": "15/04/09 10:37:47",' \
            ' "version": "1.2.0", "windowsize": 5}'
        response_failure = Response()
        response_failure.status_code = 401
        response_failure._content = '{"unauthorized": ' \
            '{"message": ' \
            '"Token is not valid for specified tenant fakeTenantId (HTTP 401)", "code": 401}}'
        clotoURL = config.get('common', 'cloto')
        clotoPort = config.get('common', 'clotoPort')
        clotoVersion = config.get('common', 'clotoVersion')
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        when(self.mockedClient).get(clotoURL + ":" + clotoPort + "/" + clotoVersion + "/" +
                                    self.tenantId, headers=headers).thenReturn(response)
        when(self.mockedClient).get(clotoURL + ":" + clotoPort + "/" + clotoVersion + "/" +
                                    self.fake_tenantId, headers=headers).thenReturn(response_failure)

    def test_cloto_client(self):
        """Tests if method gets a window size from fiware-cloto component."""
        import facts.cloto_client as Cloto
        cloto = Cloto.cloto_client()
        cloto.client = self.mockedClient
        response = cloto.get_window_size(self.tenantId)
        self.assertEqual(response, 5)

    @patch('facts.cloto_client.logging')
    def test_cloto_client_fail(self, mock_logging):
        """Tests if method fails when try to get a window size of a fake tenantId from fiware-cloto component."""
        import facts.cloto_client as Cloto
        cloto = Cloto.cloto_client()
        cloto.client = self.mockedClient
        try:
            response = cloto.get_window_size(self.fake_tenantId)
        except SystemError as ex:
            self.assertTrue(mock_logging.error.called)
            self.assertRaises(ex)
