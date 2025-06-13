from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk import transaction
from pyteal import compileTeal, Mode
import base64
import json

# Connect to Algorand node
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
client = algod.AlgodClient(algod_token, algod_address)

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])

def deploy_contract():
    # Read the TEAL files
    with open("approval.teal", "r") as f:
        approval_program = f.read()
    with open("clear.teal", "r") as f:
        clear_program = f.read()

    # Compile the programs
    approval_program_compiled = compile_program(client, approval_program)
    clear_program_compiled = compile_program(client, clear_program)

    # Get the suggested parameters
    params = client.suggested_params()

    # Create the application transaction
    txn = transaction.ApplicationCreateTxn(
        sender=account.address_from_private_key(private_key),
        sp=params,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_program_compiled,
        clear_program=clear_program_compiled,
        global_schema=transaction.StateSchema(num_uints=3, num_byte_slices=1),  # For total_supply, admin, asa_id, and whitelist
        local_schema=transaction.StateSchema(num_uints=1, num_byte_slices=0)    # For balance
    )

    # Sign the transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Submit the transaction
    try:
        client.send_transactions([signed_txn])
        print(f"Deployed contract with transaction ID: {tx_id}")
        
        # Wait for confirmation
        confirmed_txn = transaction.wait_for_confirmation(client, tx_id, 4)
        app_id = confirmed_txn["application-index"]
        print(f"Contract deployed successfully! Application ID: {app_id}")
        return app_id
    except Exception as e:
        print(f"Error deploying contract: {e}")
        return None

if __name__ == "__main__":
    # Your account mnemonic
    private_key = mnemonic.to_private_key("leaf treat inject seek extend noise weekend order prosper mammal moment hero jewel short spoon mention happy vacuum prepare illness session apology nest absorb dirt")
    
    print("Deploying contract...")
    app_id = deploy_contract()
    if app_id:
        print("\nContract deployed successfully!")
        print(f"Application ID: {app_id}")
        print("\nNext steps:")
        print("1. Fund your account with testnet ALGOs")
        print("2. Use the application ID to interact with the contract")
        print("3. Call 'get_info' to verify the ASA connection") 