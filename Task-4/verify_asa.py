from algosdk.v2client import algod
from algosdk import encoding
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Algod client
algod_token = os.getenv("ALGOD_TOKEN", "")
algod_address = os.getenv("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
client = algod.AlgodClient(algod_token, algod_address)

# ASA Configuration
ASA_ID = int(os.getenv("ASA_ID", 741149664))

def get_asa_info(asset_id):
    try:
        asset_info = client.asset_info(asset_id)
        print("\n=== ASA Information ===")
        print(f"Asset ID: {asset_id}")
        print(f"Asset Name: {asset_info['params'].get('name', 'N/A')}")
        print(f"Unit Name: {asset_info['params'].get('unit-name', 'N/A')}")
        print(f"Total Supply: {asset_info['params'].get('total', 0) / (10 ** asset_info['params'].get('decimals', 0))}")
        print("\n=== Roles ===")
        print(f"Manager: {asset_info['params'].get('manager', 'N/A')}")
        print(f"Reserve: {asset_info['params'].get('reserve', 'N/A')}")
        print(f"Freeze: {asset_info['params'].get('freeze', 'N/A')}")
        print(f"Clawback: {asset_info['params'].get('clawback', 'N/A')}")
        return asset_info
    except Exception as e:
        print(f"Error fetching ASA info: {e}")
        return None

if __name__ == "__main__":
    print("=== Verifying ASA Configuration ===")
    print(f"Checking ASA ID: {ASA_ID}")
    get_asa_info(ASA_ID)
