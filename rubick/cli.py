import sys

#temporary workaround for rubick/json and system json modules
sys.path = sys.path[1:]

import argparse
import requests
import json

Api_url = None


def arg_parse():
    p = argparse.ArgumentParser(description='Rubick cli interface')
    p.add_argument('-l', '--list-clusters',
                   help='List clusters', default=None, action='store_true')
    p.add_argument('api', help='Api url', default=None)

    return p.parse_args()


def rubick_clusters_list():
    global Api_url

    r = requests.get("%s/clusters" % Api_url)
    code = 1

    if (r.status_code == requests.codes.ok):
        code = 0
        for cluster in json.loads(r.text):
            print 'Cluster: %s' % cluster['name']
            print '\tid: %s' % cluster['id']
            print '\tnodes: %s' % len(cluster['nodes'])
            print '\tdescription: %s' % cluster['description']

    return code


def main():
    args = arg_parse()
    global Api_url

    Api_url = args.api

    if (args.list_clusters):
        return rubick_clusters_list()


if __name__ == '__main__':
    sys.exit(main())
