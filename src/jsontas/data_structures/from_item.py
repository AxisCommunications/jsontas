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
"""From datastructure."""
from .datastructure import DataStructure

# pylint:disable=too-few-public-methods


class From(DataStructure):
    """From datastructure.

    Example::

        {
            "hello" {
                "$from": {
                    "item": {
                        "value": "something",
                        "text": "world"
                    },
                    "get": "text"
                }
            }
        }
        # {"hello": "world"}
    """

    def execute(self):
        """Execute the $from datastructure.

        :return: Key and the value(s) found.
        :rtype: tuple
        """
        self.dataset.add("item", self.data.get("item"))
        query = self.data.get("get")
        if query is None:
            return self.jsonkey, None
        if not query.startswith("$item."):
            query = "$item.{}".format(query)
        _, value = self.dataset.lookup(query, {})
        return None, value
