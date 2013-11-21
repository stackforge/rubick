import argparse
from copy import copy
from lib2to3.pgen2 import driver
from lib2to3.pgen2 import token
from lib2to3.pygram import python_grammar, python_symbols as py
from lib2to3.pytree import Node, Leaf
import os
import re
import sys
import traceback

from oslo.config import cfg

from rubick.schemas.yaml_utils import yaml_string, yaml_value


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

        self.file.write("  - name: %s\n"
                        % yaml_string(fullname, allowSimple=True))
        self.file.write("    type: %s\n" % yaml_string(type, allowSimple=True))
        self.file.write("    default: %s\n" % yaml_value(default_value))
        if description:
            self.file.write("    help: %s\n" % yaml_string(description))

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


def convert(gr, raw_node):
    type, value, context, children = raw_node
    # if has children or correspond to nonterminal
    if children or type in gr.number2symbol:
        return Node(type, children, context=context)
    else:
        return Leaf(type, value, context=context)


def walk_tree(root):
    while True:
        yield root

        # Optimize traversing single-child nodes
        if len(root.children) == 1:
            root = root.children[0]
            continue

        break

    for child in copy(root.children):
        for node in walk_tree(child):
            yield node


def extract_config_from_file(path):
    with open(path) as f:
        contents = f.read()

    d = driver.Driver(python_grammar, convert=convert)
    tree = d.parse_string(contents)

    def mark_stmt(node):
        n = node
        while n:
            if n.type == py.stmt:
                n.marked = True
                break
            n = n.parent

    fullnames = {}
    # Process imports and renames
    for node in walk_tree(tree):
        if node.type == py.import_from:
            mod = str(node.children[1]).strip()
            for node2 in walk_tree(node.children[3]):
                if node2.type == py.import_as_name:
                    n = str(node2).strip()
                    f = '.'.join([mod, n])
                    fullnames[n] = f
        elif node.type == py.expr_stmt:
            if len(node.children) > 1 and node.children[1].type == token.EQUAL:
                lhs = str(node.children[0]).strip()
                rhs = str(node.children[2]).strip()
                if re.match('\S+(\.\S+)*', rhs):
                    parts = rhs.split('.')
                    if parts[0] in fullnames:
                        rhs = '.'.join([fullnames[parts[0]]] + parts[1:])
                        fullnames[lhs] = rhs

                        if any([rhs.startswith(s) for s in ['oslo.', 'oslo.config.', 'oslo.config.cfg.']]):
                            mark_stmt(node)

    # Process all callsites CONF.register*
    for node in walk_tree(tree):
        if node.type == py.power and node.children[0].children[0].type == token.NAME:
            s = str(node.children[0]).strip()
            if s in fullnames:
                s = fullnames[s]

            cs = node.children
            i = 1
            while i < len(cs) and cs[i].type == py.trailer:
                c = cs[i]
                if c.children[0].type != token.DOT:
                    break

                s += '.' + c.children[1].value
                i += 1

            if i < len(cs) and cs[i].type == py.trailer and cs[i].children[0].type == token.LPAR:
                # call site
                if s.startswith('oslo.config.cfg.CONF.'):
                    rest = s[len('oslo.config.cfg.CONF.'):]
                    if rest.startswith('register_'):
                        mark_stmt(node)

                if s.startswith('oslo.config.cfg.'):
                    rest = s[len('oslo.config.cfg.'):]
                    if rest.endswith('Opt'):
                        mark_stmt(node)

    # Traverse code and find all var references
    seen_vars = set()
    referenced_vars_queue = []

    def find_definition(tree, name):
        for node in walk_tree(tree):
            if node.type == py.classdef and node.children[1].value == name:
                return node
            elif node.type == py.funcdef and node.children[1].value == name:
                return node
            elif node.type == py.import_name:
                imported_name = str(node.children[1]).strip()
                if imported_name == name:
                    return node
            elif node.type == py.import_from:
                for n in walk_tree(node):
                    if n.type == py.import_as_name:
                        i = 0
                        if len(n.children) == 3:
                            i = 2

                        if n.children[i].value == name:
                            return node
            elif node.type == py.expr_stmt:
                if len(node.children) > 1 and node.children[1].type == token.EQUAL:
                    for n in walk_tree(node):
                        if n.type == py.power:
                            assignment_name = str(n.children[0]).strip()
                            if assignment_name == name:
                                return node

        return None

    def collect_refs(root):
        for n2 in walk_tree(root):
            if n2.type == py.power and n2.children[0].children[0].type == token.NAME:
                name = n2.children[0].children[0].value
                x = 1
                while (x < len(n2.children) and
                       n2.children[x].type == py.trailer and
                       n2.children[x].children[0].type == token.DOT):
                    name += str(n2.children[x]).strip()
                    x += 1

                if '.' not in name:
                    isKWArgName = False
                    n = n2
                    while n.parent:
                        if n.parent.type == py.argument:
                            arg = n.parent
                            if len(arg.children) > 1 and arg.children[1].type == token.EQUAL and n == arg.children[0]:
                                isKWArgName = True
                        n = n.parent

                    if isKWArgName:
                        continue

                    if name in dir(__builtins__):
                        continue

                if name not in seen_vars:
                    seen_vars.add(name)
                    referenced_vars_queue.append(name)

    for node in tree.children:
        if node.type == py.stmt and (hasattr(node, 'marked') and node.marked):
            collect_refs(node)

    for name in referenced_vars_queue:
        node = find_definition(tree, name)
        if node:
            mark_stmt(node)
            collect_refs(node)
        else:
            while '.' in name:
                name = '.'.join(name.split('.')[:-1])
                node = find_definition(tree, name)
                if node:
                    mark_stmt(node)
                    collect_refs(node)

    # Remove all unmarked top-level statements
    for node in walk_tree(tree):
        if node.type == py.stmt and node.parent.type == py.file_input:
            if not (hasattr(node, 'marked') and node.marked):
                node.remove()

    code = str(tree)

    try:
        exec code in {'__file__': path}
    except Exception:
        sys.stderr.write("Error processing file %s\n" % path)
        traceback.print_exc()
        sys.stderr.write(code)


def generate_schema_from_code(project, version, module_path, writer):
    old_sys_path = copy(sys.path)

    filepaths = []
    module_directory = ''

    if os.path.isdir(module_path):
        module_directory = module_path
        while module_directory != '':
            # TODO(mkulkin): handle .pyc and .pyo
            if not os.path.isfile(
                    os.path.join(module_directory, '__init__.py')):
                break

            module_directory = os.path.dirname(module_directory)

        if module_directory not in sys.path:
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
        extract_config_from_file(filepath)

    print_group_opts(writer, 'DEFAULT', cfg.CONF._opts.values())
    for group_name in cfg.CONF._groups:
        print_group_opts(writer, group_name, cfg.CONF._groups[group_name]._opts.values())

    sys.path = old_sys_path


def print_group_opts(writer, group, opts):
    writer.section(group)
    for opt in opts:
        print_opt(writer, opt['opt'])


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
