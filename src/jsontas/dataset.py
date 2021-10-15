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
"""Dataset module."""
import re
import logging
import traceback
import inspect
from copy import deepcopy
from jsontas.data_structures import Condition, Operator, List, Request, Filter, From, Expand, Wait, Reduce
from jsontas.data_structures.datastructure import DataStructure


class Dataset:
    """JSONTas dataset object. Used for lookup of $ notated strings in a JSON file."""

    logger = logging.getLogger("Dataset")
    # Split value into words separated by anything except ','
    regex = re.compile(r"[\$\-\w!,:]+")

    def __init__(self):
        """Create an initial dataset of the data structures."""
        self.__dataset = {
            "condition": Condition,
            "operator": Operator,
            "list": List,
            "request": Request,
            "filter": Filter,
            "expand": Expand,
            "from": From,
            "wait": Wait,
            "reduce": Reduce
        }

    def add(self, key, value):
        """Add a new dataset value and key.

        :param key: Dictionary key for global dataset dict.
        :type key: str
        :param value: Dictionary value for global dataset dict.
        :type value: any
        """
        self.__dataset[key] = value

    def merge(self, dataset):
        """Merge a dataset with this dataset.

        :param dataset: Dataset to merge with this one.
        :type dataset: dict
        """
        self.__dataset.update(**dataset)

    def copy(self):
        """Make a copy of this dataset.

        :return: A dataset object with a copy of the internal dataset in it.
        :rtype: :obj:`Dataset`
        """
        copied_dataset = deepcopy(self.__dataset)
        copy = Dataset()
        copy.merge(copied_dataset)
        return copy

    def get(self, key, default=None):
        """Get a key from dataset global dictionary.

        :param key: Key to get from global dataset dictionary.
        :type key: any
        :param default: Default value if the key does not exist.
        :type default: any
        :return: Value from key in global dataset dictionary or default.
        :rtype: any
        """
        return self.__dataset.get(key, default)

    def __iterate(self, key):
        """Create an iterator from dataset regex against a JSONTas query string.

        :param key: JSONTas query string to evaluate.
        :type key: str
        :return: Generator for all values in JSONTas query string.
        :rtype: generator
        """
        values = self.regex.findall(key)
        self.logger.debug("Query split : %r", values)
        yield from values

    def get_or_getattr(self, datasubset, key):
        """Get a key from a datasubset. Either using 'get' or 'getattr'.

        :raises: AttributeError if attribute could not be found with either 'get' or 'getattr'.
        :param datasubset: Dataset to attempt to get key from.
        :type datasubset: any
        :param key: Key to get.
        :type key: any
        :return: Value from key.
        :rtype: any
        """
        try:
            if isinstance(datasubset, (list, set, tuple)):
                _, value = List(key, datasubset, self).execute()
            else:
                value = datasubset.get(key)
        except (AttributeError, ValueError):
            if hasattr(datasubset, key):
                value = getattr(datasubset, key)
            else:
                value = None
        return value

    def lookup(self, query_string, parameters):
        """Lookup JSONTas query string against dataset.

        Query string is a dot separated string of keywords which is split and iterated over.

        If the query string is "$something.another.third"::

            # Iterate through the words
            ["something", "another", "third"]

        These keywords are then matched against the dataset very simply

        1. Try to get keyword from dataset, either via ".get" or "getattr".
        2. If keyword exists, inspect what the type of the keyword value is.
        3. If it's a :obj:`jsontas.data_structures.datastructure.DataStructure`, call its 'execute'
           method with the parameters and keyword value.
        4. If it's a function, call the function with the parameters and keyword value.
        5. If neither of the above are True, set dataset to the value.
        6. Loop to the next keyword.

        If at any point of this, the keyword value becomes None, return without changing the key.
        (the key is, by default, the query_string)

        If the keyword value is not None after the loop is finished, return the key and value.
        Note that the :obj:`jsontas.data_structures.datastructure.DataStructure` and functions
        must return a key, value pair.

        Value will be put as the 'value' in the JSON dict when returned, key is what the key will
        be changed to.

        Assume the following dataset for the JSON below::

            {
                "query": {
                    "call": "Chaos"
                }
            }

        Input::

            {
                "Text": "$query.call"
            }

        Output::

            {
                "Text": "Chaos"
            }

        In most cases, as well as in these examples, the key returned is None.
        It is expected that the caller handles this situation by setting the
        correct key when None is returned.

        The "correct" key is generally the key that was already there. In the examples
        above the the key is "Text", and this method returns None, so JSONTas will keep
        the key as 'Text'

        However, if the key returned is not None, the key is overwritten by JSONTas.
        This is not a very common use-case, but it is possible to implement in a
        :obj:`jsontas.data_structures.datastructure.DataStructure`

        This should be used with care!
        In fact, the only built-in use-case for this behavior is when there's an
        exception in the lookup or the keyword value becomes None at any point in
        order to have the key stay as the query_string in case of problems.

        :param query_string: JSONTas query string.
        :type query_string: str
        :param parameters: Parameters that exist nested below the query_string in JSON data.
                           For instance {"$querystring": {"some": "data"}} parameters would be
                           {"some": "data"}
        :type parameters: any
        :return: New key and value as defined by dataset.
        :rtype: tuple
        """
        self.logger.debug("Query string: %r", query_string)
        self.logger.debug("Parameters  : %r", parameters)
        value = None
        key = query_string
        datasubset = self.__dataset
        iterator = self.__iterate(query_string[1:])
        try:
            for jsonkey in iterator:
                self.logger.debug("Datasubset  : %r", datasubset)
                self.logger.debug("Evaluating  : %r", jsonkey)
                value = self.get_or_getattr(datasubset, jsonkey)
                self.logger.debug("Value       : %r", value)
                if value is None and isinstance(datasubset, (list, set, tuple)):
                    self.logger.debug("Getting attributes from list.")
                    value = [self.get_or_getattr(list_value, jsonkey)
                             for list_value in datasubset]
                    if all([item is None for item in value]):
                        self.logger.debug("All attributes are None.")
                        self.logger.debug("Exiting lookup.")
                        value = None
                        key = None
                        break
                elif value is None:
                    self.logger.debug("Exiting lookup.")
                    key = query_string
                    break

                # pylint: disable=unidiomatic-typecheck
                # Since value is never an instance at this point, a type check is mandatory.
                if inspect.isclass(value) and type(value) == type(DataStructure):
                    self.logger.debug("Evaluating value as DataStructure")
                    key, value = value(jsonkey, datasubset, self, **parameters).execute()
                elif inspect.isfunction(value):
                    self.logger.debug("Evaluating value as function")
                    key, value = value(jsonkey, datasubset, self, **parameters)
                else:
                    self.logger.debug("Continue with datasubset as value.")
                    key = None
                    datasubset = value
        except:  # noqa, pylint:disable=bare-except
            self.logger.warning(traceback.format_exc())
        self.logger.debug("Returning   : %r, %r", key, value)
        self.add("previous", value)
        return key, value
