from joker import Joker
import unittest


class JokerTest(unittest.TestCase):

    def setUp(self):
        self.joker = Joker()

    def test_3nodes(self):
        self.assertEqual(3, len(self.joker.discovery()))
        return 1
