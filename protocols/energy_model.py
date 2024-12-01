# protocols/energy_model.py

class EnergyModel:
    def __init__(self, energy_per_bit=50e-9, energy_per_operation=5e-9):
        """
        Initialize energy consumption parameters.
        
        :param energy_per_bit: Energy consumed per bit transmitted (Joules)
        :param energy_per_operation: Energy consumed per cryptographic operation (Joules)
        """
        self.energy_per_bit = energy_per_bit  # Energy in joules
        self.energy_per_operation = energy_per_operation  # Energy per computation step

    def calculate_transmission_energy(self, data_size_bytes):
        """
        Calculate energy consumption for data transmission.
        
        :param data_size_bytes: Size of data in bytes
        :return: Energy consumed in Joules
        """
        bits = data_size_bytes * 8
        return bits * self.energy_per_bit

    def calculate_computation_energy(self, num_operations):
        """
        Calculate energy consumption for computations.
        
        :param num_operations: Number of cryptographic operations
        :return: Energy consumed in Joules
        """
        return num_operations * self.energy_per_operation

    def total_energy(self, data_size_bytes, num_operations):
        """
        Calculate total energy consumption.
        
        :param data_size_bytes: Size of data in bytes
        :param num_operations: Number of cryptographic operations
        :return: Total energy consumed in Joules
        """
        return self.calculate_transmission_energy(data_size_bytes) + self.calculate_computation_energy(num_operations)
