# encryption/aes.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import os

class AES:
    def __init__(self, key=None):
        self.key = key if key else os.urandom(16)  # 128-bit key

    def encrypt(self, data):
        """Encrypt variable-length plaintext using AES with CBC mode."""
        iv = os.urandom(16)  # Generate a 16-byte IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        return iv + encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, encrypted_data):
        """Decrypt variable-length ciphertext."""
        iv = encrypted_data[:16]  # Extract the first 16 bytes as IV
        ciphertext = encrypted_data[16:]  # Remaining bytes are the ciphertext
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        unpadder = PKCS7(128).unpadder()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        return unpadder.update(padded_data) + unpadder.finalize()  # Unpad the plaintext

    def get_key_bytes(self):
        return self.key
