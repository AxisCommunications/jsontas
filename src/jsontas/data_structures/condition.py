# Copyright 2020 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Condition datastructure."""
from .datastructure import DataStructure
from .operator import Operator

# pylint:disable=too-few-public-methods


class Condition(DataStructure):
    """Condition datastructure.

    Example::

        {
            "$condition": {
                "if": {
                    "key": "Key to match",
                    "operator": "$eq",
                    "value": "something",
                },
                "then": "returnvalue",
                "else": "Default value"
            }
        }

    Example::

        {
            "$condition": {
                "if": [
                    {
                        "key": "Key to match",
                        "operator": "$eq",
                        "value": "something",
                    },
                    {
                        "key": "Another key to match",
                        "operator": "$in",
                        "value": "somethingelse"
                    }
                ],
                "then": "returnvalue",
                "else": "Default value"
            }
        }

    Supported operators defined here: :obj:`jsontas.data_structures.operator.Operator`

    .. document private functions
    .. automethod:: _if
    .. automethod:: _else
    """

    def _if(self, operator):
        """If operator.

        :param operator: Data to check "if" on.
        :type operator: dict
        :return: Operator result.
        :rtype: bool
        """
        if isinstance(operator, (list, set, tuple)):
            for sub_operator in operator:
                if not Operator(self.jsonkey, self.datasubset, self.dataset,
                                **sub_operator).execute()[1]:
                    return False
            else:  # pylint:disable=useless-else-on-loop
                return True
        return Operator(self.jsonkey, self.datasubset, self.dataset, **operator).execute()[1]

    @staticmethod
    def _else(data):
        """Else operator. Just return the data.

        Note that this method is added for readability in :obj:`execute` only.

        :param data: Data to just return.
        :type data: any
        :return: Condition.
        :rtype: str
        """
        return data

    def execute(self):
        """Execute data.

        :return: None and value from either 'else' or 'then'.
        :rtype: tuple
        """
        _if = self.data.get("if")
        _else = self.data.get("else")
        _then = self.data.get("then")
        if self._if(_if):
            return None, _then
        return None, self._else(_else)
