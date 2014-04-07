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

""" Class to verify the content of the json message received in the message
"""


class jsoncheck(object):
    @classmethod
    def checkit(self, dictionary, keylist, cycle):
        """ Check recursively the json dictionary in order to check that it
        contains the keys included in the keylist.

        :param dict dictionary   The dictionary of the json message
        :param list keylist      The list of keys to be checked
        :param int cycle         The step in the recurrent algorith

        :return                  By default this method does not return
                                 anything, except when some key is not found
                                 in the dictionary, then return exception.
        """
        if len(keylist) != 0:
            # Get the first key of the list, in a list format
            key = keylist[:1]

            # Get the list with the rest of keys
            restkey = keylist[1:]

            # Check the dictionary in order to detect if the key is there,
            # in that case it returns the value of that key.
            # Otherwise, it returns a null list '[]'
            result = reduce(lambda x, y:
                            dictionary.get(y) and x.append(dictionary[y]) or x, key, [])

            # If it cannot find the key in the dictionary
            if result == []:
                # Error, there is no key in the dictionary
                raise Exception("Invalid json message. We cannot obtain the key: {}".format(key[0]))

            # The first time, I need to extract the next dictionary in a different way
            if cycle == 0:
                if isinstance(result[0], list):
                    result = result[0][0]
                else:
                    # Error, there is no key in the dictionary
                    raise Exception("Invalid json message. We expected "
                                    "'['contextResponses', 'context', 'attributes']' keys but obtain"
                                    " only '{}' key".format(key[0]))
            else:
                result = result[0]

            self.checkit(result, restkey, cycle + 1)
