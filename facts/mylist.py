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


class mylist(object):
    "store file metadata"
    def __init__(self, data=None):
        self.insert(data)

    @staticmethod
    def parselist(data):
        p3 = data.lstrip().replace('[','').replace(']','').split(',')

        #p3 = [int(j) for j in p3]
        p3[0] = str(p3[0].replace("u","").replace("'",""))

        p3[1] = float(p3[1])
        p3[2] = float(p3[2])

        p3[3] = str(p3[3].lstrip().replace("'",""))

        return p3

    def insert(self, data):
        if isinstance(data, list) == False:
            self.data = []
        else:
            if isinstance(data[0], list) or isinstance(data[0], int) or (isinstance(data[0], str) and data[0][0] != '['):
                self.data = data
            else:
                if isinstance(data[0], str):
                    p4 = []

                    for i in range(0, len(data)):
                        p3 = mylist.parselist(data[i])

                        p4.append(p3)

                    self.data = p4

    def delete(self):
        self.data = []

    @staticmethod
    def sum(data):
        aux = mylist(data).get()
        if len(aux) > 1:
            return mylist(aux[0]) + mylist.sum(data[1:])
        elif len(aux) == 1:
            return mylist(aux[0])
        else:
            return float(0)

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        """ add the values of the list except the first one,
        """
        if isinstance(other, mylist):
            result = mylist()
            result.data = self.data

            for i in range(1, len(self.data)-1):
                result.data[i] = self.data[i] + other.data[i]

            return result

    def __div__(self, other):
        """ div the list by a integer number
        """
        if isinstance(other, int):
            result = mylist(self.data)
            #result.data = self.data
            for i in range(1, len(self.data)-1):
                result.data[i] = self.data[i] / float(other)

            return result


    def get(self):
        return self.data

    @classmethod
    def isdata(self, data):
        '''check that data is a valid data'''
        if isinstance(data, mylist) and isinstance(data.get(), list):
            if len(data) == 4:
                return True
            else:
                return False
        else:
            return False
