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

from config import config
from mylist import mylist
from redis.exceptions import ConnectionError
import logging
import redis

nqueue = config.get('common', 'redisQueue')

# TODO: change the default queue in redis to incorporate the server ID.
# TODO: Check the temporal mark when we want to calculate the media of data.
# TODO: Review Kalman filter in order to change the estimation of the data in the windows size.


class myredis(object):
    """
    Class to create lists on redis distribution. it is assumed
    that a redis-server is running at host:port.
    """
    def __init__(self):
        """ Initialize the class and create a connection with a redis server instance.
        The initialization includes the deletion of the previous queue
        """
        host = config.get('common', 'redisHost')
        port = config.getint('common', 'redisPort')
        self.r = redis.StrictRedis(host=host, port=port, db=0)

        try:
            # TODO: We need to delete all the queues.
            self.r.flushall()
            #self.r.delete(nqueue)

        except ConnectionError:
            message = "[{}] Cannot delete the list. Possibly redis is down".format("-")
            logging.error(message)

    def insert(self, tenantid, serverid, data):
        """ Insert data into the redis queue.

        :param list data:     The list of data to be stored in the queue
        :return               This operation does not return anything except when the data
                              is no list or the number of element is not equal to 4.
        """
        ''' we need to check that data is a list and the exact number of
        element is equal to 4 - Magic Number
        '''
        if isinstance(data, list) and len(data) == 4:
            self.r.rpush(tenantid + "." + serverid, data)
            self.r.ltrim(tenantid + "." + serverid, -5, -1)
        else:
            return "error"

    def range(self, tenantid, serverid):
        """ Return the list of element stored the que queue.
         :return a list of lists
        """
        return self.r.lrange(tenantid + "." + serverid, -100, 100)

    def media(self, lista):
        """ Calculate the media of a list of lidts

         :param mylist lista     The mylist instance with the data to be added.
         :return mylist          The media of the data
        """
        if len(lista) >= 5:
            return self.sum(lista) / len(lista)
        else:
            result = mylist()
            result.data = []
            return result

    def sum(self, lista):
        """ Calculate the sum of a list of data

        :param mylist lista:     The lists of lists which will be added.
        return mylist            The new mylist instance with the result of the operation.
        """
        if len(lista) > 1:
            return mylist.sum(lista)
        elif len(lista) == 1:
            r1 = mylist()
            r1.insert(lista)
            return r1
        else:
            return '[]'

    def delete(self):
        """ Delete a especific queue from the redis system.
        """
        self.r.delete(nqueue)
