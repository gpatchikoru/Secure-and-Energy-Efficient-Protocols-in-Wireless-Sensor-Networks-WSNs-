# encryption/chacha20_cipher.py
from Crypto.Cipher import ChaCha20
import os

class ChaCha20Cipher:
    def __init__(self):
        self.key = os.urandom(32)  # 256-bit key
        self.nonce = os.urandom(12)  # 96-bit nonce

    def encrypt(self, data):
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        return cipher.encrypt(data)

    def decrypt(self, data):
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        return cipher.decrypt(data)

    def get_key_bytes(self):
        return self.key
