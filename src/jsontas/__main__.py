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
"""Main module."""
import argparse
import sys
import logging
import json
from pprint import pprint

from jsontas import __version__
from jsontas.jsontas import JsonTas

__author__ = "Tobias Persson"
__copyright__ = "Tobias Persson"


def parse_args(args):
    """Parse command line parameters.

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="JSONTas - JSON generation language")
    parser.add_argument(
        "json_file"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output filename for the generated JSON."
    )
    parser.add_argument(
        "--dataset",
        "-d",
        help="Custom dataset file to use. Will be opened and read as JSON."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="jsontas {ver}".format(ver=__version__))
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Set up basic logging.

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Entry point allowing external calls.

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    jsontas = JsonTas()
    if args.dataset:
        with open(args.dataset) as json_file:
            dataset = json.load(json_file)
        jsontas.dataset.merge(dataset)

    data = jsontas.run(json_file=args.json_file)
    if args.output:
        with open(args.output, "w") as output_file:
            json.dump(data, output_file)
    else:
        pprint(data)


def run():
    """Entry point for console_scripts."""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
