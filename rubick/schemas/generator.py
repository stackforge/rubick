import argparse
import glob
import os.path
import logging
from collections import OrderedDict

import yaml

from rubick.common import index, Version, Issue
from rubick.schema import TypeValidatorRegistry as TypeRegistry
from rubick.schemas.yaml_utils import yaml_string, yaml_value


DIFF_THRESHOLD=0.5


logger = logging.getLogger('rubick.schemas.generator')


def yaml_dump_schema_records(records):
    lines = []

    for record in records:
        if len(record['added']) == 0 and len(record['removed']) == 0:
            continue

        lines.append('- version: %s' % yaml_string(str(record['version'])))
        if 'checkpoint' in record:
            lines.append('  checkpoint: %s' % yaml_value(record['checkpoint']))
        if 'added' in record and len(record['added']) > 0:
            lines.append('  added:')
            for param in record['added']:
                lines.append('')

                lines.append('  - name: %s' % yaml_string(param['name'], allowSimple=True))
                lines.append('    type: %s' % yaml_string(param['type'], allowSimple=True))
                if 'default' in param:
                    lines.append('    default: %s' % yaml_value(param['default']))
                if 'help' in param:
                    lines.append('    help: %s' % yaml_string(param['help']))

                extra_data = [k for k in param.keys()
                              if k not in ['name', 'type', 'default', 'help']]
                for attr in extra_data:
                    lines.append('    %s: %s' % (attr, yaml_value(param[attr])))

        if 'removed' in record and len(record['removed']) > 0:
            lines.append('  removed:')
            for removed in record['removed']:
                lines.append('  - %s' % yaml_string(removed, allowSimple=True))

        lines.append('')
        lines.append('# ====================================================')
        lines.append('')

    return "\n".join(lines)


