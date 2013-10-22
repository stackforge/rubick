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
