import sys

#temporary workaround for rubick/json and system json modules
sys.path = sys.path[1:]

import argparse
import requests
import json

Api_url = None
Debug = None


def arg_parse():
    p = argparse.ArgumentParser(description='Rubick cli interface')
    p.add_argument('-l', '--list-clusters',
                   help='List clusters', default=None, action='store_true')
    p.add_argument('-d', '--debug',
                   help='Debug data', default=None, action='store_true')
    p.add_argument('-i', '--id',
                   help='Specify cluster id', default=None)
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


def rubick_request_get(url):
    cli_debug("Get request %s " % url)
    return requests.get(url)


def rubick_clusters_list(cluster_id):
    global Api_url

    request_url = "%s/clusters%s" % (
        Api_url, "/" + cluster_id if (cluster_id) else "")


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


def main():
    global Api_url, Debug

    args = arg_parse()

    Api_url = args.api
    Debug = args.debug


    if (args.list_clusters):
        return rubick_clusters_list(args.id)


if __name__ == '__main__':
    sys.exit(main())
