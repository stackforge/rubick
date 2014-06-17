# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
import argparse
from joker import Joker
import sys


def arg_parse():
    p = argparse.ArgumentParser(description='Joker cli interface')
    p.add_argument('-i', '--identity', help='Path to identity file',
                   default=None)
    p.add_argument('-H', '--host', help='destination host')
    p.add_argument('-p', '--port', help='destination port', default=22,
                   type=int)
    p.add_argument('-u', '--user', help='username', default="root")
    p.add_argument('-P', '--password', help='username', default=None)
    return p.parse_args()


def main():
    args = arg_parse()

    print args

    j = Joker(args.identity)
    j.addNode("EntryPoint", args.host, args.port, args.user, args.password)

    print j.discover()


if __name__ == '__main__':
    sys.exit(main())
