import argparse
import re
import sys


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('project',
                        help='Name of the project (e.g. "nova")')
    parser.add_argument('version',
                        help='Version of the project (e.g. "2013.1.3")')
    parser.add_argument('config_file',
                        help='Config file sample to process')
    args = parser.parse_args(argv[1:])
    return args


def generate_schema(project, version, config_file, schema_file=None):
    if not schema_file:
        schema_file = '%s_%s.py' % (project, version.replace('.', '_'))

    with open(config_file, 'r') as f:
        config_lines = f.readlines()

    conf_variable = '%s_%s' % (project, version.replace('.', '_'))
    with open(schema_file, 'w') as f:
        f.write("""from rubick.schema import ConfigSchemaRegistry

{0} = ConfigSchemaRegistry.register_schema(project='{0}')

with {0}.version('{1}') as {2}:""".format(project, version, conf_variable)
        )

        description_lines = []
        for line in config_lines:
            if line.startswith('['):
                section_name = line.strip('[]\n')
                f.write("\n\n    %s.section('%s')" % (
                    conf_variable, section_name))
                description_lines = []
                continue

            if line.strip() in ['', '#']:
                description_lines = []
                continue

            if line.startswith('# '):
                description_lines.append(line[2:].strip())
                continue

            description = ' '.join(description_lines)
            match = re.search('^(.*)\((.*?) value\)$', description)
            if match:
                description = match.group(1)
                param_type = match.group(2).strip()
                if param_type == 'floating point':
                    param_type = 'float'
            else:
                param_type = 'string'

            line = line.strip('#\n')
            param_name, param_value = [
                s.strip() for s in re.split('[:=]', line, 1)]

            # Normalizing param value and type
            if param_value == '<None>':
                param_value = None
            elif param_type == 'boolean':
                if param_value.lower() == 'false':
                    param_value = False
                elif param_value.lower() == 'true':
                    param_value = True
            elif param_type == 'integer':
                param_value = int(param_value)
                if param_name.endswith('_port'):
                    param_type = 'port'
            elif param_type == 'float':
                param_value = float(param_value)
            elif param_type == 'list':
                param_type = 'string_list'
                if param_value == '':
                    param_value = []
                else:
                    param_value = param_value.split(',')
            elif (param_type == 'string' and
                  param_name.endswith('_host') and
                  param_value in ['0.0.0.0', 'localhost', '127.0.0.1']):
                param_type = 'host'
            elif param_type == 'string' and param_name.endswith('_listen'):
                param_type = 'host'

            f.write("\n\n    %s.param('%s', type='%s', default=%s" % (
                conf_variable, param_name, param_type, repr(param_value)))
            f.write(", description=\"%s\"" % (
                description.replace('"', '\"')))
            f.write(")")


def main(argv):
    args = parse_args(argv)
    params = vars(args)

    project = params.pop('project')
    version = params.pop('version')
    config_file = params.pop('config_file')

    generate_schema(project, version, config_file)


if __name__ == '__main__':
    main(sys.argv)
