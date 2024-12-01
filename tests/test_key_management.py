# tests/test_key_management.py
import sys
import os
import unittest

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from encryption.key_management import KeyManagement

class TestKeyManagement(unittest.TestCase):
    def setUp(self):
        self.km = KeyManagement()
        self.node_ids = ["Node_1", "Node_2", "Node_3"]

    def test_generate_and_get_key(self):
        for node_id in self.node_ids:
            self.km.generate_key(node_id)
            key = self.km.get_key(node_id)
            self.assertIsNotNone(key)
            self.assertEqual(len(key), 16)  # 128-bit key

    def test_distribute_keys(self):
        self.km.distribute_keys(self.node_ids)
        for node_id in self.node_ids:
            key = self.km.get_key(node_id)
            self.assertIsNotNone(key)
            self.assertEqual(len(key), 16)

    def test_get_key_nonexistent_node(self):
        key = self.km.get_key("Node_X")
        self.assertIsNone(key)

if __name__ == "__main__":
    unittest.main()
