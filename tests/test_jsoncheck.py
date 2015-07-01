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

from unittest import TestCase
from facts.jsoncheck import jsoncheck

mydict1 = {
    "contextResponses": [
        {
            "contextElement": {
                "attributes": [
                    {
                        "contextValue": "6",
                        "name": "users",
                        "type": "string"
                    },
                    {
                        "contextValue": "1",
                        "name": "usedMemPct",
                        "type": "string"
                    },
                    {
                        "contextValue": "0.14",
                        "name": "cpuLoadPct",
                        "type": "string"
                    },
                    {
                        "contextValue": "0.856240",
                        "name": "freeSpacePct",
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


mydict2 = {"uno": 1, "dos": "dos", "tres": "tres"}

mydict3 = {"contextResponses": 1}

mydict4 = {"a": 1}


class Testjsoncheck(TestCase):
    pass

    def test_wellformedmessage(self):
        """ Check that a correct message is recognize
        """
        key = ['contextResponses', 'contextElement', 'attributes']

        expectedvalue = ""
        result = jsoncheck.checkit(mydict1, key, 0)
        self.assertEqual(result, None)

    def test_unknowkeyvalue(self):
        """ Check that not all keys are content in the dict¡onary
        """
        key = ['contextResponses', 'context', 'attributes']

        expectedvalue = "Invalid json message. We cannot obtain the key: context"

        try:
            jsoncheck.checkit(mydict1, key, 0)
        except (Exception), err:
            self.assertEqual(expectedvalue, err.message)

    def test_unknowjsonmessage(self):
        """ Check that a not expected message is recognized
        """
        key = ['contextResponses', 'contextElement', 'attributes']

        expectedvalue = "Invalid json message. We cannot obtain the key: contextResponses"

        try:
            jsoncheck.checkit(mydict2, key, 0)
        except (Exception), err:
            self.assertEqual(expectedvalue, err.message)

    def test_dictwithonekey(self):
        """Check that an invalid json with only one valid key is recognized
        """
        key = ['contextResponses', 'contextElement', 'attributes']

        expectedvalue = "Invalid json message. We expected " \
                        "'['contextResponses', 'context', 'attributes']' keys but " \
                        "obtain only 'contextResponses' key"

        try:
            jsoncheck.checkit(mydict3, key, 0)
        except (Exception), err:
            self.assertEqual(expectedvalue, err.message)

    def test_dictwithoneinvalidkey(self):
        """Check that an invalid json with only one valid key is recognized
        """
        key = ['contextResponses', 'contextElement', 'attributes']

        expectedvalue = "Invalid json message. We cannot obtain the key: contextResponses"

        try:
            jsoncheck.checkit(mydict4, key, 0)
        except (Exception), err:
            self.assertEqual(expectedvalue, err.message)
