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
__author__ = 'fla'

from flask.ext.testing import TestCase
from flask import Flask
import urllib2
import json

"""Class to test the flask, gevent process
"""


class MyTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.url = 'http://127.0.0.1:5000/v1.0/33/servers/44'

        return app

    def test_server_is_up_and_running(self):
        """ Test that a fiware-facts is up and running and return
        information of the GET operation

        :return       200 Ok
        """
        response = urllib2.urlopen(self.url)
        self.assertEqual(response.code, 200)

    def test_some_json(self):
        """ Test that the POST operation over the API returns a error if
        content-type is not application/json.

        :return       500 Ok
        """
        data = {'ids': [12, 3, 4, 5, 6]}

        req = urllib2.Request(self.url)

        req.add_header('Content-Type', 'application/json')

        try:
            response = urllib2.urlopen(req, json.dumps(data))

        except (urllib2.HTTPError), err:
            self.assertEqual(err.code, 500)
            self.assertEqual(err.msg, "INTERNAL SERVER ERROR")
