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
"""Base datastructure."""

# pylint:disable=too-few-public-methods


class DataStructure:
    """Base datastructure class."""

    def __init__(self, jsonkey, datasubset, dataset, **data):
        """Initialize.

        :param jsonkey: Name of the key which this datastructure is handling.
        :type jsonkey: string
        :param datasubset: Datasubset which this datastructure is handling.
        :type datasubset: any
        :param dataset: Dataset object for adding new items to dataset.
        :type dataset: :obj:`jsontas.dataset.Dataset`
        :param data: Parameters in JSON 'below' this key.
        :type data: any
        """
        self.jsonkey = jsonkey
        self.datasubset = datasubset
        self.dataset = dataset
        self.data = data

    def execute(self):
        """Execute datastructure.

        Implement this.
        """
        raise NotImplementedError
