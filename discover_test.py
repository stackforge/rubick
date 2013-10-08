import logging
from itertools import groupby

from ostack_validator.common import Issue, MarkedIssue, Inspection
from ostack_validator.model import OpenstackComponent
from ostack_validator.discovery import OpenstackDiscovery
from ostack_validator.inspections import KeystoneAuthtokenSettingsInspection

def print_components(openstack):
  for host in openstack.hosts:
    print('Host %s (id = %s, addresses = %s):' % (host.name, host.id, host.network_addresses))
    for service in host.components:
      print('Service %s version %s config %s' % (service.name, service.version, service.config_path))
      service.config

      # print_service_config(service)

def print_service_config(service):
  if isinstance(service, OpenstackComponent):
    if service.config:
      for section, values in service.config.items():
        print('  [%s]' % section)
        for name, value in values.items():
          if value:
            print('    %s = %s' % (name, value))
    else:
      print('No config file found')
  else:
    print('Service is not an OpenStack component')

def print_issues(issues):
  # Filer only errors and fatal
  issues = [i for i in issues if i.type in [Issue.ERROR, Issue.FATAL]]

  if len(issues) == 0:
    print ('No issues found!')
    return

  issue_source_f = lambda i: i.mark.source if isinstance(i, MarkedIssue) else None
  source_groupped_issues = groupby(sorted(issues, key=issue_source_f), key=issue_source_f)

  for source, issues in source_groupped_issues:
    if source:
      print(source)
      for issue in sorted(issues, key=lambda i: i.mark.line):
        print('  [%s] %s (line %d column %d)' % (issue.type, issue.message, issue.mark.line+1, issue.mark.column+1))
    else:
      for issue in issues:
        print(issue)

def main():
  logging.basicConfig(level=logging.WARNING)
  logging.getLogger('ostack_validator').setLevel(logging.DEBUG)

  discovery = OpenstackDiscovery()
  with open('test_rsa') as f:
    private_key = f.read()

  openstack = discovery.discover(['172.18.65.179'], 'root', private_key=private_key)

  print_components(openstack)

  all_inspections = [KeystoneAuthtokenSettingsInspection]
  for inspection in all_inspections:
    x = inspection()
    x.inspect(openstack)

  print_issues(openstack.issues)

if __name__ == '__main__':
  main()

