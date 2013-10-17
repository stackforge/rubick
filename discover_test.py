import logging
from itertools import groupby

from ostack_validator.common import Issue, MarkedIssue, Inspection
from ostack_validator.model import OpenstackComponent
from ostack_validator.discovery import OpenstackDiscovery
from ostack_validator.inspections import KeystoneAuthtokenSettingsInspection, KeystoneEndpointsInspection, LettuceRunnerInspection


def indent_prefix(indent=0):
    s = ''
    if indent > 0:
        for i in xrange(0, indent):
            s += '  '
    return s


def print_issue(issue, indent=0):
    prefix = indent_prefix(indent)

    if hasattr(issue, 'mark'):
        print(
            '%s[%s] %s (line %d column %d)' %
            (prefix, issue.type, issue.message, issue.mark.line + 1, issue.mark.column + 1))
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
    print('  ' + str(service))
    print_issues(service.all_issues, indent=2)


def print_host(host):
    print(host)

    print_issues(host.issues, indent=1)

    for service in host.components:
        print_service(service)


def print_openstack(openstack):
    print_issues(openstack.issues)

    for host in openstack.hosts:
        print_host(host)


def main():
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('ostack_validator').setLevel(logging.DEBUG)

    discovery = OpenstackDiscovery()
    with open('test_rsa') as f:
        private_key = f.read()

    openstack = discovery.discover(
        ['172.18.65.179'],
        'root',
        private_key=private_key)

    all_inspections = [
        KeystoneAuthtokenSettingsInspection,
        KeystoneEndpointsInspection,
        LettuceRunnerInspection]
    for inspection in all_inspections:
        x = inspection()
        x.inspect(openstack)

    print_openstack(openstack)

if __name__ == '__main__':
    main()
