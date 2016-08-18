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
from mockito import mock, when
from mock import MagicMock
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
                and query.__contains__("cloto_tenantinfo")\
                and query.__contains__("WHERE tenantId=\"tenantId\""):
            self.result = [["tenantId", 5]]

    def fetchall(self):
        # returns the result of the query
        return self.result


class MyAppTest(unittest.TestCase):
    """Class to start flask server as testing mode.
    """

    @classmethod
    def setUpClass(self):
        # Put Flask into TESTING mode for the TestClient
        server.app.config['TESTING'] = True
        # Disable CSRF checking for WTForms
        server.app.config['WTF_CSRF_ENABLED'] = False
        self.app = server.app.test_client()
        self.app.post()


class MyTest(MyAppTest):
    """Class to test flask server.
    """
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

        response = self.app.post(self.url, json.dumps(data))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, '{"error":"Bad request. Content-type is not application/json"}\n')

    def test_context_broker_message(self):
        """ Test that the POST operation over the API returns a valid response if message is built correctly.

        :return       200 Ok
        """
        data2 = {"contextResponses": [
                    {
                        "contextElement": {
                           "attributes": [
                               {
                                   "value": "0.12",
                                   "name": "usedMemPct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.14",
                                   "name": "cpuLoadPct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.856240",
                                   "name": "freeSpacePct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.8122",
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

    def test_context_broker_empty_attributes_message(self):
        """ Test that the POST operation over the API returns a 400 error response if message has no attributes.

        :return       400 Bad Request
        """
        data3 = {"contextResponses": [
                    {
                        "contextElement": {
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

        response = self.app.post(self.url3, data=json.dumps(data3), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_context_broker_any_attribute_is_missing_message(self):
        """ Test that the POST operation over the API returns a 400 error response if message has no attributes.

        :return       400 Bad Request
        """
        data4 = {"contextResponses": [
                    {
                        "contextElement": {
                           "attributes": [
                               {
                                   "value": "0.14",
                                   "name": "cpuLoadPct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.856240",
                                   "name": "freeSpacePct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.8122",
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

        response = self.app.post(self.url3, data=json.dumps(data4), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_context_broker_message_attribute_out_of_range_value(self):
        """ Test that the POST operation over the API returns a 400 error response if message has an attribute value
        greater than 100.

        :return       400 Bad Request
        """
        data2 = {"contextResponses": [
                    {
                        "contextElement": {
                           "attributes": [
                               {
                                   "value": "0.12",
                                   "name": "usedMemPct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.14",
                                   "name": "cpuLoadPct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.856240",
                                   "name": "freeSpacePct",
                                   "type": "string"
                               },
                               {
                                   "value": "100.1",
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
        self.assertEqual(response.status_code, 400)

    def test_context_broker_message_attribute_with_string_value(self):
        """ Test that the POST operation over the API returns a 400 error response if message has an attribute value
        with a non-float value.

        :return       400 Bad Request
        """
        data2 = {"contextResponses": [
                    {
                        "contextElement": {
                           "attributes": [
                               {
                                   "value": "0.12",
                                   "name": "usedMemPct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.14",
                                   "name": "cpuLoadPct",
                                   "type": "string"
                               },
                               {
                                   "value": "0.856240",
                                   "name": "freeSpacePct",
                                   "type": "string"
                               },
                               {
                                   "value": "hundred",
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
        self.assertEqual(response.status_code, 400)
