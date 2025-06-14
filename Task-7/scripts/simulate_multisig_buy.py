# -*- coding: utf-8 -*-
from algosdk import mnemonic, account
from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn, Multisig, MultisigTransaction
from algosdk.error import WrongKeyLengthError, AlgodHTTPError
import base64
import sys

def handle_error(error, error_type="Unknown"):
    """Format error message for better readability"""
    error_msg = f"Error Type: {error_type}\n"
    error_msg += f"Error Details: {str(error)}\n"
    if hasattr(error, 'response'):
        error_msg += f"Response: {error.response.text}\n"
    print(error_msg, file=sys.stderr)
    return error_msg

# Connect to Algorand node
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)

# These will be injected by the backend via subprocess
mnemonic1 = "mnemonic1"
mnemonic2 = "mnemonic2"

# Add your third team member's mnemonic here permanently (since only 2 sign at a time)
mnemonic3 = "nurse point pledge ahead guide axis frog print flag sample strategy clip tip also small angle purity plug sword enter pull meat poem about patient"

try:
    # Validate that mnemonics are different
    if mnemonic1 == mnemonic2:
        raise Exception("Error: Both mnemonics are the same. Please use different mnemonics for different team members.")

    # Convert mnemonics to private keys
    try:
        private_key1 = mnemonic.to_private_key(mnemonic1)
        private_key2 = mnemonic.to_private_key(mnemonic2)
        private_key3 = mnemonic.to_private_key(mnemonic3)
    except Exception as e:
        raise Exception(f"Failed to convert mnemonics to private keys: {str(e)}")
    
    # Get public keys (addresses)
    try:
        public_key1 = account.address_from_private_key(private_key1)
        public_key2 = account.address_from_private_key(private_key2)
        public_key3 = account.address_from_private_key(private_key3)
    except Exception as e:
        raise Exception(f"Failed to generate public keys: {str(e)}")
    
    # Validate that addresses are different
    if public_key1 == public_key2:
        raise Exception("Error: Both mnemonics generate the same address. Please use different mnemonics for different team members.")
    
    print(f"Generated addresses:")
    print(f"Address 1: {public_key1}")
    print(f"Address 2: {public_key2}")
    print(f"Address 3: {public_key3}")
    
    # Create multisig account
    try:
        msig = Multisig(version=1, threshold=2, addresses=[public_key1, public_key2, public_key3])
        msig_address = msig.address()
        print("\n" + "="*50)
        print(f"IMPORTANT: Fund this multisig address first:")
        print(f"Address: {msig_address}")
        print("Steps to fund:")
        print("1. Go to https://bank.testnet.algorand.network/")
        print("2. Paste the address above")
        print("3. Request at least 0.1 ALGO")
        print("4. Wait for confirmation")
        print("="*50 + "\n")
        
        # Check account balance
        try:
            account_info = algod_client.account_info(msig_address)
            balance = account_info.get('amount', 0)
            print(f"Current balance: {balance} microAlgos")
            
            if balance < 1000:
                raise Exception(f"Please fund the multisig account {msig_address} with at least 0.1 ALGO using the Algorand Testnet Dispenser (https://bank.testnet.algorand.network/)")
                
        except Exception as e:
            if "account not found" in str(e).lower():
                raise Exception(f"Please fund the multisig account {msig_address} with at least 0.1 ALGO using the Algorand Testnet Dispenser (https://bank.testnet.algorand.network/)")
            else:
                raise Exception(f"Failed to check account balance: {str(e)}")
                
    except Exception as e:
        raise Exception(f"Failed to create multisig account: {str(e)}")
    
    # Get suggested parameters
    try:
        params = algod_client.suggested_params()
    except AlgodHTTPError as e:
        raise Exception(f"Failed to get suggested parameters: {str(e)}")
    
    # Create transaction
    try:
        # Use one of the team member addresses as the receiver for testing
        receiver = public_key1  # For testing, we'll send to the first address
        
        txn = PaymentTxn(
            sender=msig_address,
            sp=params,
            receiver=receiver,
            amt=1000  # 0.001 ALGO
        )
    except Exception as e:
        raise Exception(f"Failed to create transaction: {str(e)}")
    
    # Create and sign multisig transaction
    try:
        mtxn = MultisigTransaction(txn, msig)
        mtxn.sign(private_key1)
        mtxn.sign(private_key2)
    except Exception as e:
        raise Exception(f"Failed to sign transaction: {str(e)}")
    
    # Send transaction
    try:
        txid = algod_client.send_transaction(mtxn)
        print(f"Transaction sent with ID: {txid}")
    except AlgodHTTPError as e:
        if "Invalid number of signatures" in str(e):
            raise Exception("Transaction signing failed: Not enough valid signatures. Make sure both mnemonics are correct and the accounts have sufficient funds.")
        else:
            raise Exception(f"Failed to send transaction: {str(e)}")
    
    # Wait for confirmation
    try:
        confirmed_txn = algod_client.pending_transaction_info(txid)
        print(f"Transaction confirmed in round {confirmed_txn.get('confirmed-round', 0)}")
    except Exception as e:
        print(f"Warning: Could not confirm transaction: {str(e)}")

except WrongKeyLengthError as e:
    error_msg = handle_error(e, "Invalid Key Length")
    raise Exception("Invalid key length. Make sure you're using valid Algorand addresses.")
except AlgodHTTPError as e:
    error_msg = handle_error(e, "Algorand Network Error")
    raise Exception(f"Network error: {str(e)}")
except Exception as e:
    error_msg = handle_error(e, "Transaction Error")
    raise Exception(str(e))

# from algosdk import account, mnemonic
# from algosdk.transaction import Multisig, MultisigTransaction
# from algosdk.transaction import AssetTransferTxn
# from algosdk.v2client import algod

# algod_token = ""
# algod_address = "https://testnet-api.algonode.cloud"

# mnemonic1 = "mnemonic1"
# mnemonic2 = "mnemonic2"
# mnemonic3 = "nurse point pledge ahead guide axis frog print flag sample strategy clip tip also small angle purity plug sword enter pull meat poem about patient"
# # Generate 3 accounts
# private_keys = [mnemonic.to_private_key(mnemonic1), mnemonic.to_private_key(mnemonic2), mnemonic.to_private_key(mnemonic3)]
# addresses = [account.address_from_private_key(sk) for sk in private_keys]

# # Define multisig parameters (version 1, threshold 2)
# msig = Multisig(version=1, threshold=2, addresses=addresses)

# print("Multisig Address:", msig.address())
# print("Signers:", addresses)

# algod_client = algod.AlgodClient(algod_token, algod_address)
# params = algod_client.suggested_params()

# clawback_txn = AssetTransferTxn(
#     sender=msig.address(),
#     sp=params,
#     receiver=addresses[2],         # to whom you send the ASA
#     amt=10,
#     index=741148236,           # replace with actual ASA ID
#     revocation_target=addresses[1] # from whom to clawback
# )

# mtx = MultisigTransaction(clawback_txn, msig)
# mtx.sign(private_keys[0])  # first signer
# mtx.sign(private_keys[1])  # second signer

# # txid = algod_client.send_raw_transaction(bytes(mtx))
# from algosdk import encoding

# txid = algod_client.send_raw_transaction(encoding.msgpack_encode(mtx))

# print("Multisig Clawback TxID:", txid)
