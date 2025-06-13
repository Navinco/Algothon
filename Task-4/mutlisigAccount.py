from algosdk import account, mnemonic
from algosdk.transaction import Multisig, MultisigTransaction
from algosdk.transaction import AssetTransferTxn
from algosdk.v2client import algod

algod_token = ""
algod_address = "https://testnet-api.algonode.cloud"
# Generate 3 accounts
private_keys = [account.generate_account()[0] for _ in range(3)]
addresses = [account.address_from_private_key(sk) for sk in private_keys]

# Define multisig parameters (version 1, threshold 2)
msig = Multisig(version=1, threshold=2, addresses=addresses)

print("Multisig Address:", msig.address())
print("Signers:", addresses)

algod_client = algod.AlgodClient(algod_token, algod_address)
params = algod_client.suggested_params()

clawback_txn = AssetTransferTxn(
    sender=msig.address(),
    sp=params,
    receiver=addresses[2],         # to whom you send the ASA
    amt=10,
    index=741148236,           # replace with actual ASA ID
    revocation_target=addresses[1] # from whom to clawback
)

mtx = MultisigTransaction(clawback_txn, msig)
mtx.sign(private_keys[0])  # first signer
mtx.sign(private_keys[1])  # second signer

# txid = algod_client.send_raw_transaction(bytes(mtx))
from algosdk import encoding

txid = algod_client.send_raw_transaction(encoding.msgpack_encode(mtx))

print("Multisig Clawback TxID:", txid)