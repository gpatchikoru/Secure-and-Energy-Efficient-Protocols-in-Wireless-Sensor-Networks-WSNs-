# tests/test_encryption.py
import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from encryption.aes import AES
from encryption.speck import SpeckCipher
from encryption.present import PresentCipher
from encryption.selective_encryption import SelectiveEncryption

def test_encryption():
    aes = AES()
    speck = SpeckCipher()
    present = PresentCipher()
    selective_aes = SelectiveEncryption(aes, encryption_ratio=0.5)

    plaintexts = [
        b"Short",  # Less than block size
        b"ExactlyEight",  # Exactly 12 bytes
        b"Longer than one block, let's see how it handles this!"  # Multiple blocks
    ]

    for plaintext in plaintexts:
        print(f"\nOriginal: {plaintext}")

        encrypted_aes = aes.encrypt(plaintext)
        print(f"AES Encrypted: {encrypted_aes}")
        decrypted_aes = aes.decrypt(encrypted_aes)
        print(f"AES Decrypted: {decrypted_aes}")
        assert decrypted_aes == plaintext, "AES decryption failed!"

        encrypted_speck = speck.encrypt(plaintext)
        print(f"SPECK Encrypted: {encrypted_speck}")
        decrypted_speck = speck.decrypt(encrypted_speck)
        print(f"SPECK Decrypted: {decrypted_speck}")
        assert decrypted_speck == plaintext, "SPECK decryption failed!"

        encrypted_present = present.encrypt(plaintext)
        print(f"PRESENT Encrypted: {encrypted_present}")
        decrypted_present = present.decrypt(encrypted_present)
        print(f"PRESENT Decrypted: {decrypted_present}")
        assert decrypted_present == plaintext, "PRESENT decryption failed!"

        encrypted_selective = selective_aes.encrypt(plaintext)
        print(f"Selective AES Encrypted: {encrypted_selective}")
        decrypted_selective = selective_aes.decrypt(encrypted_selective)
        print(f"Selective AES Decrypted: {decrypted_selective}")
        assert decrypted_selective == plaintext, "Selective AES decryption failed!"

    print("\nAll encryption tests passed!")

if __name__ == "__main__":
    test_encryption()
