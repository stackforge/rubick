from nodes import NodesDict
import unittest


class NodesTest(unittest.TestCase):

    def setUp(self):
        self.nodes = NodesDict()

    def test_uniq(self):
        compute1 = dict()
        compute1['hwaddr'] = 'compute1_hwaddr'

        compute2 = dict()
        compute2['hwaddr'] = 'compute2_hwaddr'

        compute3 = dict()
        compute3['hwaddr'] = 'compute2_hwaddr'  # duplicate hwaddr

        self.nodes.add(compute1)
        self.nodes.add(compute2)
        self.nodes.add(compute3)

        self.assertEqual(2, self.nodes.__len__())

    def test_add(self):
        compute1 = dict()
        compute1['hwa3ddr'] = 'compute1_hwaddr'
        self.assertRaises(KeyError, self.nodes.add, compute1)
