# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
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
__author__ = 'fla'

from flask.ext.testing import TestCase
from flask import Flask
from mockito import *
from mock import patch, MagicMock
import urllib2
import json
import unittest
from facts import server as server


class MyCursor(MagicMock):

    # Mock of a mysql cursor
    result = None

    def execute(self, query):
        # Generates mocked results depending of the MYSQL query content
        if query.startswith("SELECT * FROM ") \
                and query.__contains__("cloto.cloto_tenantinfo")\
                and query.__contains__("WHERE tenantId=\"tenantId\""):
            self.result = [["tenantId", 5]]

    def fetchall(self):
        # returns the result of the query
        return self.result


class MyAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Put Flask into TESTING mode for the TestClient
        server.app.config['TESTING'] = True
        # Disable CSRF checking for WTForms
        server.app.config['WTF_CSRF_ENABLED'] = False
        # Point SQLAlchemy to a test database location
        # (set in virtualenv normally, but fall back to sqlite if not defined)
        self.app = server.app.test_client()
        self.app.post()


"""Class to test the flask, gevent process
"""


class MyTest(MyAppTest):

    def setUp(self):
        self.tenantId = "tenantId"
        self.mockedClient = mock()
        mockedCursor = MyCursor()
        when(self.mockedClient).cursor().thenReturn(mockedCursor)
        server.myClotoDBClient.conn = self.mockedClient
        self.url = '/v1.0/33/servers/44'
        self.url2 = '/v1.0'
        self.url3 = '/v1.0/tenantId/servers/44'

    def test_server_is_up_and_running(self):
        """ Test that a fiware-facts is up and running and return
        information of the GET operation

        :return       200 Ok
        """
        response = self.app.get(self.url2)
        self.assertEqual(response.status_code, 200)

    def test_some_json(self):
        """ Test that the POST operation over the API returns a error if
        content-type is not application/json.

        :return       500 Internal Server error
        """
        data = {'ids': [12, 3, 4, 5, 6]}

        req = urllib2.Request(self.url)

        req.add_header('Content-Type', 'application/json')

        try:
            response = self.app.post(self.url, json.dumps(data))

        except (urllib2.HTTPError), err:
            self.assertEqual(err.status_code, 500)
            self.assertEqual(err.data, "INTERNAL SERVER ERROR")

    def test_context_broker_message(self):
        """ Test that the POST operation over the API returns a valid response if message is built correctly.

        :return       200 Ok
        """
        data = {'ids': [12, 3, 4, 5, 6]}
        data2 = {"contextResponses": [
                    {
                        "contextElement": {
                            "attributes": [
                                {
                                    "value": "99.12",
                                    "name": "usedMemPct",
                                    "type": "string"
                                },
                                {
                                    "value": "99.14",
                                    "name": "cpuLoadPct",
                                    "type": "string"
                                },
                                {
                                    "value": "99.856240",
                                    "name": "freeSpacePct",
                                    "type": "string"
                                },
                                {
                                    "value": "99.8122",
                                    "name": "netLoadPct",
                                    "type": "string"
                                }
                            ],
                            "id": "Trento:193.205.211.69",
                            "isPattern": "false",
                            "type": "host"
                        },
                        "statusCode": {
                            "code": "200",
                            "reasonPhrase": "OK"
                        }

                    }
                ]
            }

        response = self.app.post(self.url3, data=json.dumps(data2), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
