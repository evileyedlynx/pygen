import unittest
from Node import Node


class TestNode(unittest.TestCase):
    def setUp(self) -> None:
        self.node = Node('node_name', 'str:14957')

    def test_generate_data(self):
        self.assertEqual(self.node.generate_data(), '14957')

    def test_generate_data_with_int(self):
        self.node.node_type = 'int'
        self.assertEqual(self.node.generate_data(), 14957)

    def test_generate_data_rand(self):
        self.node.data_generate_rule = '["item"]'
        self.assertIn(self.node.generate_data(), ["item", "data", "store"])

if __name__ == "__main__":
  unittest.main()
