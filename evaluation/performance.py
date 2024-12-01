# evaluation/performance.py
import time

class PerformanceEvaluator:
    def measure_encryption_time(self, encryption, payload):
        """
        Measure the time taken to encrypt the payload.
        
        :param encryption: Encryption instance
        :param payload: Data to encrypt
        :return: Elapsed time in seconds
        """
        try:
            start_time = time.perf_counter()  # Start high-precision timer
            encryption.encrypt(payload)  # Perform encryption
            end_time = time.perf_counter()  # End high-precision timer
            elapsed_time = end_time - start_time
            print(f"Encryption time: {elapsed_time:.10f} seconds")
            return elapsed_time
        except Exception as e:
            print(f"Error during encryption: {e}")
            return 0.0

    def measure_decryption_time(self, encryption, encrypted_payload):
        """
        Measure the time taken to decrypt the payload.
        
        :param encryption: Encryption instance
        :param encrypted_payload: Data to decrypt
        :return: Elapsed time in seconds
        """
        try:
            start_time = time.perf_counter()  # Start high-precision timer
            encryption.decrypt(encrypted_payload)  # Perform decryption
            end_time = time.perf_counter()  # End high-precision timer
            elapsed_time = end_time - start_time
            print(f"Decryption time: {elapsed_time:.10f} seconds")
            return elapsed_time
        except Exception as e:
            print(f"Error during decryption: {e}")
            return 0.0
