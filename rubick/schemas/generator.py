import argparse
import re
import sys
import os
import imp
import traceback
from copy import copy

from oslo.config import cfg


def identity(x):
    return x

__builtins__._ = identity


class SchemaBuilderSchemaWriter(object):
    def __init__(self, file, project, version):
        super(SchemaBuilderSchemaWriter, self).__init__()
        self.file = file
        self.project = project
        self.version = version
        self._started = False
        self._conf_variable = '%s_%s' % (self.project,
                                         self.version.replace('.', '_'))

    def _ensure_header(self):
        if not self._started:
            self._output_header()
            self._started = True

    def _output_header(self):
        self.file.write("""from rubick.schema import ConfigSchemaRegistry

{0} = ConfigSchemaRegistry.register_schema(project='{0}')

with {0}.version('{1}') as {2}:""".format(self.project, self.version,
                                          self._conf_variable))

    def section(self, name):
        self._ensure_header()
        self.file.write("\n\n    %s.section('%s')" % (
            self._conf_variable, name))

    def param(self, name, type, default_value=None, description=None):
        self._ensure_header()
        self.file.write("\n\n    %s.param('%s', type='%s', default=%s" % (
            self._conf_variable, name, type, repr(default_value)))
        if description:
            self.file.write(", description=\"%s\"" % (
                description.replace('"', '\'')))
        self.file.write(")")

    def comment(self, text):
        self.file.write("\n\n    # %s" % text)


class YamlSchemaWriter(object):
    def __init__(self, file, project, version):
        super(YamlSchemaWriter, self).__init__()
        self.file = file
        self.project = project
        self.version = version
        self._output_header()

    def _output_header(self):
        self.file.write("project: %s\n" % self.project)
        self.file.write("version: %s\n" % self.version)
        self.file.write("parameters:\n")

    def section(self, name):
        self._current_section = name

    def param(self, name, type, default_value=None, description=None):
        fullname = name
        if self._current_section and self._current_section != 'DEFAULT':
            fullname = '%s.%s' % (self._current_section, name)

        self.file.write("  - name: %s\n" % fullname)
        self.file.write("    type: %s\n" % type)
        self.file.write("    default: %s\n" % repr(default_value))
        if description:
            self.file.write("    help: %s\n" % repr(description))

        self.file.write("\n")

    def comment(self, text):
        self.file.write("\n# %s\n" % text)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('project',
                        help='Name of the project (e.g. "nova")')
    parser.add_argument('version',
                        help='Version of the project (e.g. "2013.1.3")')
    parser.add_argument('config_or_module',
                        help='Config file sample or Python module to process')
    args = parser.parse_args(argv[1:])
    return args


def sanitize_type_and_value(param_name, param_type, param_value):
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

    return (param_type, param_value)


def generate_schema_from_sample_config(project, version, config_file, writer):
    with open(config_file, 'r') as f:
        config_lines = f.readlines()

    description_lines = []
    for line in config_lines:
        if line.startswith('['):
            section_name = line.strip('[]\n')
            writer.section(section_name)
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

        (param_type, param_value) = \
            sanitize_type_and_value(param_name, param_type, param_value)

        writer.param(param_name, param_type, param_value, description)


OPT_TYPE_MAPPING = {
    'StrOpt': 'string',
    'BoolOpt': 'boolean',
    'IntOpt': 'integer',
    'FloatOpt': 'float',
    'ListOpt': 'list',
    'MultiStrOpt': 'multi'
}


OPTION_REGEX = re.compile(r"(%s)" % "|".join(OPT_TYPE_MAPPING.keys()))


