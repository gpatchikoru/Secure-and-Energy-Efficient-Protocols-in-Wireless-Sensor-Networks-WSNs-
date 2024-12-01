# protocols/openwsn.py
from encryption.hmac_util import HMACUtil

class OpenWSN:
    def __init__(self, encryption, energy_model):
        """
        Initialize OpenWSN protocol with encryption and energy model.
        
        :param encryption: Encryption instance (e.g., AES, SPECK)
        :param energy_model: EnergyModel instance
        """
        self.encryption = encryption
        self.hmac_util = HMACUtil(self.encryption.get_key_bytes())
        self.energy_model = energy_model

    def prepare_packet(self, payload, headers):
        """
        Prepare a packet by encrypting the payload and generating an HMAC.
        
        :param payload: The data to encrypt
        :param headers: Dictionary of headers
        :return: Dictionary representing the packet
        """
        encrypted_payload = self.encryption.encrypt(payload)  # Encrypt the entire payload
        hmac_value = self.hmac_util.generate_hmac(encrypted_payload)  # Generate HMAC
        return {
            'headers': headers,
            'payload': encrypted_payload,
            'hmac': hmac_value,
        }

    def process_packet(self, packet):
        """
        Process an incoming packet by verifying the HMAC and decrypting the payload.
        
        :param packet: Dictionary representing the packet
        :return: Decrypted payload
        """
        encrypted_payload = packet['payload']
        if not self.hmac_util.verify_hmac(encrypted_payload, packet['hmac']):
            raise ValueError("HMAC verification failed")

        # Decrypt the payload
        decrypted_payload = self.encryption.decrypt(encrypted_payload)
        return decrypted_payload
