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
"""JSONTas module."""
import json
import logging
from collections import OrderedDict
from copy import deepcopy
from jsontas.dataset import Dataset


class JsonTas:
    """JSONTas resolver."""

    logger = logging.getLogger("JSONTas")

    def __init__(self, dataset=None):
        """Initialize dataset.

        :param dataset: In order to provide a custom dataset class.
        :type dataset: :obj:`jsontas.dataset.Dataset`
        """
        if dataset is not None:
            self.dataset = dataset
        else:
            self.dataset = Dataset()

    @staticmethod
    def __get_key(key, dictionary):
        """Get a key from parent dictionary if possible.

        If key does not exist, return either the dictionary supplied or an empty dictionary.

        :param key: Key to get from dictionary.
        :type key: any
        :param dictionary: Dictionary to get key from.
        :type dictionary: dict
        :return: Value from dictionary.
        :rtype: dict
        """
        try:
            parameters = dictionary[key]
        except TypeError:
            parameters = dictionary
            if dictionary is None:
                parameters = {}
        return parameters

    def __resolve(self, query_string, parent=None):
        """Resolve a JSONTas query string against dataset.

        :param query_string: Query string to resolve.
        :type query_string: string
        :param parent: Parent dictionary where the query_string resides.
        :type parent: any
        :return: Resolved key and value pairs. Or the key and value pair already set.
        :rtype: tuple
        """
        value = None
        key = query_string
        if isinstance(query_string, str) and query_string.startswith("$"):
            self.logger.debug("Executing JSONTas query %r", query_string)
            parameters = self.__get_key(query_string, parent)
            key, value = self.dataset.lookup(query_string, parameters)
        return key, value

    def __resolve_dict(self, json_data, query_tree):
        """Resolve a dictionary in the JSONTas resolver.

        Create a new dictionary.
        Iterate through all json_data items.
        Resolve all items and add to new dictionary.
        Return new dictionary.

        :param query_tree: Keep track of the current query_tree. I.e. the full, unresolved,
                           JSON structure that is currently being resolved.
        :type query_tree: dict
        :param json_data: JSON dictionary to resolve.
        :type json_data: dict
        :return: Newly created dict with resolved values.
        :rtype: dict
        """
        query_tree.update(**deepcopy(json_data))
        new = json_data.__class__()
        for key, value in json_data.items():
            # It's important that the 'resolve' call is before the '__resolve' call.
            # This will make sure that the lowest values in dictionary are resolved
            # first.
            # Example: {"$something": {"$somethingelse": "text"}}
            # In this case "$somethingelse" will be resolved before "$something".
            self.logger.debug("Resolve sub-elements.")
            value = self.resolve(value, query_tree[key])
            self.logger.debug("Resolved value: %r", value)
            json_data[key] = value
            self.dataset.add("query_tree", query_tree[key])
            key, new_value = self.__resolve(key, json_data)
            if key is None:
                new = new_value
            else:
                if new_value is None:
                    new[key] = value
                else:
                    new[key] = new_value
        return new

    def __resolve_list(self, json_data, query_tree):
        """Resolve a list in the JSONTas resolver.

        Create a new list.
        Iterate through all json_data items.
        Resolve all items and add to new list.
        Return new list.

        :param query_tree: Keep track of the current query_tree. I.e. the full, unresolved,
                           JSON structure that is currently being resolved.
        :type query_tree: list
        :param json_data: JSON list to resolve.
        :type json_data: tuple, set or list
        :return: Newly created list with resolved values.
        :rtype: list
        """
        return json_data.__class__(self.resolve(value, query_tree[index])
                                   for index, value in enumerate(json_data))

    def resolve(self, json_data, query_tree=None):
        """Resolve JSONTas queries. Takes a JSON structure and resolve all values against dataset.

        This is a recursive method.

        :param json_data: JSON data to iterate through and resolve.
        :type json_data: any
        :param query_tree: Used in recursion to keep track of query_tree.
        :type query_tree: any
        :return: New JSON structure with resolved values.
        :rtype: any
        """
        if query_tree is None:
            query_tree = {}
        if isinstance(json_data, dict):
            self.logger.debug("Resolving dictionary %r.", json_data)
            new = self.__resolve_dict(json_data, query_tree)
        elif isinstance(json_data, (list, set, tuple)):
            self.logger.debug("Resolving list %r.", json_data)
            new = self.__resolve_list(json_data, query_tree)
        else:
            self.logger.debug("Resolving primitive %r.", json_data)
            key, new_value = self.__resolve(json_data)
            if new_value is None:
                return key
            return new_value
        return new

    def run(self, json_data=None, json_file=None, copy=True):
        """Run JSONTas. This should be the main entry to JSONTas.

        :param json_data: JSON data to run JSONTas on.
        :type json_data: :obj:`OrderedDict`
        :param json_file: JSON file to run JSONTas on.
        :type json_data: file
        :return: Resolved JSON structure.
        :rtype: :obj:`OrderedDict`
        """
        assert json_data is not None or json_file is not None, \
            "Must supply either 'json_data' or 'json_file'"
        if json_file:
            self.logger.debug("Loading JSON file.")
            with open(json_file) as _file:
                json_data = json.load(_file, object_pairs_hook=OrderedDict)
        if copy:
            self.logger.debug("Deepcopy JSON.")
            json_data = deepcopy(json_data)
        assert isinstance(json_data, OrderedDict), "JSON data must be an OrderedDict"

        self.logger.debug("Adding JSON to dataset.")
        self.dataset.add("this", json_data)
        self.logger.debug("Starting resolver.")
        return self.resolve(json_data)
