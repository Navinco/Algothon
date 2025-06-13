# Task 2: Add Metadata & Asset Controls

This task enhances the Algorand Standard Asset (ASA) with metadata and advanced asset controls as per the ARC-53 standard.

## 🎯 Features Implemented

- **ARC-53 Metadata**
  - IPFS image URL
  - Asset description
  - MIME type specification
  - Metadata hash

- **Asset Controls**
  - Manager address configuration
  - Reserve address setup
  - Freeze address for account freezing
  - Clawback address for asset recovery

- **Demonstration Functions**
  - Asset freezing for specific addresses
  - Asset clawback functionality

## 🛠️ Prerequisites

- Python 3.8+
- Algorand TestNet account with ALGOs for transactions
- `.env` file with your mnemonic phrase

## 🚀 Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your mnemonic:
   ```
   MNEMONIC="your 25-word mnemonic phrase here"
   ```

## 📝 Usage

### 1. Create Asset with Metadata

```bash
python projects/HackToken/scripts/configure_asset.py
```

Select option 1 to create a new asset with metadata.

### 2. Freeze Asset for an Address

```bash
python projects/HackToken/scripts/configure_asset.py
```

Select option 2 and provide:
- Asset ID
- Target address to freeze

### 3. Clawback Assets

```bash
python projects/HackToken/scripts/configure_asset.py
```

Select option 3 and provide:
- Asset ID
- Receiver address
- Amount to clawback

## 🔍 Verification

1. Check the asset on [AlgoExplorer TestNet](https://testnet.algoexplorer.io/)
2. Verify metadata and roles in the asset configuration
3. Confirm freeze and clawback operations work as expected

## 📁 Project Structure

```
Task-2/
├── projects/
│   └── HackToken/
│       └── scripts/
│           └── configure_asset.py
├── .env.example
├── requirements.txt
└── README.md
```

## 📜 Notes

- Ensure your account has sufficient ALGOs for transaction fees
- The IPFS URL in the example is a placeholder - replace it with your actual IPFS hash
- Always test with small amounts first on TestNet before using on MainNet
