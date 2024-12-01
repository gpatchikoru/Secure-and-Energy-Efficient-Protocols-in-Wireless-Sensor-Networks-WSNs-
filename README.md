# Secure and Energy-Efficient Protocols in Wireless Sensor Networks (WSNs)

## Project Overview

This project designs and implements secure, energy-efficient protocols for Wireless Sensor Networks (WSNs). It focuses on enhancing data integrity, confidentiality, and authentication while optimizing energy consumption to prolong network lifetime. The project compares different encryption algorithms integrated with popular WSN protocols and evaluates their performance based on various metrics.

## Features

- **Encryption Algorithms**: AES, SPECK, PRESENT, Selective Encryption
- **Protocols**: OpenWSN, DASH7
- **Metrics**:
  - Encryption Time
  - Decryption Time
  - Energy Consumption
  - Packet Size
  - Network Longevity

## File Structure

```plaintext
wsn_project/
│
├── main.py                      # Main script for running the simulation
├── encryption/                  # Encryption implementations
│   ├── aes.py                   # AES implementation
│   ├── speck.py                 # SPECK implementation
│   ├── present.py               # PRESENT implementation
│   ├── selective_encryption.py  # Selective encryption implementation
│   ├── hmac_util.py             # HMAC utilities
│   ├── key_management.py        # Lightweight key management
│   ├── __init__.py
│
├── protocols/                   # Protocol implementations
│   ├── openwsn.py               # OpenWSN protocol implementation
│   ├── dash7.py                 # DASH7 protocol implementation
│   ├── energy_model.py          # Energy consumption model
│   ├── __init__.py
│
├── evaluation/                  # Evaluation utilities
│   ├── performance.py           # Performance metrics
│   ├── visualizer.py            # Visualization tools
│   ├── __init__.py
│
├── simulation/                  # WSN simulation environment
│   ├── node_simulation.py       # Simulate nodes with protocols and metrics
│   ├── __init__.py
│
├── results/                     # Generated result plots
│   ├── encryption_time.png
│   ├── decryption_time.png
│   ├── energy_consumption.png
│   ├── network_longevity.png
│   ├── packet_size.png
│
├── tests/                       # Test scripts
│   ├── test_encryption.py
│   ├── test_protocols.py
│   ├── test_key_management.py
│
├── requirements.txt             # Dependencies
└── README.md                    # Project documentation
