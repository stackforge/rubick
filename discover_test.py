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
from flask import json
from itertools import groupby
import logging
import sys

from rubick.common import MarkedIssue, Inspection
from rubick.discovery import OpenstackDiscovery
import rubick.inspections     # noqa
import rubick.schemas         # noqa
from rubick.json import openstack_for_json


def indent_prefix(indent=0):
    s = ''
    if indent > 0:
        for i in range(0, indent):
            s += '  '
    return s


def print_issue(issue, indent=0):
    prefix = indent_prefix(indent)

    if hasattr(issue, 'mark'):
        print(
            '%s[%s] %s (line %d column %d)' %
            (prefix, issue.type, issue.message,
             issue.mark.line + 1, issue.mark.column + 1))
    else:
        print('%s[%s] %s' % (prefix, issue.type, issue.message))


def print_issues(issues, indent=0):
    issue_source_f = lambda i: i.mark.source if isinstance(
        i, MarkedIssue) else None
    source_groupped_issues = groupby(
        sorted(issues, key=issue_source_f), key=issue_source_f)

    for source, issues in source_groupped_issues:
        if source:
            print('%sFile %s' % (indent_prefix(indent), source))
            for issue in sorted(issues, key=lambda i: i.mark.line):
                print_issue(issue, indent + 1)
        else:
            for issue in issues:
                print_issue(issue, indent)


def print_service(service):
    print('    ' + service.name)
    print_issues(service.issues, indent=3)


def print_path(path):
    print('    ' + path.path)
    print_issues(path.all_issues, indent=3)


def print_host(host):
    print(host)

    print_issues(host.issues, indent=1)

    print('  Services:')

    for service in sorted(host.components, key=lambda c: c.name):
        print_service(service)

    print('  Filesystem:')

    for path in sorted(host.filesystem.values(), key=lambda f: f.path):
        print_path(path)


def print_openstack(openstack):
    print_issues(openstack.issues)

    for host in openstack.hosts:
        print_host(host)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', default='INFO',
                        help='Loglevel to use')
    parser.add_argument('-j', '--json', dest='json', default=False,
                        action='store_true',
                        help='Output result in JSON format')
    args = parser.parse_args(argv[1:])
    return args


def main(argv):
    args = parse_args(argv)
    params = vars(args)

    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('rubick').setLevel(params['loglevel'])

    discovery = OpenstackDiscovery()
    try:
        with open('test_rsa') as f:
            private_key = f.read()
    except Exception:
        private_key = sys.stdin.read()

    openstack = discovery.discover(
        ['172.18.65.179'],
        private_key=private_key)

    all_inspections = Inspection.all_inspections()
    for inspection in all_inspections:
        x = inspection()
        x.inspect(openstack)

    if params['json']:
        print(json.dumps(openstack_for_json(openstack)))
    else:
        print_openstack(openstack)

if __name__ == '__main__':
    main(sys.argv)
