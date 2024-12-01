# main.py
from encryption.aes import AES
from encryption.speck import SpeckCipher
from encryption.present import PresentCipher
from encryption.selective_encryption import SelectiveEncryption
from encryption.chacha20_cipher import ChaCha20Cipher  # Newly added
from encryption.key_management import KeyManagement
from protocols.openwsn import OpenWSN
from protocols.dash7 import DASH7
from protocols.energy_model import EnergyModel
from evaluation.performance import PerformanceEvaluator
from evaluation.visualizer import Visualizer
from evaluation.report_generator import ReportGenerator
from simulation.node_simulation import NodeSimulation

def main():
    # Initialize Key Management
    key_mgmt = KeyManagement()
    node_ids = [f"Node_{i}" for i in range(1, 7)]  # Example node IDs
    key_mgmt.distribute_keys(node_ids)

    # Initialize Encryption Algorithms with keys
    aes = AES()
    speck = SpeckCipher()
    present = PresentCipher()
    chacha20 = ChaCha20Cipher()  # Newly added
    selective_aes = SelectiveEncryption(aes, encryption_ratio=0.5)  # 50% selective encryption

    # Initialize Energy Model
    energy_model = EnergyModel()

    # Initialize Protocols with Encryption and Energy Model
    protocols = {
        "OpenWSN_AES": OpenWSN(aes, energy_model),
        "OpenWSN_SPECK": OpenWSN(speck, energy_model),
        "OpenWSN_PRESENT": OpenWSN(present, energy_model),
        "OpenWSN_ChaCha20": OpenWSN(chacha20, energy_model),  # Newly added
        "DASH7_AES": DASH7(aes, energy_model),
        "DASH7_SPECK": DASH7(speck, energy_model),
        "DASH7_PRESENT": DASH7(present, energy_model),
        "DASH7_ChaCha20": DASH7(chacha20, energy_model),  # Newly added
        "OpenWSN_SelectiveAES": OpenWSN(selective_aes, energy_model)
    }

    # Initialize Node Simulation
    simulation = NodeSimulation(protocols, num_cycles=1000, energy_initial=1.0)  # 1 Joule initial energy
    results = simulation.run_simulation()

    # Display Results
    print("\n=== Simulation Results ===")
    for protocol, metrics in results.items():
        print(f"{protocol}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value}")
        print()

    # Visualize Results
    visualizer = Visualizer()
    visualizer.visualize_results(results)

    # Generate PDF Report
    report_generator = ReportGenerator()
    report_generator.generate_pdf_report(results)

if __name__ == "__main__":
    main()
