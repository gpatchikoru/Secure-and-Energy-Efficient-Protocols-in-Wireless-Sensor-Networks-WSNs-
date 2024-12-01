# protocols/dash7.py
from encryption.hmac_util import HMACUtil

class DASH7:
    def __init__(self, encryption, energy_model):
        """
        Initialize DASH7 protocol with encryption and energy model.
        
        :param encryption: Encryption instance (e.g., AES, SPECK)
        :param energy_model: EnergyModel instance
        """
        self.encryption = encryption
        self.hmac_util = HMACUtil(self.encryption.get_key_bytes())
        self.energy_model = energy_model

    def query_response(self, query, response):
        """
        Prepare a query-response packet.
        
        :param query: The query string
        :param response: The response data
        :return: Dictionary representing the response packet
        """
        # Encrypt the response
        encrypted_response = self.encryption.encrypt(response)
        # Generate HMAC for the encrypted response
        hmac_value = self.hmac_util.generate_hmac(encrypted_response)
        return {
            'query': query,
            'response': encrypted_response,
            'hmac': hmac_value,
        }

    def process_response(self, response_packet):
        """
        Process an incoming query-response packet.
        
        :param response_packet: Dictionary representing the response packet
        :return: Decrypted response
        """
        encrypted_response = response_packet['response']
        if not self.hmac_util.verify_hmac(encrypted_response, response_packet['hmac']):
            raise ValueError("HMAC verification failed")

        # Decrypt the response
        decrypted_response = self.encryption.decrypt(encrypted_response)
        return decrypted_response
