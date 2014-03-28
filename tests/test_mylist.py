__author__ = 'fla'

from unittest import TestCase

from mylist import mylist

__author__ = 'fla'


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
        """check the sum of vectors"""
        p1 = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]

        expectedvalue = [1, 6, 9, 12]

        result = mylist.sum(p1)

        print "Result: {}".format(result)

        self.assertEqual(expectedvalue, result.data)

if __name__ == "__main__":
    unittest.main()
