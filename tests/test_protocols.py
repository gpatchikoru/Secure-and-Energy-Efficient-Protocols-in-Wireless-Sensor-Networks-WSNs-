# tests/test_protocols.py
import sys
import os
import unittest

# Add the root directory to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from encryption.aes import AES
from encryption.speck import SpeckCipher
from encryption.present import PresentCipher
from encryption.selective_encryption import SelectiveEncryption
from protocols.openwsn import OpenWSN
from protocols.dash7 import DASH7
from protocols.energy_model import EnergyModel

class TestProtocols(unittest.TestCase):
    def setUp(self):
        self.energy_model = EnergyModel()
        self.aes = AES()
        self.speck = SpeckCipher()
        self.present = PresentCipher()
        self.selective_aes = SelectiveEncryption(self.aes, encryption_ratio=0.5)

        self.openwsn_aes = OpenWSN(self.aes, self.energy_model)
        self.openwsn_speck = OpenWSN(self.speck, self.energy_model)
        self.openwsn_present = OpenWSN(self.present, self.energy_model)
        self.dash7_aes = DASH7(self.aes, self.energy_model)
        self.dash7_speck = DASH7(self.speck, self.energy_model)
        self.dash7_present = DASH7(self.present, self.energy_model)
        self.openwsn_selective_aes = OpenWSN(self.selective_aes, self.energy_model)

        self.plaintext = b"Test message for protocol functionality!"

    def test_openwsn_aes(self):
        packet = self.openwsn_aes.prepare_packet(self.plaintext, headers={"Type": "Data"})
        decrypted = self.openwsn_aes.process_packet(packet)
        self.assertEqual(decrypted, self.plaintext, "OpenWSN AES decryption failed!")

    def test_openwsn_speck(self):
        packet = self.openwsn_speck.prepare_packet(self.plaintext, headers={"Type": "Data"})
        decrypted = self.openwsn_speck.process_packet(packet)
        self.assertEqual(decrypted, self.plaintext, "OpenWSN SPECK decryption failed!")

    def test_openwsn_present(self):
        packet = self.openwsn_present.prepare_packet(self.plaintext, headers={"Type": "Data"})
        decrypted = self.openwsn_present.process_packet(packet)
        self.assertEqual(decrypted, self.plaintext, "OpenWSN PRESENT decryption failed!")

    def test_dash7_aes(self):
        response = self.dash7_aes.query_response("Query1", self.plaintext)
        decrypted = self.dash7_aes.process_response(response)
        self.assertEqual(decrypted, self.plaintext, "DASH7 AES decryption failed!")

    def test_dash7_speck(self):
        response = self.dash7_speck.query_response("Query1", self.plaintext)
        decrypted = self.dash7_speck.process_response(response)
        self.assertEqual(decrypted, self.plaintext, "DASH7 SPECK decryption failed!")

    def test_dash7_present(self):
        response = self.dash7_present.query_response("Query1", self.plaintext)
        decrypted = self.dash7_present.process_response(response)
        self.assertEqual(decrypted, self.plaintext, "DASH7 PRESENT decryption failed!")

    def test_openwsn_selective_aes(self):
        packet = self.openwsn_selective_aes.prepare_packet(self.plaintext, headers={"Type": "Data"})
        decrypted = self.openwsn_selective_aes.process_packet(packet)
        self.assertEqual(decrypted, self.plaintext, "OpenWSN Selective AES decryption failed!")

    def test_all_protocols(self):
        protocols = [
            self.openwsn_aes,
            self.openwsn_speck,
            self.openwsn_present,
            self.dash7_aes,
            self.dash7_speck,
            self.dash7_present,
            self.openwsn_selective_aes
        ]

        for protocol in protocols:
            if isinstance(protocol, OpenWSN):
                packet = protocol.prepare_packet(self.plaintext, headers={"Type": "Data"})
                decrypted = protocol.process_packet(packet)
            elif isinstance(protocol, DASH7):
                response = protocol.query_response("Query1", self.plaintext)
                decrypted = protocol.process_response(response)
            self.assertEqual(decrypted, self.plaintext, f"{protocol} decryption failed!")

if __name__ == "__main__":
    unittest.main()
