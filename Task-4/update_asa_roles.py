from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
from algosdk.transaction import AssetConfigTxn
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

# Current manager's mnemonic (verified from Task 1)
CURRENT_MANAGER_MNEMONIC = "heart spice twin lyrics tumble guide chief interest fault left equip stadium impact judge sketch seven place purpose shell habit planet decade swamp able first"
CURRENT_MANAGER_PK = mnemonic.to_private_key(CURRENT_MANAGER_MNEMONIC)
CURRENT_MANAGER_ADDR = account.address_from_private_key(CURRENT_MANAGER_PK)

def update_asa_roles():
    print("=== Updating ASA Roles ===")
    print(f"ASA ID: {ASA_ID}")
    print(f"Current Manager: {CURRENT_MANAGER_ADDR}")
    
    # Get current ASA info
    try:
        asset_info = client.asset_info(ASA_ID)
        print("\nCurrent ASA Info:")
        print(f"Name: {asset_info['params'].get('name', 'N/A')}")
        print(f"Manager: {asset_info['params'].get('manager', 'N/A')}")
        print(f"Clawback: {asset_info['params'].get('clawback', 'N/A')}")
        print(f"Freeze: {asset_info['params'].get('freeze', 'N/A')}")
        
        # Set the new multisig address (from the previous output)
        new_multisig_addr = "JW7WTZD4ZIDMOJR5M4GM3VRCBWRTMSEZXUKTGRVM5RMH5NNTEUWYKNMTQU"
        
        # Prepare transaction
        params = client.suggested_params()
        txn = AssetConfigTxn(
            sender=CURRENT_MANAGER_ADDR,
            sp=params,
            index=ASA_ID,
            manager=new_multisig_addr,
            reserve=asset_info['params']['reserve'],
            freeze=new_multisig_addr,
            clawback=new_multisig_addr,
            strict_empty_address_check=False
        )
        
        print(f"\nUpdating roles to use multisig: {new_multisig_addr}")
        
        # Sign and submit
        stxn = txn.sign(CURRENT_MANAGER_PK)
        tx_id = client.send_transaction(stxn)
        print(f"Transaction ID: {tx_id}")
        
        # Wait for confirmation
        result = transaction.wait_for_confirmation(client, tx_id, 4)
        print(f"Transaction confirmed in round: {result['confirmed-round']}")
        print("\nASA roles updated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_asa_roles()
