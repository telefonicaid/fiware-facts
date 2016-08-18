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
from mock import patch, MagicMock
from keystoneclient.exceptions import NotFound


class MyCursor(MagicMock):
    # Mock of a mysql cursor
    result = None

    def execute(self, query):
        # Generates mocked results depending of the MYSQL query content
        if query.startswith("SELECT * FROM ") \
                and query.__contains__("cloto_tenantinfo")\
                and query.__contains__("WHERE tenantId=\"tenantId\""):
            self.result = [["tenantId", 5]]

    def fetchall(self):
        # returns the result of the query
        return self.result


class cloto_client_tests(TestCase):
    def setUp(self):

        self.tenantId = "tenantId"
        self.fake_tenantId = "fakeTenantId"
        self.mockedClient = mock()
        mockedCursor = MyCursor()
        when(self.mockedClient).cursor().thenReturn(mockedCursor)

    def test_cloto_client(self):
        """Tests if method gets a window size from fiware-cloto component."""
        import facts.cloto_db_client as Cloto
        cloto = Cloto.cloto_db_client()
        cloto.conn = self.mockedClient
        response = cloto.get_window_size(self.tenantId)
        self.assertEqual(response, 5)

    @patch('facts.cloto_db_client.logging')
    @patch('facts.cloto_db_client.mysql', )
    def test_cloto_client_no_connection(self, mock_mysql, mock_logging):
        """Tests if method fails when try to get a window size of a fake tenantId from fiware-cloto component."""
        import facts.cloto_db_client as Cloto
        cloto = Cloto.cloto_db_client()
        try:
            response = cloto.get_window_size(self.tenantId)
        except NotFound as ex:
            self.assertTrue(mock_mysql.connect.called)
            self.assertTrue(mock_logging.error.called)
            self.assertRaises(ex)
