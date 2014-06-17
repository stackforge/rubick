# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.


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
