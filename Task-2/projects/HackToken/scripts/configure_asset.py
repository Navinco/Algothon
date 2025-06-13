import os
import json
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk import transaction
from dotenv import load_dotenv

# Load environment variables from .env file in the current working directory
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Initialize Algod client
def get_algod_client():
    algod_address = "https://testnet-api.algonode.cloud"
    return algod.AlgodClient("", algod_address)

# Get account from mnemonic
def get_account():
    mnemonic_phrase = os.getenv('MNEMONIC')
    if not mnemonic_phrase:
        raise ValueError("MNEMONIC not found in .env file")
    private_key = mnemonic.to_private_key(mnemonic_phrase)
    address = account.address_from_private_key(private_key)
    return {"private_key": private_key, "address": address}

# Create asset with metadata and roles
def create_asset_with_metadata():
    # Initialize client and account
    algod_client = get_algod_client()
    account_info = get_account()
    
    # Get network suggested parameters
    params = algod_client.suggested_params()
    
    # Asset creation transaction with metadata and roles
    txn = transaction.AssetConfigTxn(
        sender=account_info['address'],
        sp=params,
        total=1_000_000,  # 1M tokens
        decimals=6,       # 6 decimal places
        default_frozen=False,
        unit_name="HACK2",
        asset_name="Hackathon Token V2",
        manager=account_info['address'],
        reserve=account_info['address'],
        freeze=account_info['address'],
        clawback=account_info['address'],
        url="ipfs://bafybeifx7yeb55armcsxwwitkymga5xf53dxiarykms3ygqoc223z5s3di",  # Replace with your IPFS hash
        metadata_hash=b"HACKTOKEN123456HACKTOKEN12345678",  # 32-byte hash
        strict_empty_address_check=False
    )
    
    # Sign and send the transaction
    try:
        signed_txn = txn.sign(account_info['private_key'])
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"✅ Transaction ID: {tx_id}")
        
        # Wait for confirmation with timeout
        print("⏳ Waiting for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 10)
        print(f"✅ Transaction confirmed in round: {confirmed_txn['confirmed-round']}")
        
        # Get the asset ID from the transaction results
        if 'asset-index' in confirmed_txn:
            asset_id = confirmed_txn['asset-index']
            print(f"🎉 Asset created successfully!")
            print(f"   Asset ID: {asset_id}")
            print(f"   View on AlgoExplorer: https://testnet.algoexplorer.io/asset/{asset_id}")
            return asset_id
        else:
            print("❌ Error: No asset ID in transaction response")
            print("Transaction response:", confirmed_txn)
            return None
            
    except Exception as e:
        print(f"❌ Error during transaction: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Freeze an asset
def freeze_asset(asset_id, target_address):
    algod_client = get_algod_client()
    account_info = get_account()
    
    params = algod_client.suggested_params()
    
    txn = transaction.AssetFreezeTxn(
        sender=account_info['address'],
        sp=params,
        index=asset_id,
        target=target_address,
        new_freeze_state=True
    )
    
    signed_txn = txn.sign(account_info['private_key'])
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"Waiting for freeze transaction {tx_id} to be confirmed...")
    transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print(f"Asset {asset_id} frozen for address {target_address}")

# Clawback an asset
def clawback_asset(asset_id, receiver_address, amount):
    algod_client = get_algod_client()
    account_info = get_account()
    
    params = algod_client.suggested_params()
    
    txn = transaction.AssetTransferTxn(
        sender=account_info['address'],
        sp=params,
        receiver=receiver_address,
        amt=amount,
        index=asset_id,
        revocation_target=account_info['address']  # Address to clawback from
    )
    
    signed_txn = txn.sign(account_info['private_key'])
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"Waiting for clawback transaction {tx_id} to be confirmed...")
    transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print(f"Clawed back {amount} of asset {asset_id} to {receiver_address}")

if __name__ == "__main__":
    print("=== Algorand Asset Configuration Tool ===")
    print("1. Create Asset with Metadata")
    print("2. Freeze Asset for Address")
    print("3. Clawback Asset")
    
    choice = input("Select an option (1-3): ")
    
    if choice == "1":
        print("\nCreating asset with metadata...")
        asset_id = create_asset_with_metadata()
        if asset_id:
            print(f"\n🎉 Asset created successfully with ID: {asset_id}")
            print(f"🔗 View on AlgoExplorer: https://testnet.algoexplorer.io/asset/{asset_id}")
    
    elif choice == "2":
        asset_id = int(input("Enter Asset ID: "))
        target_address = input("Enter target address to freeze: ")
        print(f"\nFreezing asset {asset_id} for address {target_address}...")
        freeze_asset(asset_id, target_address)
    
    elif choice == "3":
        asset_id = int(input("Enter Asset ID: "))
        receiver = input("Enter receiver address: ")
        amount = int(input("Enter amount to clawback: "))
        print(f"\nClawing back {amount} of asset {asset_id} to {receiver}...")
        clawback_asset(asset_id, receiver, amount)
    
    else:
        print("Invalid option selected.")
