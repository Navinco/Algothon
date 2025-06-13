# AlgoThon - Algorand Hackathon Project

Welcome to the AlgoThon project! This repository contains various tasks and projects related to Algorand blockchain development.

## 🏗️ Project Structure

```
AlgoThon/
├── Task-1/                    # Task 1: Basic ASA Token Creation
│   └── projects/
│       └── HackToken/
│           └── scripts/
│               ├── create_asset.py
│               ├── check_balance.py
│               └── generate_mnemonic.py
│
└── Task-2/                    # Task 2: Advanced Asset Controls & Metadata
    └── projects/
        └── HackToken/
            └── scripts/
                └── configure_asset.py
```

## 🚀 Getting Started

Each task has its own directory with specific instructions. Navigate to the task you're interested in for more details.

## 📋 Tasks

### 1. Task 1: Basic ASA Token
- Created a custom token on Algorand TestNet
- Implemented scripts for token creation and management
- [View Task 1 Details](Task-1/README.md)

### 2. Task 2: Advanced Asset Controls & Metadata
- Added ARC-53 compliant metadata (IPFS, description, MIME type)
- Implemented asset roles (Manager, Reserve, Freeze, Clawback)
- Added freeze and clawback functionality
- [View Task 2 Details](Task-2/README.md)

## ⚙️ Prerequisites

- Python 3.8+
- Algorand SDK (`pip install py-algorand-sdk`)
- A funded Algorand TestNet account (get ALGOs from the [TestNet Dispenser](https://bank.testnet.algorand.network/))
- Python-dotenv (`pip install python-dotenv`)

## 🔧 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Navinco/Algothon.git
   cd Algothon
   ```

2. Navigate to the task directory and install dependencies:
   ```bash
   cd Task-1  # or Task-2
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` to `.env` and add your mnemonic phrase

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
