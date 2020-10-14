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
"""Request datastructure."""
import time
from json import JSONDecodeError
import traceback
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from .datastructure import DataStructure


class Request(DataStructure):
    """HTTP request datastructure.

    Example::

        {
            "$request" {
                "url": "http://localhost:8000/something.json",
                "method": "GET"
            }
        }

    Example::

        {
            "$request" {
                "url": "http://localhost:8000/something.json",
                "method": "POST",
                "json": {
                    "my_json": "hello"
                },
                "headers": {
                    "Content-Type": "application/json"
                },
                "auth": {
                    "username": "admin",
                    "password": "admin",
                    "type": "basic"
                }
            }
        }

    Example getting response after::

        # Assume response from request is: {"hello": "world"}
        {
            "data": {
                "$request" {
                    "url": "http://localhost:8000/something.json",
                    "method": "GET"
                }
            },
            "text": "$response.json.hello"
        }
        # Resulting JSON will be:
        {
            "data": {
                "hello": "world"
            },
            "text": "world"
        }
    """

    @staticmethod
    def wait(method, timeout=None, interval=5, **kwargs):
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
                yield method(**kwargs)
            except Exception as exception:  # pylint:disable=broad-except
                if isinstance(exception, GeneratorExit):
                    break
                traceback.print_exc()
            time.sleep(interval)

    @staticmethod
    def __auth(username, password, type="basic"):  # pylint:disable=redefined-builtin
        """Create an authentication for HTTP request.

        :param username: Username to authenticate.
        :type username: str
        :param password: Password to authenticate with.
        :type password: str
        :param type: Type of authentication. 'basic' or 'digest'.
        :type type: str
        :return: Authentication method.
        :rtype: :obj:`requests.auth`
        """
        # TODO: Handle encrypted passwords.
        if type.lower() == "basic":
            return HTTPBasicAuth(username, password)
        return HTTPDigestAuth(username, password)

    def request(self, url, method, json=None, headers=None, **requests_parameters):
        """Make an HTTP request.

        :param url: URL to request.
        :type url: str
        :param method: HTTP method.
        :type method: str
        :param json: Optional JSON data to request.
        :type json: dict
        :param headers: Optional extra headers to request.
        :type headers: dict
        :param requests_parameters: Extra parameters to python requests.
        :type requests_parameters: dict
        :return: Wait generator for getting responses from request.
        :rtype: generator
        """
        requests_parameters["timeout"] = requests_parameters.get("timeout", 10)
        if requests_parameters.get("auth"):
            requests_parameters["auth"] = self.__auth(**requests_parameters["auth"])

        request = getattr(requests, method.lower())
        requests_parameters["url"] = url
        requests_parameters["json"] = json
        requests_parameters["headers"] = headers
        return self.wait(request, **requests_parameters)

    def execute(self):
        """Execute data.

        :return: None and response as JSON (or None).
        :rtype: Tuple
        """
        response_generator = self.request(**self.data)
        response = None
        data = None
        value = None
        for response in response_generator:
            data = {
                "status_code": response.status_code,
                "reason": response.reason,
                "headers": response.headers,
                "cookies": response.cookies,
                "content": response.content,
                "encoding": response.encoding,
                "is_permanent_redirect": response.is_permanent_redirect,
                "is_redirect": response.is_redirect,
                "links": response.links,
                "ok": response.ok,
                "url": response.url,
                "json": None
            }
            if response.headers.get("Content-Type") == "application/json":
                try:
                    value = response.json()
                    data["json"] = value
                except JSONDecodeError:
                    pass
            break
        self.dataset.add("response", data)
        return None, data
