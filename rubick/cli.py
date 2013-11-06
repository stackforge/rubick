import sys

sys.path = sys.path[1:]

import argparse
import requests
import json


def arg_parse():
    p = argparse.ArgumentParser(description='Rubick cli interface')
    p.add_argument('-l', '--list-clusters',
                   help='List clusters', default=None, action='store_true')
    p.add_argument('api', help='Api url', default=None)

    return p.parse_args()


def main():
    args = arg_parse()

    if (args.list_clusters):
        r = requests.get("%s/clusters" % args.api)
        if (r.status_code == requests.codes.ok):
            print "Avialable clusters:"
            for cluster in json.loads(r.text):
                print "\t%s (%d nodes)" % (
                    cluster['name'], len(cluster['nodes'])
                    )


if __name__ == '__main__':
    sys.exit(main())
