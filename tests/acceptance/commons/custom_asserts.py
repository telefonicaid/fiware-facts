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

from hamcrest.core.base_matcher import BaseMatcher
import json


class IsMessageInConsumerList(BaseMatcher):
    """
    Custom assertion. Checks if the given message is in the retrieved consumer list
        > Message is given as dict of pair attribute-values. These are the expected values.
        > Consumer list is a list of messages retrieved from RabbitMQ consumer.
          Format: [{'id': 'message_id_as_string', 'body': 'body_message_as_string'}, ...]
          One of its body values should match with the given message.

        The assertion will be TRUE if the message is a sub-dict of some the messages body stored in the consumer_list.
        That is:
            if message is IN some body message of consumer_list (list of messages received by RabbitMQ consumer)
    """

    def __init__(self, consumer_list):
        """
        :param consumer_list: Format: [{'id': 'message_id_as_string', 'body': 'body_message_as_string'}, ...]
        :return: None
        """
        self.consumer_list = consumer_list

    def _matches(self, message):
        """
        Matcher.
        :param message (dict): Expected body to look for it in consumer's list.
        :return: Matches if message is in some retrieved body from RabbitMQ consumer.
        """

        self.message = message

        if not isinstance(self.consumer_list, list):
            return False

        if not isinstance(self.message, dict):
            return False

        # Check each element in the dict.
        # If all elements of self.message are in some of the messages stored in rabbit_message body, -> Matches!
        found = False
        for rabbit_message in self.consumer_list:

            rabbit_message_model = json.loads(rabbit_message['body'])

            equals = len(self.message)
            for element in self.message:
                if element in rabbit_message_model and self.message[element] == rabbit_message_model[element]:
                    equals -= 1
                else:
                    break

            if equals == 0:
                found = True
                break

        return found

    def describe_to(self, description):
        """
        Description of the error.
        :param description: Description given by the user.
        :return: None
        """
        description.append_text('message in the list retrieved from RabbitMQ consumer. ')    \
                   .append_text('The RabbitMQ consumer list is: ' + str(self.consumer_list))


def is_message_in_consumer_list(message):
    """
    Entry point for custom assertion: IsMessageInConsumerList
    :param message: The message to check if it is IN some of the body message of
       consumer_list (list of messages received by RabbitMQ consumer)
    :return: IsMessageInConsumerList Hamcrest matcher.
    """

    return IsMessageInConsumerList(message)
