# encryption/key_management.py
import os

class KeyManagement:
    def __init__(self):
        self.keys = {}

    def generate_key(self, node_id):
        """
        Generate and assign a unique key for a given node.
        
        :param node_id: Unique identifier for the node
        """
        self.keys[node_id] = os.urandom(16)  # Generate a random 128-bit key

    def get_key(self, node_id):
        """
        Retrieve the key for a given node.
        
        :param node_id: Unique identifier for the node
        :return: The key in bytes or None if not found
        """
        return self.keys.get(node_id, None)

    def distribute_keys(self, node_ids):
        """
        Generate and distribute keys to multiple nodes.
        
        :param node_ids: List of node identifiers
        """
        for node_id in node_ids:
            self.generate_key(node_id)
