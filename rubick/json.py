__all__ = ['openstack_for_json']


def json_issues(issues):
    return [str(issue) for issue in issues]


def json_component(component):
    result = dict(type='component', name=component.name)

    if len(component.all_issues) > 0:
        result['issues'] = json_issues(component.all_issues)

    return result


def json_host(host):
    result = dict(type='host', name=host.name,
                  addresses=host.network_addresses,
                  components=[json_component(c) for c in host.components])
    if len(host.issues) > 0:
        result['issues'] = json_issues(host.issues)

    return result


def json_openstack(openstack):
    result = dict(type='openstack',
                  hosts=[json_host(host) for host in openstack.hosts])
    if len(openstack.issues) > 0:
        result['issues'] = json_issues(openstack.issues)

    return result


def openstack_for_json(openstack):
    return json_openstack(openstack)
