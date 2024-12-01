# encryption/hmac_util.py
import hmac
import hashlib

class HMACUtil:
    def __init__(self, key):
        if not isinstance(key, bytes):
            raise ValueError("Key must be in bytes format")
        self.key = key[:16]  # Use the first 16 bytes for HMAC

    def generate_hmac(self, data):
        return hmac.new(self.key, data, hashlib.sha256).hexdigest()

    def verify_hmac(self, data, received_hmac):
        expected_hmac = self.generate_hmac(data)
        return hmac.compare_digest(expected_hmac, received_hmac)
