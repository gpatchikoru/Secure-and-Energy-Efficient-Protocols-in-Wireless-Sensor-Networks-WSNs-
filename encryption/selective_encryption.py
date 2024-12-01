from cryptography.hazmat.primitives.padding import PKCS7


class SelectiveEncryption:
    def __init__(self, base_encryption, encryption_ratio=0.5):
        """
        Initialize with a base encryption algorithm and the ratio of data to encrypt.

        :param base_encryption: An instance of an encryption class (e.g., AES)
        :param encryption_ratio: Float between 0 and 1 indicating the portion to encrypt
        """
        self.base_encryption = base_encryption
        self.encryption_ratio = encryption_ratio
        self.block_size = 128  # Block size in bits (16 bytes for AES)

    def _apply_padding(self, data):
        """Apply PKCS7 padding to the data."""
        padder = PKCS7(self.block_size).padder()
        return padder.update(data) + padder.finalize()

    def _remove_padding(self, data):
        """Remove PKCS7 padding from the data."""
        unpadder = PKCS7(self.block_size).unpadder()
        return unpadder.update(data) + unpadder.finalize()

    def encrypt(self, data):
        """Encrypt only a portion of the data based on encryption_ratio."""
        # Split data into critical and non-critical portions
        split_index = int(len(data) * self.encryption_ratio)
        critical_data = data[:split_index]
        non_critical_data = data[split_index:]

        # Pad the critical portion
        padded_critical_data = self._apply_padding(critical_data)

        # Encrypt the padded critical portion
        encrypted_critical = self.base_encryption.encrypt(padded_critical_data)

        # Combine encrypted critical data and non-critical data using delimiter
        delimiter = b"||"
        return encrypted_critical + delimiter + non_critical_data

    def decrypt(self, encrypted_data):
        """Decrypt only the encrypted portion of the data."""
        # Split encrypted critical data and non-critical data using the delimiter
        delimiter = b"||"
        if delimiter not in encrypted_data:
            raise ValueError("Data does not contain expected delimiter '||'.")
        
        encrypted_critical, non_critical_data = encrypted_data.split(delimiter, maxsplit=1)

        # Decrypt the critical portion
        decrypted_critical = self.base_encryption.decrypt(encrypted_critical)

        # Remove padding from the critical portion
        try:
            unpadded_critical_data = self._remove_padding(decrypted_critical)
        except ValueError as e:
            raise ValueError("Invalid padding during decryption") from e

        # Combine decrypted critical data and non-critical data
        return unpadded_critical_data + non_critical_data

    def get_key_bytes(self):
        """Delegate to the base encryption's `get_key_bytes` method."""
        return self.base_encryption.get_key_bytes()
