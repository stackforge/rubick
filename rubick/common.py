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
import copy
import os.path

from recordtype import recordtype


def find(l, predicate):
    results = [x for x in l if predicate(x)]
    return results[0] if len(results) > 0 else None


def index(l, predicate):
    i = 0
    while i < len(l):
        if predicate(l[i]):
            return i
        i += 1
    return -1


def all_subclasses(klass):
    subclasses = klass.__subclasses__()
    for d in list(subclasses):
        subclasses.extend(all_subclasses(d))
    return subclasses


def path_relative_to(path, base_path):
    if not path.startswith('/'):
        path = os.path.join(base_path, path)

    return path


class Version:

    def __init__(self, major, minor=0, maintenance=0):
        "Create Version object by either passing 3 integers,"
        "one string or an another Version object"
        if isinstance(major, str):
            self.parts = [int(x) for x in major.split('.', 3)]
            while len(self.parts) < 3:
                self.parts.append(0)

        elif isinstance(major, Version):
            self.parts = major.parts
        else:
            self.parts = [int(major), int(minor), int(maintenance)]

    @property
    def major(self):
        return self.parts[0]

    @major.setter
    def major(self, value):
        self.parts[0] = int(value)

    @property
    def minor(self):
        return self.parts[1]

    @minor.setter
    def minor(self, value):
        self.parts[1] = int(value)

    @property
    def maintenance(self):
        return self.parts[2]

    @maintenance.setter
    def maintenance(self, value):
        self.parts[2] = value

    def __str__(self):
        return '.'.join([str(p) for p in self.parts])

    def __repr__(self):
        return '<Version %s>' % str(self)

    def __cmp__(self, other):
        for i in range(0, 3):
            x = self.parts[i] - other.parts[i]
            if x != 0:
                return -1 if x < 0 else 1
        return 0

    def __lt__(self, other):
        for i in range(0, 3):
            x = self.parts[i] - other.parts[i]
            if x != 0:
                return True if x < 0 else False
        return False

    def __le__(self, other):
        for i in range(0, 3):
            x = self.parts[i] - other.parts[i]
            if x != 0:
                return True if x < 0 else False
        return True

    def __ne__(self, other):
        for i in range(0, 3):
            x = self.parts[i] - other.parts[i]
            if x != 0:
                return True
        return False

    def __eq__(self, other):
        for i in range(0, 3):
            x = self.parts[i] - other.parts[i]
            if x != 0:
                return False
        return True


class Mark(object):

    def __init__(self, source, line=0, column=0):
        self.source = source
        self.line = line
        self.column = column

    def __eq__(self, other):
        return (
            (self.source == other.source) and
            (self.line == other.line) and
            (self.column == other.column)
        )

    def __ne__(self, other):
        return not self == other

    def merge(self, other):
        return (
            Mark(
                self.source,
                self.line +
                other.line,
                self.column +
                other.column)
        )

    def __repr__(self):
        return '%s line %d column %d' % (self.source, self.line, self.column)


class Error:

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return (
            '<%s "%s">' % (
                str(self.__class__).split('.')[-1][:-2],
                self.message)
        )

    def __str__(self):
        return self.message


class Issue(object):
    FATAL = 'FATAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'

    def __init__(self, type, message):
        self.type = type
        self.message = message

    def __eq__(self, other):
        if not isinstance(other, Issue):
            return False

        return self.type == other.type and self.message == other.message

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return (
            '<%s type=%s message=%s>' % (
                str(self.__class__).split('.')[-1][:-2],
                self.type,
                self.message)
        )

    def __str__(self):
        return '[%s] %s' % (self.type, self.message)


class MarkedIssue(Issue):

    def __init__(self, type, message, mark):
        super(MarkedIssue, self).__init__(type, message)
        self.mark = mark

    def offset_by(self, base_mark):
        other = copy.copy(self)
        other.mark = base_mark.merge(self.mark)
        return other

    def __eq__(self, other):
        if not isinstance(other, MarkedIssue):
            return False

        return super(MarkedIssue, self).__eq__(other) and self.mark == other.mark

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return (
            '<%s type=%s message=%s mark=%s>' % (
                str(self.__class__).split('.')[-1][:-2],
                self.type,
                self.message,
                self.mark)
        )

    def __str__(self):
        return (
            super(MarkedIssue, self).__str__() +
            (' (source "%s" line %d column %d)' %
                (self.mark.source, self.mark.line + 1, self.mark.column + 1))
        )


Rule = recordtype('Rule', ['name', 'description'])


class Inspection(object):

    @classmethod
    def all_inspections(klass):
        return [c for c in all_subclasses(klass)]

    @classmethod
    def rules(klass):
        if hasattr(klass, 'name') and hasattr(klass, 'description'):
            return [Rule(klass.name, klass.description)]
        else:
            return []

    def inspect(self, openstack):
        pass
