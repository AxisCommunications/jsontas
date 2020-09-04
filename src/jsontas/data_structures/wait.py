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
"""Wait datastructure."""
import time
from copy import deepcopy
from .datastructure import DataStructure


class Wait(DataStructure):
    """Wait datastructure.

    Wait for a query tree to evaluate to True.

    Example::

        {
            "$wait": {
                "for": {
                    "$request": {
                        "url": "http://example.com",
                        "method": "GET"
                    }
                },
                "interval": 1,
                "timeout": 20,
                "else": {}
            }
        }

    Request example.com until a non-null response. Maximum 1 request/s for 20s

    Due to the storage of the 'query_tree' in dataset it is possible to nest queries::

    Example::

        {
            "response": {
                "$from": {
                    "item": {
                        "$wait": {
                            "for": {
                                "$condition": {
                                    "then": {
                                        "$request": {
                                            "url": "http://example.com",
                                            "method": "GET"
                                        }
                                    },
                                    "if": {
                                        "key": "$response.status_code",
                                        "operator": "$eq",
                                        "value": 200
                                    },
                                    "else": null
                                }
                            },
                            "interval": 1,
                            "timeout": 20,
                            "else": {}
                        }
                    },
                    "get": "items"
                }
            }
        }

    Wait for example.com to respond with status_code 200 and a non-null response and get the
    'items' key from the response. Maximum 1 request/s for 20s
    """

    @staticmethod
    def wait(method, timeout, interval, **kwargs):
        """Iterate over result from method call.

        :param method: Method to call.
        :type method: :meth:
        :param timeout: How long, in seconds, to iterate.
        :type timeout: int or None
        :param interval: How long, in seconds, to wait between method calls.
        :type interval: int
        :param kwargs: Keyword arguments to pass to method call.
        :type kwargs: dict
        """
        end = time.time() + timeout
        while time.time() < end:
            try:
                yield method(**deepcopy(kwargs))
            except GeneratorExit:
                break
            except:  # pylint:disable=bare-except
                continue
            time.sleep(interval)

    def execute(self):
        """Execute wait datastructure.

        Waiting for will requires a 'query_tree' which is a collection of all requests
        that are 'below' the 'wait' datastructure. This is to keep track of the queries
        that have executed before (but not the results of these queries).

        This query tree is then executed in the :meth:`jsontas.jsontas.JsonTas.resolve` method,
        which can be considered weird. We're executing JsonTas inside of a JsonTas query.
        But this is the only way to re-run a query tree.

        :return: None and the result of re-running a query tree.
        :rtype: Tuple
        """
        if self.data.get("for"):
            return None, self.data.get("for")
        # This is a circular import.
        # pylint:disable=cyclic-import
        # pylint:disable=import-outside-toplevel
        from jsontas.jsontas import JsonTas
        jsontas = JsonTas(self.dataset)
        value = None
        query_tree = self.dataset.get("query_tree")
        for value in self.wait(jsontas.resolve,
                               self.data.get("timeout"),
                               self.data.get("interval"),
                               json_data=query_tree.get("for")):
            if value:
                break
        return None, value or self.data.get("else")
