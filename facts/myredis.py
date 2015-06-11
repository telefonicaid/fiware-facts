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

from config import config, fact_attributes, windowsize_attributes
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
        if isinstance(data, list) and len(data) == len(fact_attributes):
            self.r.rpush(tenantid + "." + serverid, data)
            self.r.ltrim(tenantid + "." + serverid, -5, -1)
        else:
            return "error"

    def range(self, tenantid, serverid):
        """ Return the list of element stored the que queue.
         :return a list of lists
        """
        return self.r.lrange(tenantid + "." + serverid, -100, 100)

    def media(self, lista, windowsize):
        """ Calculate the media of a list of data

         :param mylist lista     The mylist instance with the data to be added.
         :return mylist          The media of the data
        """
        if isinstance(windowsize, list) and len(windowsize) == 1:
            windowsize = int(windowsize[0])
        if len(lista) >= windowsize:
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
        """ Delete a specific queue from the redis system.
        """
        self.r.delete(nqueue)

    def insert_window_size(self, tenantid, data):
        """ Insert data into the redis queue.

        :param list data:     The list of data to be stored in the queue
        :return               This operation does not return anything except when the data
                              is no list or the number of element is not equal to 4.
        """
        if isinstance(data, int) or isinstance(data, long):
            self.r.rpush("windowsize" + "." + tenantid, data)
            self.r.ltrim("windowsize" + "." + tenantid, -1, -1)

    def get_windowsize(self, tenantid):
        """ Return the list of element stored the que queue for the tenant.
         :return a list of lists
        """
        return self.r.lrange("windowsize" + "." + tenantid, -100, 100)

    def check_time_stamps(self, tenantid, serverid, lista, data):
        """
        Check if the list is valid checking last item time-stamp with the new item time-stamp
        :return:
        """
        from dateutil import parser
        textmin = lista[-1].split("'")
        datemin = parser.parse(textmin[-2], fuzzy=True)
        datemax = parser.parse(data[-1], fuzzy=True)
        from config import windowsize_facts

        timediff = datemax - datemin
        if  timediff > windowsize_facts:
            self.r.delete(tenantid + "." + serverid)
            return False
        else:
            return True
