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
"""Operator datastructure."""
import re
from .datastructure import DataStructure

# pylint:disable=too-few-public-methods


class Operator(DataStructure):
    """Operator datastructure.

    Example::

        {
            "$operator": {
                "key": "key to match",
                "operator": "$eq",
                "value": "value to match against key"
            }
        }


    Supported operators:

    * :$eq: :obj:`_equal`
    * :$in: :obj:`_in`
    * :$notin: :obj:`_notin`
    * :$startswith: :obj:`_startswith`
    * :$regex: :obj:`_regex`

    .. document private functions
    .. automethod:: _equal
    .. automethod:: _in
    .. automethod:: _notin
    .. automethod:: _startswith
    .. automethod:: _regex
    """

    def __init__(self, *args, **kwargs):
        """Initialize.

        See :obj:`jsontas.data_structures.datastructure.DataStructure`
        """
        super().__init__(*args, **kwargs)
        self.operators = {
            "$eq": self._equal,
            "$in": self._in,
            "$notin": self._notin,
            "$startswith": self._startswith,
            "$regex": self._regex
        }
        self.key = self.data.get("key")
        self.value = self.data.get("value")
        self.operator = self.operators.get(self.data.get("operator"))

    def _equal(self):
        """Operator '=='.

        Example::

            {
                "$operator": {
                    "key": "key to match",
                    "operator": "$eq",
                    "value": "value to match against key"
                }
            }
        """
        return self.key == self.value

    def _in(self):
        """Operator 'in'.

        Example - In list::

            {
                "$operator": {
                    "key": "key",
                    "operator": "$in",
                    "value": ["key", "anotherkey"]
                }
            }

        Example - In string::

            {
                "$operator": {
                    "key": "k",
                    "operator": "$in",
                    "value": "key"
                }
            }
        """
        return self.key in self.value

    def _notin(self):
        """Operator 'not in'.

        Example - In list::

            {
                "$operator": {
                    "key": "key",
                    "operator": "$notin",
                    "value": ["key", "anotherkey"]
                }
            }

        Example - In string::

            {
                "$operator": {
                    "key": "k",
                    "operator": "$notin",
                    "value": "key"
                }
            }
        """
        return self.key not in self.value

    def _startswith(self):
        """Operator 'str.startswith()'.

        Example::

            {
                "$operator": {
                    "key": "key",
                    "operator": "$startswith",
                    "value": "k"
                }
            }
        """
        return self.key.startswith(self.value)

    def _regex(self):
        """Operator 're.match'.

        Example::

            {
                "$operator": {
                    "key": "key",
                    "operator": "$regex",
                    "value": "^[A-Za-z]+$"
                }
            }
        """
        match = re.match(self.value, self.key)
        return match is not None

    def execute(self):
        """Execute operator.

        :return: None and whether key matches value or not.
        :rtype: tuple
        """
        if self.operator is None:
            raise Exception("Unknown operator: %r" % self.operator)
        try:
            return None, self.operator()
        except:  # pylint: disable=bare-except
            return None, False
