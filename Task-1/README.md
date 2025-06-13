# 🔥 Hackathon Token: HACK (ASA ID: 741146741)

This repository contains the implementation of **Hackathon Token (HACK)**, an Algorand Standard Asset (ASA) created on the Algorand TestNet.

## 🚀 Token Details

- **Token Name**: Hackathon Token
- **Ticker**: HACK
- **Asset ID**: `741146741`
- **Total Supply**: 1,000,000 HACK
- **Decimals**: 6 (1 HACK = 1,000,000 micro-HACK)
- **Creator**: `IAPGHDFZUHEBQ2C5E6GSE75UWOPLNUFGLHVAOVBSQYBORV6URBN2GTGWXA`
- **TestNet Explorer**: [View on AlgoExplorer](https://testnet.algoexplorer.io/asset/741146741)

## 🛠️ Project Structure

```
create-token/
├── projects/
│   └── HackToken/
│       ├── .env                    # Contains your mnemonic
│       └── scripts/
│           ├── create_asset.py    # Script to create the token
│           ├── check_balance.py   # Check token balances
│           └── generate_mnemonic.py # Generate new account
└── README.md                     # This file
```

## 🚀 Quick Start

1. **Set up environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install py-algorand-sdk python-dotenv
   ```

2. **Configure your account**
   - Copy `.env.example` to `.env`
   - Add your mnemonic phrase:
     ```
     MNEMONIC=your_25_word_mnemonic_phrase_here
     ```

## 📜 Scripts

### Create Token
```bash
python projects/HackToken/scripts/create_asset.py
```

### Check Balances
```bash
# Check all token balances
python projects/HackToken/scripts/check_balance.py

# Check specific asset
python projects/HackToken/scripts/check_balance.py 741146741
```

### Generate New Account
```bash
python projects/HackToken/scripts/generate_mnemonic.py
```

## 🤝 Interacting with the Token

### Opt-in to Receive Tokens
Before receiving HACK tokens, an account must opt-in to the asset:

```python
from algosdk.v2client import algod
from algosdk import transaction

# Initialize client
algod_client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")

# Account info
receiver = "RECEIVER_ADDRESS"
private_key = mnemonic.to_private_key("YOUR_MNEMONIC")

# Build opt-in transaction
params = algod_client.suggested_params()
txn = transaction.AssetOptInTxn(
    sender=receiver,
    sp=params,
    index=741146741  # HACK asset ID
)

# Sign and send
stxn = txn.sign(private_key)
txid = algod_client.send_transaction(stxn)
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Opted in to HACK in transaction: {txid}")
```

### Transfer Tokens
```python
# After opt-in, transfer tokens
txn = transaction.AssetTransferTxn(
    sender="SENDER_ADDRESS",
    sp=params,
    receiver=receiver,
    amt=100000,  # 0.1 HACK (6 decimals)
    index=741146741
)

# Sign and send as above
```

## 📊 Token Metrics

- **Circulating Supply**: 1,000,000 HACK
- **Holders**: 1 (initially)
- **Transactions**: View on [AlgoExplorer](https://testnet.algoexplorer.io/asset/741146741)

## 📝 License

MIT License - feel free to use this code as a template for your own Algorand tokens!

## 🙏 Acknowledgements

- [Algorand](https://www.algorand.com/)
- [AlgoKit](https://developer.algorand.org/algokit/)