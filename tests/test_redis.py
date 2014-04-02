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
from module.myredis import myredis
from module.mylist import mylist

__author__ = 'fla'

""" Class to test the interaction with redis
"""
class TestRedis(TestCase):
    pass

    def testInsertListWithOneElement(self):
        """testInsertOneElement should always return [] due to we insert a list with no elements"""
        p = myredis()

        expectedvalue = []
        p.insert([1])
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testInsertListWithFourElements(self):
        """testInsertOneElement should always return [] due to we insert a list with one element"""
        p = myredis()

        expectedvalue = ['[1, 2, 3, 4]']
        p.insert([1, 2, 3, 4])
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testInsertTwoCorrectElements(self):
        """testInsertTwoElement should always return two element in the list"""
        p = myredis()

        expectedvalue = ['[1, 2, 3, 4]', '[5, 6, 7, 8]']
        p.insert([1, 2, 3, 4])
        p.insert([5, 6, 7, 8])
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testInsertGTFiveElement(self):
        """testInsertGTFiveElement should always return five element if we have
        five or more than five element in the list"""
        p = myredis()

        expectedvalue = ["['5', 6, 7, '8']", "['9', 10, 11, '12']", "['13', 14, 15, '16']",
                         "['17', 18, 19, '20']", "['21', 22, 23, '24']"]

        p.insert(['1', 2, 3, '4'])
        p.insert(['5', 6, 7, '8'])
        p.insert(['9', 10, 11, '12'])
        p.insert(['13', 14, 15, '16'])
        p.insert(['17', 18, 19, '20'])
        p.insert(['21', 22, 23, '24'])
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testSumOneValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = myredis()
        expected = [['1', 2, 3, '4']]
        p.insert([1, 2, 3, 4])
        result = p.sum(p.range())

        self.assertEqual(expected, result.data)

    def testSumZeroValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = myredis()
        expected = '[]'
        result = p.sum(p.range())

        self.assertEqual(expected, result)

    def testSumListValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = myredis()

        expected = ['1', 8, 12, '4']

        p.insert(['1', 2, 3, '4'])
        p.insert(['1', 2, 3, '4'])
        p.insert(['1', 2, 3, '4'])
        p.insert(['1', 2, 3, '4'])

        li = p.range()

        result = p.sum(li)

        self.assertEqual(expected, result.data)

    def testSumListValue2(self):
        """testSumValores should return the sum of the last
        5 values of the list of values"""
        p = myredis()

        expected = ['100', 2222200, 3333300, '400']

        p.insert(['1', 2, 3, '4'])
        p.insert(['10', 20, 30, '40'])

        p.insert(['100',         200,     300,     '400'])
        p.insert(['1000',       2000,    3000,    '4000'])
        p.insert(['10000',     20000,   30000,   '40000'])
        p.insert(['100000',   200000,  300000,  '400000'])
        p.insert(['1000000', 2000000, 3000000, '4000000'])

        li = p.range()

        result = p.sum(li)

        self.assertEqual(expected, result.data)

    def testMediaListof4Values(self):
        """ return the media of a list of 4 values
        """
        p = myredis()

        expected = ['1', 10, 11.6, '4']

        p.insert([1, 2, 3, 4])
        p.insert([5, 6, 7, 8])
        p.insert([9, 10, 11, 12])
        p.insert([13, 14, 18, 16])
        p.insert([17, 18, 19, 20])

        li = p.range()

        result = p.media(li)

        self.assertEqual(expected, result.data)

    def testRealData(self):
        """Test with real data"""
        p = myredis()

        p1 = "[u'44', 1.0, 0.14, '2014-03-29T19:18:25.784424']"

        expected = []

        p2 = mylist.parselist(p1)

        p.insert(p2)
        p.insert(p2)

        result = p.media(p.range())

        self.assertEqual(expected, result.data)

    def testRealData2(self):
        """Test with real data"""
        p = myredis()

        p1 = "[u'44', 1.0, 0.14, '2014-03-29T19:18:25.784424']"

        expected = ['44', 1.0, 0.14, '2014-03-29T19:18:25.784424']

        p2 = mylist.parselist(p1)

        p.insert(p2)
        p.insert(p2)
        p.insert(p2)
        p.insert(p2)
        p.insert(p2)

        result = p.media(p.range())

        self.assertEqual(expected, result.data)
