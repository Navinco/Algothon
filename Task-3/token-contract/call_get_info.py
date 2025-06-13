from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import base64

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""
APP_ID = 741149985
mnemonic_phrase = "leaf treat inject seek extend noise weekend order prosper mammal moment hero jewel short spoon mention happy vacuum prepare illness session apology nest absorb dirt"
private_key = mnemonic.to_private_key(mnemonic_phrase)
sender = account.address_from_private_key(private_key)
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def call_get_info():
    params = client.suggested_params()
    app_args = [b"get_info"]
    txn = transaction.ApplicationNoOpTxn(
        sender=sender,
        sp=params,
        index=APP_ID,
        app_args=app_args
    )
    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)
    print(f"Sent get_info call, tx id: {tx_id}")
    result = transaction.wait_for_confirmation(client, tx_id, 4)
    print("Confirmed in round:", result["confirmed-round"])
    logs = result["logs"] if "logs" in result else []
    print("Contract logs:")
    for log in logs:
        print(base64.b64decode(log))

if __name__ == "__main__":
    call_get_info() 