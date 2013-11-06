import argparse
import sys
from joker import Joker

def arg_parse():
    p = argparse.ArgumentParser(description = 'Joker cli interface')
    p.add_argument('-i', '--identity', help = 'Path to identity file', default = None)
    p.add_argument('-H', '--host', help = 'destination host')
    p.add_argument('-p', '--port', help = 'destination port', default = 22, type = int )
    p.add_argument('-u', '--user', help = 'username', default = "root" )
    p.add_argument('-P', '--password', help = 'username', default = None )
    return p.parse_args()

def main():
    args = arg_parse()

    print args

    j = Joker(args.identity)
    j.addNode("EntryPoint", args.host, args.port, args.user, args.password)

    print j.discover()


if __name__ == '__main__':
    sys.exit(main())

