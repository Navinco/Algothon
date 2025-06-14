# from algosdk import mnemonic
# from algosdk.future.transaction import PaymentTxn, Multisig, MultisigTransaction
# from algokit_utils import get_algod_client

# algod = get_algod_client()
# team_mnemonics = ["mnemonic1", "mnemonic2", "mnemonic3"]  # Replace with your mnemonics

# keys = [mnemonic.to_private_key(m) for m in team_mnemonics]
# addresses = [mnemonic.to_public_key(m) for m in team_mnemonics]

# msig = Multisig(version=1, threshold=2, addresses=addresses)
# params = algod.suggested_params()
# txn = PaymentTxn(msig.address(), params, receiver="NFT_SELLER_ADDRESS", amt=100000)
# mtxn = MultisigTransaction(txn, msig)

# mtxn.sign(keys[0])
# mtxn.sign(keys[1])
# algod.send_raw_transaction(mtxn.serialize())
# print("NFT buy simulated with 2-of-3 multisig")

from algosdk import mnemonic
from algosdk.future.transaction import PaymentTxn, Multisig, MultisigTransaction
from algokit_utils import get_algod_client

algod = get_algod_client()

# These will be injected by the backend via subprocess
mnemonic1 = "mnemonic1"
mnemonic2 = "mnemonic2"

# Add your third team member's mnemonic here permanently (since only 2 sign at a time)
mnemonic3 = "nurse point pledge ahead guide axis frog print flag sample strategy clip tip also small angle purity plug sword enter pull meat poem about patient"

team_mnemonics = [mnemonic1, mnemonic2, mnemonic3]

# Convert to keys and addresses
keys = [mnemonic.to_private_key(m) for m in team_mnemonics]
addresses = [mnemonic.to_public_key(m) for m in team_mnemonics]

# Construct multisig
msig = Multisig(version=1, threshold=2, addresses=addresses)
params = algod.suggested_params()

# TODO: replace with actual NFT seller address or admin address
txn = PaymentTxn(msig.address(), params, receiver="NFT_SELLER_ADDRESS", amt=100000)

# Sign with the first two keys (mnemonic1 and mnemonic2)
mtxn = MultisigTransaction(txn, msig)
mtxn.sign(keys[0])
mtxn.sign(keys[1])

# Send transaction
algod.send_raw_transaction(mtxn.serialize())
print("NFT buy simulated with 2-of-3 multisig")
