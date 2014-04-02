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
from module.mylist import mylist


class Testmylist(TestCase):
    pass

    def testisdatatrue(self):
        """testisdatatrue should always return true due to p1 is mylist and the length is 4"""
        p1 = mylist()

        p1.insert([1, 2, 3, 4])

        expectedvalue = True

        result = mylist.isdata(p1)

        self.assertEqual(expectedvalue, result)

    def testisdatafalse1(self):
        """testisdatafalse should always return false due to p1 is mylist but the length is not equal to 4"""
        p1 = mylist()

        p1.insert([1, 2, 3])

        expectedvalue = False

        result = mylist.isdata(p1)

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
        p1 = mylist([1, 2, 3, 4])

        expectedvalue = [1, 2, 3, 4]

        result = p1.get()

        self.assertEqual(expectedvalue, result)

    def testsum(self):
        """check the sum of list"""
        p1 = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]

        expectedvalue = [1, 6, 9, 4]

        result = mylist.sum(p1)

        self.assertEqual(expectedvalue, result.data)

    def testdivlist(self):
        """check the division by a integer the list except the first one"""
        p1 = [1, 2, 4, 8]

        expectedvalue = [1, 1, 2, 8]

        p1mylist = mylist(p1)

        result = p1mylist / 2

        self.assertEqual(expectedvalue, result.data)

    def testdivlistFloat(self):
        """check the division by a float the list except the first one"""
        p1 = [1, 3, 5, 8]

        expectedvalue = [1, 1.5, 2.5, 8]

        p1mylist = mylist(p1)

        result = p1mylist / 2

        self.assertEqual(expectedvalue, result.data)

    def testmedia(self):
        """check the media of a list of data"""

        expectedvalue = ['1', 8, 9.75, '4']

        p1 = ['[1, 2, 3, 4]', '[5, 6, 7, 8]', '[9, 10, 11, 12]', '[13, 14, 18, 16]']

        result = mylist.sum(p1) / len(p1)

        self.assertEqual(expectedvalue, result.data)

    def testsum2(self):
        """check the sum of a list of strings but with commas"""
        p1 = ['[1, 2, 3, 4]', '[1, 2, 3, 4]', '[1, 2, 3, 4]', '[1, 2, 3, 4]']

        expectedvalue = ['1', 8, 12, '4']

        result = mylist.sum(p1)

        self.assertEqual(expectedvalue, result.data)

    def testinsert(self):
        """check the insertion of list of strings"""
        p1 = ['[1, 2, 3, 4]']

        r1 = mylist()

        expectedvalue = [['1', 2, 3, '4']]

        r1.insert(p1)

        result = r1.get()

        self.assertEqual(expectedvalue, result)

    def testinsert2(self):
        """check the insertion of list of strings"""
        p1 = ['[1, 2, 3, 4]', '[1, 2, 3, 4]', '[1, 2, 3, 4]', '[1, 2, 3, 4]']

        r1 = mylist()

        expectedvalue = [['1', 2, 3, '4'], ['1', 2, 3, '4'], ['1', 2, 3, '4'], ['1', 2, 3, '4']]

        r1.insert(p1)

        result = r1.get()

        print result

        self.assertEqual(expectedvalue, result)

    def testRealInsert(self):
        """test insertion of real data"""

        expectedvalue = [[u'44', 1.0, 0.14, '2014-03-29T19:18:25.784424']]
        p1 = ["[u'44', 1.0, 0.14, '2014-03-29T19:18:25.784424']"]

        r1 = mylist()
        r1.insert(p1)

        result = r1.get()

        print result

        self.assertEqual(expectedvalue, result)

    def testRealInsert2(self):
        """test insertion of real data"""

        expectedvalue = [u'44', 1.0, 0.14, '2014-03-29T19:18:25.784424']
        p1 = "[u'44', 1.0, 0.14, '2014-03-29T19:18:25.784424']"

        print mylist.parselist(p1)

        r1 = mylist()
        r1.insert(mylist.parselist(p1))

        result = r1.get()

        print result

        self.assertEqual(expectedvalue, result)

    def testReadMedia1Data(self):
        """test the insertion of a real data and calculate its media"""

        p1 = [u'44', 1.0, 0.14, '2014-03-29T23:02:46.973949']
        expectedvalue = [u'44', 1.0, 0.14, '2014-03-29T23:02:46.973949']

        p1[0] = str(p1[0])

        p2 = list()

        p2.insert(0, p1)

        result = mylist.sum(p2) / len(p2)

        self.assertEqual(expectedvalue, result.data)