def generate_schema_from_code(project, version, module_path, writer):
    old_sys_path = copy(sys.path)

    mods_by_pkg = dict()
    filepaths = []
    module_directory = ''

    if os.path.isdir(module_path):
        module_directory = module_path
        while module_directory != '':
            # TODO: handle .pyc and .pyo
            if not os.path.isfile(
                    os.path.join(module_directory, '__init__.py')):
                break

            module_directory = os.path.dirname(module_directory)

        if not module_directory in sys.path:
            sys.path.insert(0, module_directory)

        for (dirpath, _, filenames) in os.walk(module_path):
            for filename in filenames:
                if not filename.endswith('.py'):
                    continue

                filepath = os.path.join(dirpath, filename)
                with open(filepath) as f:
                    content = f.read()
                    if not re.search('Opt\(', content):
                        continue

                filepaths.append(filepath)
    else:
        filepaths.append(module_path)

    for filepath in filepaths:
        pkg_name = filepath.split(os.sep)[1]
        mod_path = filepath
        if module_directory != '':
            mod_path = filepath.replace(module_directory + '/', '', 1)
        mod_str = '.'.join(['.'.join(mod_path.split(os.sep)[:-1]),
                           os.path.basename(mod_path).split('.')[0]])

        mods_by_pkg.setdefault(pkg_name, list()).append(mod_str)

    pkg_names = filter(lambda x: x.endswith('.py'), mods_by_pkg.keys())
    pkg_names.sort()
    ext_names = filter(lambda x: x not in pkg_names, mods_by_pkg.keys())
    ext_names.sort()
    pkg_names.extend(ext_names)

    # opts_by_group is a mapping of group name to an options list
    # The options list is a list of (module, options) tuples
    opts_by_group = {'DEFAULT': []}

    for pkg_name in pkg_names:
        mods = mods_by_pkg.get(pkg_name)
        mods.sort()
        for mod_str in mods:
            if mod_str.endswith('.__init__'):
                mod_str = mod_str[:mod_str.rfind(".")]

            mod_obj = _import_module(mod_str)
            if not mod_obj:
                sys.stderr.write("Unable to import module %s" % mod_str)

            for group, opts in _list_opts(mod_obj):
                opts_by_group.setdefault(group, []).append((mod_str, opts))

    print_group_opts(writer, 'DEFAULT', opts_by_group.pop('DEFAULT', []))
    for group, opts in opts_by_group.items():
        print_group_opts(writer, group, opts)

    sys.path = old_sys_path


def _import_module(mod_str):
    try:
        if mod_str.startswith('bin.'):
            imp.load_source(mod_str[4:], os.path.join('bin', mod_str[4:]))
            return sys.modules[mod_str[4:]]
        else:
            __import__(mod_str)
            return sys.modules[mod_str]
    except ImportError:
        traceback.print_exc()
        # sys.stderr.write("%s\n" % str(ie))
        return None
    except Exception:
        traceback.print_exc()
        return None


def _is_in_group(opt, group):
    "Check if opt is in group."
    for key, value in group._opts.items():
        if value['opt'] == opt:
            return True
    return False


def _guess_groups(opt, mod_obj):
    # is it in the DEFAULT group?
    if _is_in_group(opt, cfg.CONF):
        return 'DEFAULT'

    # what other groups is it in?
    for key, value in cfg.CONF.items():
        if not isinstance(value, cfg.CONF.GroupAttr):
            continue

        if _is_in_group(opt, value._group):
            return value._group.name

    # raise RuntimeError(
    #     "Unable to find group for option %s, "
    #     "maybe it's defined twice in the same group?"
    #     % opt.name
    # )

    return 'DEFAULT'


def _list_opts(obj):
    def is_opt(o):
        return (isinstance(o, cfg.Opt) and
                not isinstance(o, cfg.SubCommandOpt))

    opts = list()
    for attr_str in dir(obj):
        attr_obj = getattr(obj, attr_str)
        if is_opt(attr_obj):
            opts.append(attr_obj)
        elif (isinstance(attr_obj, list) and
              all(map(lambda x: is_opt(x), attr_obj))):
            opts.extend(attr_obj)

    ret = {}
    for opt in opts:
        ret.setdefault(_guess_groups(opt, obj), []).append(opt)
    return ret.items()


def print_group_opts(writer, group, opts_by_module):
    writer.section(group)
    for mod, opts in opts_by_module:
        writer.comment("Options defined in %s" % mod)
        for opt in opts:
            print_opt(writer, opt)


def print_opt(writer, opt):
    opt_name, opt_default, opt_help = opt.dest, opt.default, opt.help

    if not opt_help:
        sys.stderr.write('WARNING: "%s" is missing help string.\n' % opt_name)
        opt_help = ""

    opt_type = None
    try:
        opt_type = OPT_TYPE_MAPPING.get(
            OPTION_REGEX.search(str(type(opt))).group(0))
    except (ValueError, AttributeError) as err:
        sys.stderr.write("%s\n" % str(err))
        opt_type = 'string'

    writer.param(opt_name, opt_type, opt_default, opt_help)


def main(argv):
    args = parse_args(argv)
    params = vars(args)

    project = params.pop('project')
    version = params.pop('version')
    path = params.pop('config_or_module')

    writer = YamlSchemaWriter(sys.stdout, project, version)

    if os.path.isdir(path) or path.endswith('.py'):
        generate_schema_from_code(project, version, path,
                                  writer=writer)
    else:
        generate_schema_from_sample_config(project, version, path,
                                           writer=writer)


if __name__ == '__main__':
    main(sys.argv)
