from unittest import TestCase

from Redis import Redis

__author__ = 'fla'


class TestRedis(TestCase):
    pass

    def testInsertOneElement(self):
        """testInsertOneElement should always return one element in the list"""
        p = Redis()
        expectedvalue = ['1']
        p.insert(1)
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testInsertTwoElement(self):
        """testInsertTwoElement should always return two element in the list"""
        p = Redis()
        expectedvalue = ['1', '2']
        p.insert(1)
        p.insert(2)
        result = p.range()

        self.assertEqual(expectedvalue, result)

    def testInsertGTFiveElement(self):
        """testInsertGTFiveElement should always return five element if we have
        five or more than five element in the list"""
        p = Redis()
        expected = ['2', '3', '4', '5', '6']
        p.insert(1)
        p.insert(2)
        p.insert(3)
        p.insert(4)
        p.insert(5)
        p.insert(6)
        result = p.range()

        self.assertEqual(expected, result)

    def testSumOneValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = Redis()
        expected = 1
        p.insert(1)
        result = p.sum(p.range())

        self.assertEqual(expected, result)

    def testSumZeroValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = Redis()
        expected = 0
        result = p.sum(p.range())

        self.assertEqual(expected, result)

    def testSumListValue(self):
        """testSumValores should return the sum of a list
         of values"""
        p = Redis()

        expected = 10

        p.insert(1)
        p.insert(2)
        p.insert(3)
        p.insert(4)

        li = p.range()

        result = p.sum(li)

        self.assertEqual(expected, result)

    def testSumListValue(self):
        """testSumValores should return the sum of the last
        5 values of the list of values"""
        p = Redis()

        expected = 25

        p.insert(1)
        p.insert(2)

        p.insert(3)
        p.insert(4)
        p.insert(5)
        p.insert(6)
        p.insert(7)

        li = p.range()

        result = p.sum(li)

        self.assertEqual(expected, result)

    def testMediaListof4Values(self):
        """ return the media of a list of values
        """
        p = Redis()

        expected = 2.5

        p.insert(1)
        p.insert(2)
        p.insert(3)
        p.insert(4)

        li = p.range()

        result = p.media(li)

        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
