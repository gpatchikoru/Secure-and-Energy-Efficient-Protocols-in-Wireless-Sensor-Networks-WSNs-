# simulation/node_simulation.py
from protocols.openwsn import OpenWSN
from protocols.dash7 import DASH7
from protocols.energy_model import EnergyModel

class NodeSimulation:
    def __init__(self, protocols, num_cycles=1000, energy_initial=1.0, energy_threshold=0.05):
        """
        Initialize the simulation environment.
        
        :param protocols: Dictionary of protocol instances
        :param num_cycles: Number of simulation cycles
        :param energy_initial: Initial energy per node in Joules
        :param energy_threshold: Energy level below which to switch protocols
        """
        self.protocols = protocols
        self.num_cycles = num_cycles
        self.energy_initial = energy_initial  # Joules
        self.energy_threshold = energy_threshold  # Threshold to switch protocols
        self.energy_model = EnergyModel()

    def switch_protocol(self, current_protocol, energy_level):
        """
        Switch protocols based on energy level.
        
        :param current_protocol: Current protocol name
        :param energy_level: Remaining energy
        :return: New protocol name or current if no switch
        """
        if energy_level < self.energy_threshold:
            # Example logic: Switch between OpenWSN and DASH7
            if "OpenWSN" in current_protocol:
                new_protocol = current_protocol.replace("OpenWSN", "DASH7")
            elif "DASH7" in current_protocol:
                new_protocol = current_protocol.replace("DASH7", "OpenWSN")
            else:
                new_protocol = current_protocol
            return new_protocol
        return current_protocol

    def run_simulation(self):
        """
        Run the simulation across all protocols.
        
        :return: Dictionary containing results for each protocol
        """
        results = {}
        plaintext = b"Environmental data: Temp=25C, Humidity=60%"

        for protocol_name, protocol in self.protocols.items():
            print(f"\nSimulating protocol: {protocol_name}")
            remaining_energy = self.energy_initial
            cycle = 0

            encryption_times = []
            decryption_times = []
            energy_consumptions = []
            packet_sizes = []
            current_protocol = protocol_name

            while cycle < self.num_cycles and remaining_energy > 0:
                current_protocol_instance = self.protocols.get(current_protocol, protocol)
                
                if isinstance(current_protocol_instance, OpenWSN):
                    # For OpenWSN, use prepare_packet
                    packet = current_protocol_instance.prepare_packet(plaintext, headers={"Type": "Data"})
                    packet_size = len(packet['payload']) + len(packet['hmac']) + len(packet['headers']['Type'])

                    # Measure encryption time
                    encryption_time = current_protocol_instance.energy_model.calculate_computation_energy(1)  # One encryption operation
                    encryption_times.append(encryption_time)

                    # Process packet
                    try:
                        decrypted_payload = current_protocol_instance.process_packet(packet)
                        assert decrypted_payload == plaintext, "Decryption failed!"
                    except Exception as e:
                        print(f"Error processing packet: {e}")
                        break

                elif isinstance(current_protocol_instance, DASH7):
                    # For DASH7, use query_response
                    response_packet = current_protocol_instance.query_response("Query1", plaintext)
                    packet_size = len(response_packet['response']) + len(response_packet['hmac']) + len(response_packet['query'])

                    # Measure encryption time
                    encryption_time = current_protocol_instance.energy_model.calculate_computation_energy(1)  # One encryption operation
                    encryption_times.append(encryption_time)

                    # Process response
                    try:
                        decrypted_response = current_protocol_instance.process_response(response_packet)
                        assert decrypted_response == plaintext, "Decryption failed!"
                    except Exception as e:
                        print(f"Error processing response: {e}")
                        break

                else:
                    print(f"Unknown protocol type: {current_protocol}")
                    break

                # Measure energy consumption for transmission
                transmission_energy = current_protocol_instance.energy_model.calculate_transmission_energy(packet_size)
                packet_sizes.append(packet_size)

                # Measure total energy consumption
                total_energy = current_protocol_instance.energy_model.total_energy(packet_size, 1)
                energy_consumptions.append(total_energy)
                remaining_energy -= total_energy

                # Adaptive Protocol Switching
                new_protocol = self.switch_protocol(current_protocol, remaining_energy)
                if new_protocol != current_protocol:
                    print(f"Switching protocol from {current_protocol} to {new_protocol} due to low energy.")
                    current_protocol = new_protocol

                cycle += 1

            # Estimate network lifetime as number of cycles before energy depletion
            network_lifetime = cycle

            # Aggregate results
            total_encryption_time = sum(encryption_times)
            total_decryption_time = total_encryption_time  # Assuming symmetric operations
            total_energy_consumed = sum(energy_consumptions)

            results[protocol_name] = {
                "Encryption Time (s)": total_encryption_time,
                "Decryption Time (s)": total_decryption_time,
                "Energy Consumption (J)": total_energy_consumed,
                "Packet Size (bytes)": sum(packet_sizes) / len(packet_sizes) if packet_sizes else 0,
                "Network Lifetime (cycles)": network_lifetime
            }

            print(f"Protocol: {protocol_name} | Cycles: {network_lifetime} | Energy Consumed: {total_energy_consumed:.6f} J")

        return results
