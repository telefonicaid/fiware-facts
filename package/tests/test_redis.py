from unittest import TestCase

from package.Redis import Redis

__author__ = 'fla'


class TestRedis(TestCase):
    pass

    def testInsertListWithOneElement(self):
        """testInsertOneElement should always return [] due to we insert a list with no 4 elements"""
        p = Redis()

        expectedvalue = []
        p.insert([1])
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testInsertListWithFourElements(self):
        """testInsertOneElement should always return [] due to we insert a list with no 4 elements"""
        p = Redis()

        expectedvalue = ['[1, 2, 3, 4]']
        p.insert([1, 2, 3, 4])
        result = p.range()

        self.assertEqual(expectedvalue, result)


    def testInsertTwoCorrectElements(self):
        """testInsertTwoElement should always return two element in the list"""
        p = Redis()

        expectedvalue = ['[1, 2, 3, 4]', '[5, 6, 7, 8]']
        p.insert([1, 2, 3, 4])
        p.insert([5, 6, 7, 8])
        result = p.range()

        self.assertEqual(expectedvalue, result)


    def testInsertGTFiveElement(self):
        """testInsertGTFiveElement should always return five element if we have
        five or more than five element in the list"""
        p = Redis()

        expectedvalue = ['[5, 6, 7, 8]', '[9, 10, 11, 12]', '[13, 14, 15, 16]', '[17, 18, 19, 20]', '[21, 22, 23, 24]']
        p.insert([1, 2, 3, 4])
        p.insert([5, 6, 7, 8])
        p.insert([9, 10, 11, 12])
        p.insert([13, 14, 15, 16])
        p.insert([17, 18, 19, 20])
        p.insert([21, 22, 23, 24])
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testSumOneValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = Redis()
        expected = '[1, 2, 3, 4]'
        p.insert([1, 2, 3, 4])
        result = p.sum(p.range())

        self.assertEqual(expected, result)

    def testSumZeroValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = Redis()
        expected = '[]'
        result = p.sum(p.range())

        self.assertEqual(expected, result)

    def testSumListValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = Redis()

        expected = [1, 8, 12, 4]

        p.insert([1, 2, 3, 4])
        p.insert([1, 2, 3, 4])
        p.insert([1, 2, 3, 4])
        p.insert([1, 2, 3, 4])

        li = p.range()

        result = p.sum(li)

        self.assertEqual(expected, result.data)

    def testSumListValue(self):
        """testSumValores should return the sum of the last
        5 values of the list of values"""
        p = Redis()

        expected = [100, 2222200, 3333300, 400]

        p.insert([1, 2, 3, 4])
        p.insert([10, 20, 30, 40])

        p.insert([100,         200,     300,     400])
        p.insert([1000,       2000,    3000,    4000])
        p.insert([10000,     20000,   30000,   40000])
        p.insert([100000,   200000,  300000,  400000])
        p.insert([1000000, 2000000, 3000000, 4000000])

        li = p.range()

        result = p.sum(li)

        self.assertEqual(expected, result.data)

    def testMediaListof4Values(self):
        """ return the media of a list of values
        """
        p = Redis()

        expected = [1, 8, 9.75, 4]

        p.insert([1, 2, 3, 4])
        p.insert([5, 6, 7, 8])
        p.insert([9, 10, 11, 12])
        p.insert([13, 14, 18, 16])

        li = p.range()

        result = p.media(li)

        self.assertEqual(expected, result.data)

