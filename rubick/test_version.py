from rubick.common import Version

import unittest


class VersionTests(unittest.TestCase):

    def test_creation_from_components(self):
        v = Version(1, 3, 7)
        self.assertEqual(1, v.major)
        self.assertEqual(3, v.minor)
        self.assertEqual(7, v.maintenance)

    def test_creation_from_string(self):
        v = Version('1.2.12')
        self.assertEqual(1, v.major)
        self.assertEqual(2, v.minor)
        self.assertEqual(12, v.maintenance)

    def test_creation_from_string_with_less_parts(self):
        v = Version('1.2')
        self.assertEqual(1, v.major)
        self.assertEqual(2, v.minor)
        self.assertEqual(0, v.maintenance)

        v = Version('12')
        self.assertEqual(12, v.major)
        self.assertEqual(0, v.minor)
        self.assertEqual(0, v.maintenance)

    def test_creation_from_other_version(self):
        v = Version('1.2.3')
        v2 = Version(v)
        self.assertEqual(1, v2.major)
        self.assertEqual(2, v2.minor)
        self.assertEqual(3, v2.maintenance)

    def test_equility(self):
        v1 = Version('1.2.3')
        v2 = Version(1, 2, 3)
        v3 = Version(1, 2, 4)

        self.assertTrue(v1 == v2)
        self.assertFalse(v1 == v3)

    def test_non_equility(self):
        v1 = Version('1.2.3')
        v2 = Version(1, 2, 3)
        v3 = Version(1, 2, 4)

        self.assertFalse(v1 != v2)
        self.assertTrue(v1 != v3)

    def test_comparision(self):
        v1 = Version('1.2.3')
        v2 = Version(1, 1, 5)

        self.assertTrue(v1 > v2)
        self.assertFalse(v1 < v2)


if __name__ == '__main__':
    unittest.main()
