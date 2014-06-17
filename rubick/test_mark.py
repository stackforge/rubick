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
from rubick.common import Mark

import unittest


class MarkTests(unittest.TestCase):

    def test_creation(self):
        m = Mark('nova.conf', 3, 5)
        self.assertEqual('nova.conf', m.source)
        self.assertEqual(3, m.line)
        self.assertEqual(5, m.column)

    def test_merge(self):
        m1 = Mark('nova.conf', 3, 5)
        m2 = Mark('unknown', 2, 7)

        m = m1.merge(m2)

        self.assertEqual(m1.source, m.source)
        self.assertEqual(m1.line + m2.line, m.line)
        self.assertEqual(m1.column + m2.column, m.column)
