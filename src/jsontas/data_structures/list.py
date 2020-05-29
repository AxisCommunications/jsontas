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
"""List datastructure."""
from .datastructure import DataStructure


class List(DataStructure):
    """List datastructure.

    Not to be used directly in JSON structure.
    Use it with the .int operator.

    :obj:`index` - Index 0::

        {
            "something": "$value.0"
        }

    :obj:`index` - Last index::

        {
            "something": "$value.-1"
        }

    :obj:`slice` - Everything after index 1::

        {
            "something": "$value.1:"
        }

    :obj:`slice` - Everything before index 4::

        {
            "something": "$value.:4"
        }

    :obj:`slice` - Everything between index 2 and 4::

        {
            "something": "$value.2:4"
        }
    """

    @staticmethod
    def split(value):
        """Split a string on ':' and return first and second value.

        :param value: Value to split.
        :type value: str
        :return: First and second value. Any of them can be None.
        :rtype: tuple
        """
        first, second = None, None
        sliced = value.split(":")
        try:
            first = int(sliced[0])
        except ValueError:
            pass
        try:
            second = int(sliced[1])
        except (IndexError, ValueError):
            pass
        return first, second

    @staticmethod
    def slice(data, first, second):
        """Slice a string based on first and second integers.

        :param data: Data to get slice from.
        :type data: list, set or tuple
        :param first: Number to put before ':' if not None.
        :type first: int or None
        :param second: Number to put after ':' if not None.
        :type second: int or None.
        :return: Sliced list.
        :rtype: list
        """
        sliced = None
        if first is None:
            sliced = data[:second]
        elif second is None:
            sliced = data[first:]
        else:
            sliced = data[first:second]
        return sliced

    @staticmethod
    def index(data, index):
        """Get an index from data.

        :param data: Data to get index from.
        :type data: list, set or tuple
        :param index: Index to get.
        :type index: int
        :return: Value on index.
        :rtype: any
        """
        return data[index]

    def execute(self):
        """Execute the list datastructure.

        :return: Key and the value(s) found.
        :rtype: tuple
        """
        if ":" in self.jsonkey:
            value = self.slice(self.datasubset, *self.split(self.jsonkey))
        else:
            value = self.index(self.datasubset, int(self.jsonkey))
        return self.jsonkey, value
