from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import base64

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""
APP_ID = 741149985
ASA_ID = 741148236
mnemonic_phrase = "leaf treat inject seek extend noise weekend order prosper mammal moment hero jewel short spoon mention happy vacuum prepare illness session apology nest absorb dirt"
private_key = mnemonic.to_private_key(mnemonic_phrase)
sender = account.address_from_private_key(private_key)
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# CHANGE THESE TO THE SENDER AND RECEIVER ADDRESSES
receiver = "PUT_RECEIVER_ADDRESS_HERE"
amount = 5  # Number of tokens to transfer

def transfer_tokens():
    params = client.suggested_params()
    app_args = [b"transfer", b"", amount.to_bytes(8, 'big')]
    app_call = transaction.ApplicationNoOpTxn(
        sender=sender,
        sp=params,
        index=APP_ID,
        app_args=app_args,
        accounts=[receiver],
        foreign_assets=[ASA_ID]
    )
    asset_send = transaction.AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=receiver,
        amt=amount,
        index=ASA_ID
    )
    gid = transaction.calculate_group_id([app_call, asset_send])
    app_call.group = gid
    asset_send.group = gid
    stxn1 = app_call.sign(private_key)
    stxn2 = asset_send.sign(private_key)
    tx_id = client.send_transactions([stxn1, stxn2])
    print(f"Sent transfer group, tx id: {tx_id}")
    result = transaction.wait_for_confirmation(client, tx_id, 4)
    print("Confirmed in round:", result["confirmed-round"])
    logs = result["logs"] if "logs" in result else []
    print("Contract logs:")
    for log in logs:
        print(base64.b64decode(log))

if __name__ == "__main__":
    transfer_tokens() 