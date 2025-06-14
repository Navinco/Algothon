from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import base64

# Connect to Algorand node
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
client = algod.AlgodClient(algod_token, algod_address)

# Your account mnemonic
mnemonic_phrase = "leaf treat inject seek extend noise weekend order prosper mammal moment hero jewel short spoon mention happy vacuum prepare illness session apology nest absorb dirt"
private_key = mnemonic.to_private_key(mnemonic_phrase)
sender = account.address_from_private_key(private_key)

def create_nft():
    params = client.suggested_params()
    txn = transaction.AssetCreateTxn(
        sender=sender,
        sp=params,
        total=1,
        decimals=0,
        default_frozen=False,
        manager=sender,
        reserve=sender,
        freeze=sender,
        clawback=sender,
        unit_name="NFT",
        asset_name="NFT #1",
        url="https://example.com",
        metadata_hash=None
    )

    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)
    print(f"Sent NFT creation transaction with tx id: {tx_id}")
    
    # Wait for confirmation
    result = transaction.wait_for_confirmation(client, tx_id, 4)
    print("Confirmed in round:", result["confirmed-round"])
    print("Asset ID:", result["asset-index"])

if __name__ == "__main__":
    create_nft()
