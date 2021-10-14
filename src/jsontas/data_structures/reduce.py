# Copyright 2020-2021 Axis Communications AB.
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
"""Reduce datastructure."""
from jsontas.data_structures.datastructure import DataStructure

# pylint:disable=too-few-public-methods


class Reduce(DataStructure):
    """Reduce a list from end to beginning (from right) to a specific value
    
    Example::

        {
            "reduced_list": {
                "$reduce": {
                    "value": [
                        "element 1",
                        "element 2",
                        "element 3"
                    ],
                    "to": 2
                }
            }
        }

    Result::

        {
            "reduced_list": [
                "element 1",
                "element 2"
            ]
        }
    
    """

    def execute(self):
        """Execute reduce.

        :return: None and a list of values.
        :rtype: tuple
        """
        _list = self.data.get("list")
        reduce_to_value = self.data.get("to", 1)
        reduced_list = _list[:reduce_to_value]
        return None, reduced_list