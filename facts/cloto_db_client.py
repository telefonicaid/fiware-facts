#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
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
__author__ = 'gjp'
import logging.config
from config import config
import MySQLdb as mysql
from keystoneclient.exceptions import NotFound


class cloto_db_client():
    """This class provides methods to provide connection with Cloto database.
    """
    conn = None

    def get_window_size(self, tenantId):
        """
        This method is in charge of retrieve the window size of a tenantId from cloto database.

        :param tenantId: the id of the tenant to request the windowsize
        :return: the window size
        """
        try:
            db = config.get('mysql', 'db')
            if self.conn == None:
                self.conn = mysql.connect(charset=config.get('mysql', 'charset'), use_unicode=True,
                                     host=config.get('mysql', 'host'),
                                     user=config.get('mysql', 'user'), passwd=config.get('mysql', 'password'),
                                     db=db)
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM cloto_tenantinfo WHERE tenantId="{0}"'.format(tenantId))
            data = cursor.fetchall()
            if len(data) == 0:
                raise NotFound('{"error": "TenantID %s not found in database"}' % tenantId)
            else:
                tenant_information = data[0]
                window_size = tenant_information[1]

        except Exception, e:
                logging.error("Error %s" % e.message)
                raise e
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
        return window_size
