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
import json
import requests
import logging.config
from config import config


class cloto_client():
    """This class provides methods to provide connection with Cloto component.
    """
    client = requests

    def get_window_size(self, tenantId):
        """Subscribes server to Context Broker to get information about  cpu and memory monitoring"""
        clotoURL = config.get('common', 'cloto')
        clotoPort = config.get('common', 'clotoPort')
        clotoVersion = config.get('common', 'clotoVersion')
        headers = {"Content-type": "application/json", "Accept": "application/json"}

        r = self.client.get(clotoURL + ":" + clotoPort + "/" + clotoVersion + "/" + tenantId, headers=headers)

        if r.status_code == 200:
            decoded = json.loads(r.text.decode())

        else:
            logging.error("ERROR, HTTP Response: %d"
                % (r.status_code))
            raise SystemError("ERROR, HTTP Response: %d"
                % (r.status_code))

        return decoded["windowsize"]
