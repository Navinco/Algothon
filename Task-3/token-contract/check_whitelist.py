from algosdk.v2client import algod
from algosdk import encoding
import base64
import sys

def check_whitelist(app_id, address):
    # Initialize the client
    algod_address = "https://testnet-api.algonode.cloud"
    client = algod.AlgodClient("", algod_address)
    
    # Get application info
    app_info = client.application_info(app_id)
    
    # The key we're looking for
    whitelist_key = "Whitelist" + address
    print(f"Looking for whitelist key: {whitelist_key}")
    
    # Print all global state for debugging
    print("\nGlobal state:")
    for state in app_info['params']['global-state']:
        key = state['key']
        value = state['value']
        
        # Decode key if it's base64 encoded
        try:
            decoded_key = base64.b64decode(key).decode('utf-8')
            print(f"Key: {decoded_key} (raw: {key})")
            
            # Check if this is our whitelist key
            if decoded_key == whitelist_key:
                print(f"Found matching whitelist entry!")
                return True
                
        except Exception as e:
            print(f"Could not decode key {key}: {e}")
    
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_whitelist.py <app_id> <address>")
        sys.exit(1)
        
    app_id = int(sys.argv[1])
    address = sys.argv[2]
    
    print(f"Checking if {address} is whitelisted in app {app_id}...")
    is_whitelisted = check_whitelist(app_id, address)
    print(f"\nResult: {address} is {'whitelisted' if is_whitelisted else 'not whitelisted'} in app {app_id}")
