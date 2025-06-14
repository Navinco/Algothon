from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk import transaction
import base64
import os

# Setup client
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
client = algod.AlgodClient(algod_token, algod_address)

# Get keys
mnemonic_phrase = "mercy fat escape very tomato dumb tuition glue boil boring excess rookie business because poem remove eye unaware blue fold wagon gospel news absorb sustain"
private_key = mnemonic.to_private_key(mnemonic_phrase)
sender = account.address_from_private_key(private_key)

# App ID from deployment
app_id = 741174713  # Your app ID

# Create transaction
params = client.suggested_params()

# App call to update ASA ID
app_args = [
    b"update_asa_id",
    741149664  # Your ASA ID
]

txn = transaction.ApplicationNoOpTxn(
    sender=sender,
    sp=params,
    index=app_id,
    app_args=app_args,
)

# Sign and send
signed_txn = txn.sign(private_key)
tx_id = client.send_transaction(signed_txn)
print(f"Sent update ASA ID transaction: {tx_id}")

# Wait for confirmation
result = transaction.wait_for_confirmation(client, tx_id, 4)
print(f"Transaction confirmed in round: {result.get('confirmed-round', 0)}")

# Verify the update
print("\nVerifying update...")
app_info = client.application_info(app_id)
print("Current app state:", app_info['params']['global-state'])
