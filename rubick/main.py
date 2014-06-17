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
import logging
import sys


from rubick.inspection import MainConfigValidationInspection
from rubick.model_parser import ModelParser


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--debug',
        help='set debug log level',
        action='store_true')
    parser.add_argument('path', help='Path to config snapshot')

    args = parser.parse_args(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)

    model_parser = ModelParser()

    print('Analyzing configs in "%s"' % args.path)

    model = model_parser.parse(args.path)

    inspections = [MainConfigValidationInspection()]

    issues = []
    for inspection in inspections:
        issues.extend(inspection.inspect(model))

    if len(issues) == 0:
        print('No issues found')
    else:
        print('Found issues:')
        for issue in issues:
            print(issue)


if __name__ == '__main__':
    main(sys.argv[1:])
