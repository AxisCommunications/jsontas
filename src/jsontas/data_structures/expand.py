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
"""Expand datastructure."""
from copy import deepcopy
from .datastructure import DataStructure

# pylint:disable=too-few-public-methods


class Expand(DataStructure):
    """Expand datastructure.

    Expand a value into a list of a certain number of elements.

    Example::

        {
            "a_list": {
                "$expand": {
                    "value": {
                        "hello": "world"
                    },
                    "to": 5
                }
            }
        }

    Result::

        {
            "a_list": [
                {
                    "hello": "world"
                },
                {
                    "hello": "world"
                },
                {
                    "hello": "world"
                },
                {
                    "hello": "world"
                },
                {
                    "hello": "world"
                }
            ]
        }

    Example::

        {
            "another_list": {
                "$expand": {
                    "value": "something"
                    "to": 5
                }
            }
        }

    Result::

        {
            "another_list": [
                "something",
                "something",
                "something",
                "something",
                "something"
            ]
        }
    """

    def execute(self):
        """Execute expand.

        :return: None and a list of values.
        :rtype: tuple
        """
        # This is a circular import.
        # pylint:disable=cyclic-import
        # pylint:disable=import-outside-toplevel
        from jsontas.jsontas import JsonTas
        jsontas = JsonTas(self.dataset)
        query_tree = self.dataset.get("query_tree")
        amount = self.data.get("to", 0)

        evaluated = []
        for index in range(amount):
            value = deepcopy(query_tree.get("value"))
            self.dataset.add("expand_index", index)
            self.dataset.add("expand_value", value)
            evaluated.append(jsontas.resolve(json_data=value))
        return None, evaluated
