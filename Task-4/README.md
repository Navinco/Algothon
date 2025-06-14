# Task 4: Multisig Asset Management

This project demonstrates how to manage Algorand Standard Assets (ASA) using a 2-of-3 multisignature account for enhanced security.

## Features

- Create a 2-of-3 multisignature account
- Update ASA roles (manager, clawback, freeze) to use the multisig address
- Perform secure clawback operations requiring multiple signatures
- Comprehensive error handling and transaction confirmation

## Prerequisites

- Python 3.7+
- Algorand TestNet account with some ALGOs for transaction fees
- ASA ID you want to manage (from Task 3)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the example environment file and update with your details:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add:
   - Your ASA ID
   - Optionally, add account mnemonics for existing accounts

## Usage

### 1. Initialize the Multisig Manager

```bash
python multisig_asa_manager.py
```

This will:
1. Generate 3 new accounts (or use provided mnemonics)
2. Create a 2-of-3 multisig account
3. Display account information including addresses and mnemonics

### 2. Update ASA Roles (One-Time Setup)

Uncomment and modify the following section in `multisig_asa_manager.py`:

```python
# Uncomment to actually update ASA roles (requires manager private key)
manager.update_asa_roles(ASA_ID)
```

This will update the ASA's manager, clawback, and freeze addresses to use the multisig address.

### 3. Perform a Clawback Operation

Uncomment and modify the following section in `multisig_asa_manager.py`:

```python
print("\n=== Performing Clawback ===")
tx_id = manager.clawback_asset(
    asa_id=ASA_ID,
    sender=manager.msig.address(),
    receiver=manager.addresses[2],  # Send to third account
    amount=100,  # Amount in base units
    revocation_target=manager.addresses[1]  # Take from second account
)
if tx_id:
    print(f"Clawback successful! Transaction ID: {tx_id}")
else:
    print("Clawback failed.")
```

## Security Notes

- Never commit your `.env` file to version control
- Store private keys and mnemonics securely
- In production, use a secure key management system
- The multisig threshold is set to 2-of-3 by default

## Troubleshooting

- Ensure all accounts have sufficient ALGOs for transaction fees
- Verify the ASA ID is correct and exists on the TestNet
- Check Algorand's network status if transactions are failing

## License

This project is licensed under the MIT License.
