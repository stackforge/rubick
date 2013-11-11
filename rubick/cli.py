import sys

# temporary workaround for rubick/json and system json modules
sys.path = sys.path[1:]

import argparse
import json
import requests

Api_url = None
Debug = None


def arg_parse():
    p = argparse.ArgumentParser(description='Rubick cli interface')
    p.add_argument('-l', '--list-cluster',
                   help='List clusters', default=None, action='store_true')
    p.add_argument('-a', '--add-cluster',
                   help='Add cluster', default=None, action='store_true')
    p.add_argument('-v', '--verbose',
                   help='More verbose', default=None, action='store_true')
    p.add_argument('-i', '--id',
                   help='Specify cluster id', default=None)

    p.add_argument('-n', '--name',
                   help='Cluster name', default=None)
    p.add_argument('-d', '--description',
                   help='Cluster description', default=None)

    p.add_argument('-H', '--host',
                   help='Entry point host in cluster', default=None)

    p.add_argument('-k', '--key',
                   help='Identity key', default=None)

    p.add_argument('api', help='Api url', default=None)

    return p.parse_args()


def cli_debug(debug_data):
    global Debug
    if (Debug):
        print "*** " + debug_data


def rubick_cluster_show(cluster):
    print 'Cluster: %s' % cluster['name']
    print '\tid: %s' % cluster['id']
    print '\tnodes: %s' % len(cluster['nodes'])
    print '\tdescription: %s' % cluster['description']


def rubick_request_get(uri):
    global Api_url
    cli_debug("Get request %s " % (Api_url + uri))
    return requests.get(Api_url + uri)


def rubick_request_post(uri, payload_data):
    global Api_url
    cli_debug("POST request %s " % (Api_url + uri))
    cli_debug("POST data %s " % payload_data)
    return requests.post(Api_url + uri, json.dumps(payload_data))


def rubick_cluster_list(cluster_id):

    request_url = "/clusters%s" % ("/" + cluster_id if (cluster_id) else "")

    #r = requests.get(request_url)
    r = rubick_request_get(request_url)

    code = 1

    if (r.status_code == requests.codes.ok):
        code = 0

        if (cluster_id is None):
            json_data = json.loads(r.text)
        else:
            # for single output interface
            json_data = [json.loads(r.text)]

        for cluster in json_data:
                rubick_cluster_show(cluster)

    return code


def rubick_cluster_add(name, description, host, key):
    if (not bool(name) or not bool(description) or not(host) or not(key)):
        # usage error
        return 1

    try:
        with open(key) as f:
            keyData = f.read()
    except IOError:
        return 1

    request_payload = {
        "description":  description,
        "name": name,
        "nodes": host,
        "private_key": keyData
    }

    r = rubick_request_post("/clusters", request_payload)
    print r


def main():
    global Api_url, Debug

    args = arg_parse()

    Api_url = args.api
    Debug = args.verbose

    if (args.list_cluster):
        return rubick_cluster_list(args.id)

    if (args.add_cluster):
        return rubick_cluster_add(
            args.name, args.description, args.host, args.key)


if __name__ == '__main__':
    sys.exit(main())
