import argparse
import logging
import sys


from ostack_validator.inspection import MainConfigValidationInspection
from ostack_validator.model_parser import ModelParser


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
