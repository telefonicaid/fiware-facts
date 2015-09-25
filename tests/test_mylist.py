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
__author__ = 'fla'

from unittest import TestCase
from facts.mylist import mylist


class Testmylist(TestCase):
    pass

    def testisdatatrue(self):
        """testisdatatrue should always return true due to p1 is mylist and the length is 3"""
        p1 = mylist()

        p1.insert([2, 3, 4])

        expectedvalue = True

        result = mylist.isdata(p1)

        self.assertEqual(expectedvalue, result)

    def testisdatafalse1(self):
        """testisdatafalse should always return false due to p1 is mylist but the length is not equal to 3"""
        p1 = mylist()

        expectedvalue = False

        p1.insert([1, 2])

        result = mylist.isdata(p1)

        self.assertEqual(expectedvalue, result)

    def testisdatafalse5(self):
        """testisdatafalse should always return false due to p1 is mylist but the length is not equal to 3"""
        p2 = mylist()

        expectedvalue = False

        p2.insert([1, 2, 3, 4])

        result = mylist.isdata(p2)

        self.assertEqual(expectedvalue, result)

    def testisdatafalse2(self):
        """testisdata should always return false due to p1 is mylist but the content is not a list"""
        p1 = mylist()

        p1.insert(1)

        expectedvalue = False

        result = mylist.isdata(p1)

        self.assertEqual(expectedvalue, result)

    def testisdatafalse3(self):
        """testisdata should always return false due to p1 is not mylist"""
        p1 = 1

        expectedvalue = False

        result = mylist.isdata(p1)

        self.assertEqual(expectedvalue, result)

    def testinit(self):
        """ check the creation of a instance
        """
        p1 = mylist([2, 3, 4])

        expectedvalue = [2, 3, 4]

        result = p1.get()

        self.assertEqual(expectedvalue, result)

    def testsum(self):
        """check the sum of list"""
        p1 = [['serverId', 1, 2, 3], ['serverId', 1, 2, 4], ['serverId', 1, 2, 5]]

        expectedvalue = ['serverId', 3, 6, 5]

        result = mylist.sum(p1)

        self.assertEqual(expectedvalue, result.data)

    def testdivlist(self):
        """check the division by a integer the list except the first one"""
        p1 = ['serverId', 2, 4, 8]

        expectedvalue = ['serverId', 1, 2, 8]

        p1mylist = mylist(p1)

        result = p1mylist / 2

        self.assertEqual(expectedvalue, result.data)

    def testdivlistFloat(self):
        """check the division by a float the list except the first one"""
        p1 = ['serverId', 3, 5, 8]

        expectedvalue = ['serverId', 1.5, 2.5, 8]

        p1mylist = mylist(p1)

        result = p1mylist / 2

        self.assertEqual(expectedvalue, result.data)

    def testmedia(self):
        """check the media of a list of data"""

        expectedvalue = ['serverId', 7, 8, 18]

        p1 = [['serverId', 1, 2, 3], ['serverId', 5, 6, 7], ['serverId', 9, 10, 11], ['serverId', 13, 14, 18]]

        result = mylist.sum(p1) / len(p1)

        self.assertEqual(expectedvalue, result.data)

    def testsum2(self):
        """check the sum of a list of strings but with commas"""
        p1 = ['[serverId, 1, 2, 1]', '[serverId, 1, 2, 2]', '[serverId, 1, 2, 3]', '[serverId, 1, 2, 4]']

        expectedvalue = ['serverId', 4.0, 8.0, '4']

        result = mylist.sum(p1)

        self.assertEqual(expectedvalue, result.data)

    def testinsert(self):
        """check the insertion of list of strings"""
        p1 = ['[serverId, 1, 2, 4]']

        r1 = mylist()

        expectedvalue = [['serverId', 1, 2, '4']]

        r1.insert(p1)

        result = r1.get()

        self.assertEqual(expectedvalue, result)

    def testinsert2(self):
        """check the insertion of list of strings"""
        p1 = ['[serverId, 1, 2, 4]', '[serverId, 1, 2, 4]', '[serverId, 1, 2, 4]', '[serverId, 1, 2, 4]']

        r1 = mylist()

        expectedvalue = [['serverId', 1.0, 2.0, '4'], ['serverId', 1.0, 2.0, '4'], ['serverId', 1.0, 2.0, '4'],
                         ['serverId', 1.0, 2.0, '4']]

        r1.insert(p1)

        result = r1.get()

        self.assertEqual(expectedvalue, result)

    def testRealInsert(self):
        """test insertion of real data"""

        expectedvalue = [['serverId', 1.0, 0.14, '2014-03-29T19:18:25.784424']]
        p1 = ["[serverId, 1.0, 0.14, '2014-03-29T19:18:25.784424']"]

        r1 = mylist()
        r1.insert(p1)

        result = r1.get()

        self.assertEqual(expectedvalue, result)

    def testRealInsert2(self):
        """test insertion of real data"""

        expectedvalue = ['serverId', 1.0, 0.14, '2014-03-29T19:18:25.784424']
        p1 = "[serverId, 1.0, 0.14, '2014-03-29T19:18:25.784424']"

        r1 = mylist()
        r1.insert(mylist.parselist(p1))

        result = r1.get()

        self.assertEqual(expectedvalue, result)

    def testReadMedia1Data(self):
        """test the insertion of a real data and calculate its media"""

        fact = ['serverId', 1.0, 0.14, '2014-03-29T23:02:46.973949']
        expectedvalue = ['serverId', 1.0, 0.14, '2014-03-29T23:02:46.973949']

        p2 = list()

        p2.insert(0, fact)
        p2.insert(0, fact)

        result = mylist.sum(p2)

        result = result / len(p2)

        self.assertEqual(expectedvalue, result.data)

    def testDeleteAQueue(self):
        """test the insertion of a real data and delete the queue"""
        mylist_instance = mylist()
        fact = ['serverId', 1.0, 0.14, '2014-03-29T23:02:46.973949']
        expected_initial_length = 2
        expected_final_length = 0

        p2 = list()

        p2.insert(0, fact)
        p2.insert(0, fact)

        mylist_instance.insert(p2)

        self.assertEqual(expected_initial_length, mylist_instance.__len__())

        mylist_instance.delete()

        self.assertEqual(expected_final_length, mylist_instance.__len__())

    def testInsertAnEmptyQueue(self):
        """test the insertion of a fake data with 0 items"""
        mylist_instance = mylist()
        expected_final = 0
        response = mylist_instance.sum(0)
        self.assertEqual(expected_final, response)