def generate_project_schema(project):
    logger.info('Processing project %s' % project)
    project_path = os.path.join(os.path.dirname(__file__), project)

    files = glob.glob(os.path.join(project_path, '*.yml'))
    if files == []:
        logger.info("Found no YAML files in project %s. Skipping it" % project)
        return

    x = index(files, lambda f: f.endswith('.conf.yml'))
    if x != -1:
        database_file = files[x]
        del files[x]
    else:
        database_file = os.path.join(project_path, project+'.conf.yml')

    schema_records = []
    if os.path.exists(database_file):
        logger.debug("Processing database file %s" % database_file)
        with open(database_file) as f:
            schema_records.extend(yaml.load(f.read()))

    schema_versions = []
    for version_file in files:
        logger.debug("Processing version file %s" % version_file)
        with open(version_file) as f:
            schema_versions.append(yaml.load(f.read()))

    schema_versions = sorted(schema_versions, key=lambda s: Version(s['version']))

    parameters = OrderedDict()
    for schema in schema_versions:
        added = []

        seen = set()

        logger.debug('Processing schema version %s' % schema['version'])

        for param in schema['parameters']:
            prev_param = parameters.get(param['name'], None)

            if not prev_param:
                logger.debug('Parameter %s does not exist yet, adding it as new' % param['name'])
                added.append(param)
            else:
                seen.add(param['name'])

                if param['type'] != prev_param['type']:
                    validator = TypeRegistry.get_validator(prev_param['type'])
                    if param['type'] == validator.base_type:
                        param['type'] = prev_param['type']

                        if param.get('default', None) is not None:
                            value = validator.validate(param['default'])
                            if isinstance(value, Issue):
                                logger.error("In project '%s' version %s default value for parameter '%s' is not valid value of type %s: %s" %
                                            (project, schema['version'], param['name'], param['type'], repr(param['default'])))
                    else:
                        logger.debug('Parameter %s type has changed from %s to %s' %
                                    (param['name'], prev_param['type'], param['type']))
                        param['comment'] = 'Type has changed'
                        added.append(param)
                        continue

                if param.get('default', None) != prev_param.get('default', None):
                    logger.debug('Parameter %s default value has changed from %s to %s' %
                                (param['name'], prev_param['default'], param['default']))
                    param['comment'] = 'Default value has changed'
                    added.append(param)
                    continue

                if param.get('help', None) != prev_param.get('help', None):
                    param['comment'] = 'Help string has changed'
                    added.append(param)

        removed = [name for name in parameters.keys() if name not in seen]
        if len(removed) > 0:
            logger.debug('Following parameters from previous schema version are not present in current version, marking as removed: %s' % ','.join(removed))

        # Decide either to use full schema update or incremental
        changes_count = sum(map(len, [added, removed]))

        logger.debug('Found %d change(s) from previous version schema' % changes_count)

        if changes_count > int(len(parameters)*DIFF_THRESHOLD):
            logger.debug('Using full schema update')

            new_parameters = parameters.copy()
            for param in added:
                new_parameters[param['name']] = param
            for name in removed:
                del new_parameters[name]

            new_schema_record = dict(version=schema['version'],
                                     added=new_parameters.values(),
                                     removed=[],
                                     checkpoint=True)
        else:
            logger.debug('Using incremental schema update')

            new_schema_record = dict(version=schema['version'],
                                     added=added, removed=removed)

        # Place schema record either replacing existing one or appending as new
        old_schema_record_idx = index(
            schema_records, lambda r: str(r['version']) == str(new_schema_record['version']))

        if old_schema_record_idx != -1:
            old_schema_record = schema_records[old_schema_record_idx]
            # Collect information from existing records
            old_schema_parameters = {}
            for param in old_schema_record.get('added', []):
                old_schema_parameters[param['name']] = param

            for param in added:
                old_param = old_schema_parameters.get(param['name'], None)
                if not old_param:
                    if 'comment' not in param:
                        param['comment'] = 'New param'
                    continue

                extra_data = [(k, v) for k, v in old_param.items()
                                if k not in ['name', 'type', 'default', 'help']]
                param.update(extra_data)

                validator = TypeRegistry.get_validator(old_param['type'])
                if param['type'] not in [old_param['type'], validator.base_type]:
                    # Type has changed, enforcing old type to prevent accidental data loss
                    param['type'] = old_param['type']

                if param.get('default', None) is not None:
                    value = validator.validate(old_param['default'])
                    if isinstance(value, Issue):
                        logger.error("In project '%s' version %s default value for parameter '%s' is not valid value of type %s: %s" %
                                        (project, schema['version'], param['name'], param['type'], repr(param['default'])))

                if param.get('default', None) != old_param.get('default', None):
                    param['comment'] = 'Default value has changed'
                    continue

            logger.debug('Replacing schema record %s' % repr(new_schema_record))
            schema_records[old_schema_record_idx] = new_schema_record
        else:
            for param in added:
                if 'comment' not in param:
                    param['comment'] = 'New param'

            logger.debug('Appending schema record %s' % repr(new_schema_record))
            schema_records.append(new_schema_record)

        # Update parameter info
        for param in new_schema_record.get('added', []):
            parameters[param['name']] = param

        for name in new_schema_record.get('removed', []):
            del parameters[name]


    schema_records = sorted(schema_records,
                            key=lambda r: Version(r['version']))

    with open(database_file, 'w') as f:
        f.write(yaml_dump_schema_records(schema_records))


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', default='INFO', help='Loglevel to use')
    parser.add_argument('projects', nargs='*', help='Name of the projects (e.g. "nova")')
    args = parser.parse_args(argv[1:])
    return args


def main(argv):
    args = parse_args(argv)
    params = vars(args)

    logging.basicConfig(level=params['loglevel'])
    if 'project' in params:
        projects = [params['project']]
    else:
        projects = []
        for project_path in glob.glob(os.path.join(os.path.dirname(__file__), '*')):
            if not os.path.isdir(project_path):
                continue
            projects.append(os.path.basename(project_path))

    for project in projects:
        generate_project_schema(project)


if __name__ == '__main__':
    import sys
    main(sys.argv)
