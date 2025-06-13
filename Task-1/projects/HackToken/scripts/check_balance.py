from algosdk.v2client import algod
from algosdk import mnemonic, account
import os
from dotenv import load_dotenv
import sys

# Load environment variables from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

def get_account_from_env():
    m = os.getenv("MNEMONIC")
    if not m:
        raise Exception("❌ 'MNEMONIC' not set in .env file.")
    private_key = mnemonic.to_private_key(m)
    address = account.address_from_private_key(private_key)
    return address

def check_balance(asset_id=None):
    # Initialize Algod client for TestNet
    algod_address = "https://testnet-api.algonode.cloud"
    algod_client = algod.AlgodClient("", algod_address)
    
    try:
        # Get account from .env
        address = get_account_from_env()
        print(f"🔍 Checking balance for address: {address}")
        
        # Get account info
        account_info = algod_client.account_info(address)
        
        # Print ALGO balance
        algo_balance = account_info.get('amount', 0) / 1e6
        print(f"\n💰 ALGO Balance: {algo_balance} ALGO")
        
        # Print all assets if no specific asset_id provided
        assets = account_info.get('assets', [])
        if not assets:
            print("\n📭 No other assets found in this account.")
        else:
            print("\n📦 Asset Balances:")
            for asset in assets:
                asset_id = asset['asset-id']
                amount = asset['amount']
                print(f"   - Asset ID: {asset_id}, Balance: {amount} units")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # If an asset ID is provided as a command-line argument, check that specific asset
    asset_id = int(sys.argv[1]) if len(sys.argv) > 1 else None
    check_balance(asset_id)
