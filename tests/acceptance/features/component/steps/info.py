# -*- coding: utf-8 -*-
#
# Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U
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

__author__ = "@jframos"

import behave
from behave import step
from hamcrest import assert_that, equal_to, is_, contains_string

behave.use_step_matcher("re")


@step(u'the fiware-facts service properly deployed')
def fiware_facts_service_properly_deployed(context):

    # Nnothing to do, so far
    pass


@step(u'I request the service info')
def i_request_the_service_info(context):

    print("> GET server info from FACTS server")
    context.response = context.facts_client.get_server_info()


@step(u'the HTTP "(?P<status_code>.*)" is returned')
def http_code_is_returned(context, status_code):

    assert_that(str(context.response.status_code), is_(status_code),
                "Response to CB notification has not got the expected HTTP response code: Message: {}".format(
                    context.response.text))


@step(u'response contains "(.*)"')
def and_the_response_contains(context, content):

    assert_that(context.response.text, contains_string(content),
                "Response does not contains the expected value")
