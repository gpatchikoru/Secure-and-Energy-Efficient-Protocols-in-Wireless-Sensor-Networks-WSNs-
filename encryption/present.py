# encryption/present.py
import os

class PresentCipher:
    def __init__(self, key=None):
        self.key = key if key else os.urandom(10)  # 80-bit key
        self.key_int = int.from_bytes(self.key, byteorder="big")

    def encrypt(self, plaintext):
        """Encrypt variable-length plaintext by padding and chunking."""
        block_size = 8
        plaintext = self.pad_data(plaintext, block_size)  # Apply padding
        encrypted_chunks = []
        for i in range(0, len(plaintext), block_size):
            chunk = plaintext[i:i + block_size]
            chunk_int = int.from_bytes(chunk, byteorder="big")
            encrypted_int = (chunk_int ^ self.key_int) & 0xFFFFFFFFFFFFFFFF
            encrypted_chunks.append(encrypted_int.to_bytes(block_size, byteorder="big"))
        return b"".join(encrypted_chunks)

    def decrypt(self, ciphertext):
        """Decrypt variable-length ciphertext by chunking and unpadding."""
        block_size = 8
        decrypted_chunks = []
        for i in range(0, len(ciphertext), block_size):
            chunk = ciphertext[i:i + block_size]
            chunk_int = int.from_bytes(chunk, byteorder="big")
            decrypted_int = (chunk_int ^ self.key_int) & 0xFFFFFFFFFFFFFFFF
            decrypted_chunks.append(decrypted_int.to_bytes(block_size, byteorder="big"))
        decrypted_data = b"".join(decrypted_chunks)
        return self.unpad_data(decrypted_data)

    def pad_data(self, data, block_size):
        """Pad data to make its length a multiple of the block size."""
        padding_length = block_size - (len(data) % block_size)
        return data + bytes([padding_length] * padding_length)

    def unpad_data(self, padded_data):
        """Remove padding from the data."""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]

    def get_key_bytes(self):
        return self.key
