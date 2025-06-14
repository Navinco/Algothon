from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import base64
import sys

# Initialize client
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
client = algod.AlgodClient(algod_token, algod_address)

# Application ID from deployment
APP_ID = 741174790

# Admin account
mnemonic_phrase = "leaf treat inject seek extend noise weekend order prosper mammal moment hero jewel short spoon mention happy vacuum prepare illness session apology nest absorb dirt"
private_key = mnemonic.to_private_key(mnemonic_phrase)
sender = account.address_from_private_key(private_key)

def add_to_whitelist():
    if len(sys.argv) != 2:
        print("Usage: python add_to_whitelist.py <address_to_whitelist>")
        sys.exit(1)
        
    address_to_whitelist = sys.argv[1]
    
    print(f"Admin account: {sender}")
    print(f"Adding to whitelist: {address_to_whitelist}")
    
    try:
        # Prepare transaction
        params = client.suggested_params()
        app_args = [b"add_to_whitelist"]
        
        # Create the transaction
        txn = transaction.ApplicationNoOpTxn(
            sender=sender,
            sp=params,
            index=APP_ID,
            app_args=app_args,
            accounts=[address_to_whitelist]
        )
        
        # Sign and send
        signed_txn = txn.sign(private_key)
        tx_id = client.send_transaction(signed_txn)
        print(f"Sent add_to_whitelist call, tx id: {tx_id}")
        
        # Wait for confirmation
        result = transaction.wait_for_confirmation(client, tx_id, 4)
        print("Confirmed in round:", result["confirmed-round"])
        
        # Print logs
        if "logs" in result and result["logs"]:
            print("Contract logs:")
            for log in result["logs"]:
                try:
                    print("-", base64.b64decode(log).decode('utf-8'))
                except:
                    print("-", log)
        else:
            print("No logs in transaction")
            
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'args') and len(e.args) > 0 and 'data' in e.args[0]:
            print("Error details:", e.args[0]['data'])

if __name__ == "__main__":
    add_to_whitelist()