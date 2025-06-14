import os
from algosdk import account, mnemonic, encoding
from algosdk.transaction import (
    Multisig,
    MultisigTransaction,
    AssetConfigTxn,
    AssetTransferTxn,
    wait_for_confirmation
)
from algosdk.v2client import algod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Algod client
algod_token = os.getenv("ALGOD_TOKEN", "")
algod_address = os.getenv("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
client = algod.AlgodClient(algod_token, algod_address)

# ASA Configuration
ASA_ID = int(os.getenv("ASA_ID", 741149664))  # Default to your ASA ID from Task 3

class MultisigASAManager:
    def __init__(self, mnemonics=None):
        """Initialize with optional list of 3 mnemonics."""
        if mnemonics and len(mnemonics) == 3:
            self.private_keys = [mnemonic.to_private_key(m) for m in mnemonics]
            self.addresses = [account.address_from_private_key(sk) for sk in self.private_keys]
        else:
            # Generate new accounts if none provided
            self.private_keys = [account.generate_account()[0] for _ in range(3)]
            self.addresses = [account.address_from_private_key(sk) for sk in self.private_keys]
        
        # Create 2-of-3 multisig
        self.msig = Multisig(version=1, threshold=2, addresses=self.addresses)
    
    def account_info(self):
        """Print account information."""
        print("\n=== Multisig Account ===")
        print(f"Address: {self.msig.address()}")
        print("\nSigners:")
        for i, (addr, sk) in enumerate(zip(self.addresses, self.private_keys)):
            print(f"{i+1}. Address: {addr}")
            print(f"   Private key: {sk}")
            print(f"   Mnemonic: {mnemonic.from_private_key(sk)}\n")
    
    def update_asa_roles(self, asa_id, manager_address=None, clawback_address=None, freeze_address=None):
        """Update ASA roles to use the multisig address."""
        params = client.suggested_params()
        
        # Get current ASA info to preserve existing settings
        try:
            asset_info = client.asset_info(asa_id)
            current_manager = asset_info['params']['manager']
            current_clawback = asset_info['params'].get('clawback', '')
            current_freeze = asset_info['params'].get('freeze', '')
        except Exception as e:
            print(f"Error fetching asset info: {e}")
            return None
        
        # Use provided addresses or current ones
        manager = manager_address or current_manager
        clawback = clawback_address or current_clawback or self.msig.address()
        freeze = freeze_address or current_freeze or self.msig.address()
        
        # Create the transaction
        txn = AssetConfigTxn(
            sender=current_manager,  # Must be the current manager
            sp=params,
            index=asa_id,
            manager=manager,
            reserve=asset_info['params']['reserve'],
            freeze=freeze,
            clawback=clawback,
            strict_empty_address_check=False
        )
        
        # Sign and submit
        return self._sign_and_submit(txn, [self.private_keys[0]])  # Assuming first account is the current manager
    
    def clawback_asset(self, asa_id, sender, receiver, amount, revocation_target):
        """Perform a clawback operation using the multisig."""
        params = client.suggested_params()
        
        txn = AssetTransferTxn(
            sender=sender,
            sp=params,
            receiver=receiver,
            amt=amount,
            index=asa_id,
            revocation_target=revocation_target
        )
        
        # Sign with first two private keys (2-of-3)
        return self._sign_and_submit(txn, self.private_keys[:2])
    
    def _sign_and_submit(self, txn, signers):
        """Helper to sign and submit a transaction."""
        # Create multisig transaction
        mtx = MultisigTransaction(txn, self.msig)
        
        # Sign with provided keys
        for sk in signers:
            mtx.sign(sk)
        
        try:
            # Send the transaction
            tx_id = client.send_raw_transaction(mtx.encode())
            print(f"Transaction sent with ID: {tx_id}")
            
            # Wait for confirmation
            result = wait_for_confirmation(client, tx_id, 4)
            print(f"Transaction confirmed in round: {result['confirmed-round']}")
            return tx_id
            
        except Exception as e:
            print(f"Error submitting transaction: {e}")
            return None

def main():
    print("=== Algorand Multisig ASA Manager ===\n")
    
    # Load mnemonics from environment if available
    mnemonics = [
        os.getenv("ACCOUNT1_MNEMONIC"),
        os.getenv("ACCOUNT2_MNEMONIC"),
        os.getenv("ACCOUNT3_MNEMONIC")
    ]
    
    if all(mnemonics):
        manager = MultisigASAManager(mnemonics)
    else:
        print("No mnemonics provided in .env, generating new accounts...")
        manager = MultisigASAManager()
    
    # Display account info
    manager.account_info()
    
    # Example: Update ASA roles to use multisig
    print("\n=== Updating ASA Roles ===")
    print(f"ASA ID: {ASA_ID}")
    print(f"Setting manager/clawback/freeze to: {manager.msig.address()}")
    
    # Uncomment to actually update ASA roles (requires manager private key)
    # manager.update_asa_roles(ASA_ID)
    
    # Example: Perform a clawback (uncomment and modify as needed)
    # print("\n=== Performing Clawback ===")
    # tx_id = manager.clawback_asset(
    #     asa_id=ASA_ID,
    #     sender=manager.msig.address(),
    #     receiver=manager.addresses[2],  # Send to third account
    #     amount=100,  # Amount in base units
    #     revocation_target=manager.addresses[1]  # Take from second account
    # )
    # if tx_id:
    #     print(f"Clawback successful! Transaction ID: {tx_id}")
    # else:
    #     print("Clawback failed.")

if __name__ == "__main__":
    main()
