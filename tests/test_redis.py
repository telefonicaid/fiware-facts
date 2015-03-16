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
#

from unittest import TestCase
from facts.myredis import myredis
from facts.mylist import mylist

__author__ = 'fla'

""" Class to test the interaction with redis
"""

serverid = ""
tenantid = ""


class TestRedis(TestCase):
    pass

    def testInsertListWithOneElement(self):
        """testInsertOneElement should always return [] due to we insert a list with no elements"""
        p = myredis()

        expectedvalue = []
        p.insert(serverid, tenantid, [1])
        result = p.range(serverid, tenantid)

        self.assertEqual(expectedvalue, result)

    def testInsertListWithThreeElements(self):
        """testInsertOneElement should always return [] due to we insert a list with one element"""
        p = myredis()

        expectedvalue = ["['', 1, 2, 3]"]
        p.insert(serverid, tenantid, [serverid, 1, 2, 3])
        result = p.range(serverid, tenantid)

        self.assertEqual(expectedvalue, result)

    def testInsertListWithMoreThanThreeElements(self):
        """testInsertOneElement should always return [] due to we insert a list with more than 3 elements"""
        p = myredis()

        expectedvalue = []
        p.insert(serverid, tenantid, [serverid, 1, 2, 3, 4])
        result = p.range(serverid, tenantid)

        self.assertEqual(expectedvalue, result)

    def testInsertTwoCorrectElements(self):
        """testInsertTwoElement should always return two element in the list"""
        p = myredis()

        expectedvalue = ["['', 1, 2, 3]", "['', 5, 6, 7]"]
        p.insert(serverid, tenantid, [serverid, 1, 2, 3])
        p.insert(serverid, tenantid, [serverid, 5, 6, 7])
        result = p.range(serverid, tenantid)

        self.assertEqual(expectedvalue, result)

    def testInsertGTFiveElement(self):
        """testInsertGTFiveElement should always return five element if we have
        five or more than five element in the list"""
        p = myredis()

        expectedvalue = ["['', 5, 6, '8']", "['', 9, 10, '12']", "['', 13, 14, '16']",
                         "['', 17, 18, '20']", "['', 21, 22, '24']"]

        p.insert(serverid, tenantid, [serverid, 1, 2, '4'])
        p.insert(serverid, tenantid, [serverid, 5, 6, '8'])
        p.insert(serverid, tenantid, [serverid, 9, 10, '12'])
        p.insert(serverid, tenantid, [serverid, 13, 14, '16'])
        p.insert(serverid, tenantid, [serverid, 17, 18, '20'])
        p.insert(serverid, tenantid, [serverid, 21, 22, '24'])
        result = p.range(serverid, tenantid)

        self.assertEqual(expectedvalue, result)

    def testSumOneValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = myredis()
        expected = [["''", 1.0, 2.0, '3']]
        p.insert(serverid, tenantid, [serverid, 1, 2, 3])
        result = p.sum(p.range(serverid, tenantid))

        self.assertEqual(expected, result.data)

    def testSumZeroValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = myredis()
        expected = '[]'
        result = p.sum(p.range(serverid, tenantid))

        self.assertEqual(expected, result)

    def testSumListValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = myredis()

        expected = ["''''''''", 4, 8, '3']

        p.insert(serverid, tenantid, [serverid, 1, 2, 3])
        p.insert(serverid, tenantid, [serverid, 1, 2, 3])
        p.insert(serverid, tenantid, [serverid, 1, 2, 3])
        p.insert(serverid, tenantid, [serverid, 1, 2, 3])

        li = p.range(serverid, tenantid)

        result = p.sum(li)

        self.assertEqual(expected, result.data)

    def testSumListValue2(self):
        """testSumValores should return the sum of the last
        5 values of the list of values"""
        p = myredis()

        expected = ["''''''''''", 1111100, 2222200, '3000000']

        p.insert(serverid, tenantid, [serverid, 1, 2, '4'])
        p.insert(serverid, tenantid, [serverid, 10, 20, '40'])

        p.insert(serverid, tenantid, [serverid, 100,         200,     300])
        p.insert(serverid, tenantid, [serverid, 1000,       2000,    3000])
        p.insert(serverid, tenantid, [serverid, 10000,     20000,   30000])
        p.insert(serverid, tenantid, [serverid, 100000,   200000,  300000])
        p.insert(serverid, tenantid, [serverid, 1000000, 2000000, 3000000])

        li = p.range(serverid, tenantid)

        result = p.sum(li)

        self.assertEqual(expected, result.data)

    def testMediaListof4Values(self):
        """ return the media of a list of 4 values
        """
        p = myredis()

        expected = ["''''''''''", 6, 7, '14']

        p.insert(serverid, tenantid, [serverid, 0, 1, 2])
        p.insert(serverid, tenantid, [serverid, 3, 4, 5])
        p.insert(serverid, tenantid, [serverid, 6, 7, 8])
        p.insert(serverid, tenantid, [serverid, 9, 10, 11])
        p.insert(serverid, tenantid, [serverid, 12, 13, 14])

        li = p.range(serverid, tenantid)

        result = p.media(li)

        self.assertEqual(expected, result.data)

    def testRealData(self):
        """Test with real data"""
        p = myredis()

        p1 = "[1.0, 0.14, '2014-03-29T19:18:25.784424']"

        expected = []

        p2 = mylist.parselist(p1)

        p.insert(serverid, tenantid, p2)
        p.insert(serverid, tenantid, p2)

        result = p.media(p.range(serverid, tenantid))

        self.assertEqual(expected, result.data)

    def testRealData2(self):
        """Test with real data"""
        p = myredis()

        p1 = "[, 1.0, 0.14, '2014-03-29T19:18:25.784424']"

        expected = ["''''''''''", 1.0, 0.14, '2014-03-29T19:18:25.784424']

        p2 = mylist.parselist(p1)

        p.insert(serverid, tenantid, p2)
        p.insert(serverid, tenantid, p2)
        p.insert(serverid, tenantid, p2)
        p.insert(serverid, tenantid, p2)
        p.insert(serverid, tenantid, p2)


        result = p.media(p.range(serverid, tenantid))

        self.assertEqual(expected, result.data)
