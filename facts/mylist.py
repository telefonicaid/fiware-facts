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

""" Specific list class in order to work with the appropriate representation
of message data.
"""


class mylist(object):
    def __init__(self, data=None):
        """Initialize the list of data

        :param list   data:     The initial value of the list to be processed

        :return:                The mylist object created
        """
        self.insert(data)

    @staticmethod
    def parselist(data):
        """ Static method used to obtain a list from a string representation
        of the data

        :param string data:   The string representation of data

        :return:              The list representation of the string
        """
        # Delete from the string the '[', ']'  and white spaces and divide the
        # content by ',' in a list
        p3 = data.lstrip().replace('[', '').replace(']', '').split(',')

        aux = len(p3) - 1
        # Convert the %cpu and %memory into a float value
        for i in range(1, aux):
            p3[i] = float(p3[i])

        # delete white spaces and ''' in the last value
        p3[aux] = str(p3[aux].lstrip().replace("'", ""))

        return p3

    def insert(self, data):
        """ Insert a list into the class

        :param list data:   The list to be inserted into the class

        :return:            Nothing
        """
        # If the parameter data is not a list, assign a null list
        if isinstance(data, list) == False:
            self.data = []
        else:
            # If the 1st element is a list too e.g.:[ [1, 2, 4], [1, 2, 4] ...]
            # OR the 1st element in a integer number e.g. [1, 2 ,4]
            # OR (the 1st is a string AND the 1st character is a '[' e.g. ['[1, 2, 4]', '[1, 2, 4]', ...]
            # then data is a valid list to be processed
            if isinstance(data[0], list) or isinstance(data[0], int) or isinstance(data[0], float) or \
                    (isinstance(data[0], str) and data[0][0] != '['):
                self.data = data
            else:
                # if the 1st element is a string BUT the 1st character is != to a '['
                # e.g. ['['1', 2.3, 'xxxx']', '['1', 2.3, 'xxxx']', '['1', 2.3, 'xxxx']']
                if isinstance(data[0], str):
                    p4 = []

                    # Extract the sublist in order to process them
                    for i in range(0, len(data)):
                        p3 = mylist.parselist(data[i])

                        p4.append(p3)

                    self.data = p4

    def delete(self):
        """ Delete the content of the list
        """
        self.data = []

    @staticmethod
    def sum(data):
        """ Calculate the addition of all the sublists received in the data list
         :param list data:      The list of data to add with the format [ [1, 2, 'xxx'], [4, 5, 'yyy], ... ]

         :return:               A list with the sum all data in 2nd and 3rd position of each list
        """
        aux = mylist(data).get()
        if len(aux) > 1:
            return mylist(aux[0]) + mylist.sum(data[1:])
        elif len(aux) == 1:
            return mylist(aux[0])
        else:
            return float(0)

    def __len__(self):
        """ Calculate the len of teh data list
         :return:    The len of the data list contained in my class
        """
        return len(self.data)

    def __add__(self, other):
        """ Operator overloading: add the values of the list except the first one
        :param mylist other:      An instance of the mylist class whose data is someth. similar to [1, 2, 'xxxx']
        :return mylist:           A new mylist instance with the sum of all components except the first and the last
        """
        if isinstance(other, mylist):
            result = mylist()
            result.data = self.data

            limit = len(self.data) - 1

            for i in range(1, limit):
                result.data[i] = self.data[i] + other.data[i]

            result.data[limit] = other.data[limit]

            return result

    def __div__(self, other):
        """ Operator overloading: division of the list by a integer number
        :param int other:       The divisor of the list (except the last value). It is not necessary to check if it's 0
                                due to it will be manage by the caller of the function.
        :return mylist:         A new mylist instance with the result of the division.
        """
        if isinstance(other, int):
            result = mylist(self.data)
            for i in range(1, len(self.data) - 1):
                result.data[i] = self.data[i] / float(other)

            return result

    def get(self):
        """ Return the list
        """
        return self.data

    @classmethod
    def isdata(self, info):
        """ Check that info is a valid mylist and the content of data.data is a list
        :param <?> data:       The information to validate
        :return boolean:       True if it is a valid information
                                    info is a instance of mylist
                                    info.get() return a list AND
                                    len(info) is 3
                               False otherwise
        """
        if isinstance(info, mylist) and isinstance(info.get(), list):
            if len(info) == 3:
                return True
            else:
                return False
        else:
            return False
