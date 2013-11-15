def yaml_string(s, allowSimple=False):
    if "'" in s:
        return '"%s"' % s.replace('\\', '\\\\').replace('"', '\\"')
    else:
        if not allowSimple or any([c in s for c in " :,"]):
            return "'%s'" % s
        else:
            return s


def yaml_value(x):
    if x is None:
        return '~'
    elif x is True:
        return 'true'
    elif x is False:
        return 'false'
    elif isinstance(x, str):
        return yaml_string(x)
    else:
        return repr(x)
