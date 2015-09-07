# -*- coding: utf-8 -*-
#
# Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is parpt of FI-WARE project.
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

__author__ = "@jframos"


from commons.environment_commons import set_up
from qautils.logger.logger_utils import get_logger

__logger__ = get_logger(__name__)


def before_all(context):

    __logger__.info("START ...")
    __logger__.info("Setting UP acceptance test project ")
    set_up(context)


def before_feature(context, feature):

    __logger__.info("=========== START FEATURE =========== ")
    __logger__.info("Feature name: %s", feature.name)


def before_scenario(context, scenario):

    __logger__.info("********** START SCENARIO **********")
    __logger__.info("Scenario name: %s", scenario.name)


def after_scenario(context, scenario):

    __logger__.info("********** END SCENARIO **********")


def after_feature(context, feature):

    __logger__.info("=========== END FEATURE =========== ")


def after_all(context):

    __logger__.info("... END  :)")
