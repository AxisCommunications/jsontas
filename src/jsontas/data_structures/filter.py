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
"""Filter datastructure."""
from copy import deepcopy
from .datastructure import DataStructure


class Filter(DataStructure):
    """Filter datastructure.

    Example::

        {
            "data": {
                "$filter": {
                    "items": [
                        {
                            "status": "success",
                            "value": "1"
                        },
                        {
                            "status": "failure",
                            "value": "2"
                        },
                        {
                            "status": "success",
                            "value": "3"
                        }
                    ],
                    "filters": [
                        {
                            "key": "status",
                            "operator": "$eq",
                            "value": "success"
                        }
                    ]
                }
            }
        }
        # {"data": [{"status": "success", "value": "1"}, {"status": "success", "value": "3"}]}
    """

    def filter(self, item):
        """Execute the filtering list against item.

        The filtering list is the list of key,operator,value dictionaries
        following the format of :obj:`jsontas.data_structures.operator.Operator`
        (in fact, the :obj:`jsontas.data_structures.operator.Operator` datastructure is
        used in this method to validate the filters)

        Note that when running the filter, the dataset is appended with an
        "item" which is a single item from the "items" filter list (can be seen above).

        The dataset could then be this::

            {
                **current_dataset,
                "item": { "status": "success", "value": "1"}
            }

        With the filter being::

            {
                "key": "status",
                "operator": "$eq",
                "value": "success"
            }

        And the filter would be True (the status of the item is 'success').
        Note that this method will only ever run on the "item". If there is
        not "$item" in the "key", the method will add it.
        That is why it's possible to write::

            {"key": "status"}

        instead of::

            {"key": "$item.status"}

        But it would also mean that if one were to write::

            {"key": "$anotherkey.something.else"}

        it would become::

            {"key": "$item.$anotherkey.something.else"}

        which would fail.

        This is a design choice. The filter shall not utilize any data aside
        from the 'item' key in the dataset.

        :param item: Item to filter.
        :type item: dict
        :return: Whether or not all items in filter evaluates to True.
        :rtype: bool
        """
        self.dataset.add("item", item)
        filters = deepcopy(self.data.get("filters"))
        for _filter in filters:
            key = _filter.get("key")
            if not key.startswith("$item."):
                key = "$item.{}".format(key)
                _, _filter["key"] = self.dataset.lookup(key, {})
            _, value = self.dataset.lookup("$operator", _filter)
            if not value:
                return False
        return True

    def execute(self):
        """Execute the filter datastructure.

        :return: Key and the value(s) found.
        :rtype: tuple
        """
        value = []
        if not isinstance(self.data.get("items"), (list, tuple, set)):
            return None, value
        for item in self.data.get("items", []):
            if self.filter(item):
                value.append(item)
        return None, value
