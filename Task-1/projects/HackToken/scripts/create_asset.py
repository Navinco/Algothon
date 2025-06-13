from algosdk import transaction, account, mnemonic
from algosdk.v2client import algod
import os
from dotenv import load_dotenv

# For type hints
from typing import Any

# Load environment variables from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Helper function to load account from .env
def get_account_from_env():
    m = os.getenv("MNEMONIC")
    if not m:
        raise Exception("❌ 'MNEMONIC' not set in .env file.")
    private_key = mnemonic.to_private_key(m)
    address = account.address_from_private_key(private_key)
    return type('Account', (), {
        'private_key': private_key,
        'address': address
    })

def create_custom_asset(
    algod_client: algod.AlgodClient,
    creator: Any,
    total: int,
    decimals: int,
    unit_name: str,
    asset_name: str,
    url: str
) -> int:
    print(f"\n🚀 Creating {asset_name} ({unit_name}) asset...")
    try:
        params = algod_client.suggested_params()
        params.fee = 2000

        txn = transaction.AssetCreateTxn(
            sender=creator.address,
            sp=params,
            total=total,
            decimals=decimals,
            unit_name=unit_name,
            asset_name=asset_name,
            url=url,
            default_frozen=False,
        )

        signed_txn = txn.sign(creator.private_key)
        txid = algod_client.send_transaction(signed_txn)

        result = transaction.wait_for_confirmation(algod_client, txid, 4)
        asset_id = result['asset-index']

        print(f"✅ {asset_name} created successfully!")
        print(f"📝 Transaction ID: {txid}")
        print(f"🔗 View on AlgoExplorer: https://testnet.algoexplorer.io/asset/{asset_id}")
        return asset_id

    except Exception as e:
        print(f"❌ Failed to create asset: {e}")
        raise

def transfer_asset_to_receiver(
    algod_client: algod.AlgodClient,
    sender: Any,
    receiver_address: str,
    asset_id: int,
    amount: int
) -> str:
    print(f"\n🔄 Transferring {amount} tokens to {receiver_address}...")

    try:
        # Opt-in if needed
        try:
            params = algod_client.suggested_params()
            opt_in_txn = transaction.AssetOptInTxn(
                sender=receiver_address,
                sp=params,
                index=asset_id
            )
            signed_opt_in = opt_in_txn.sign(sender.private_key)
            txid = algod_client.send_transaction(signed_opt_in)
            transaction.wait_for_confirmation(algod_client, txid, 4)
            print("✅ Receiver has opted in to receive the asset")
        except Exception as e:
            if "already opted in" in str(e).lower():
                print("ℹ️  Receiver has already opted in to the asset")
            else:
                print(f"⚠️  Opt-in failed: {e}")

        # Transfer
        params = algod_client.suggested_params()
        transfer_txn = transaction.AssetTransferTxn(
            sender=sender.address,
            sp=params,
            receiver=receiver_address,
            amt=amount,
            index=asset_id
        )

        signed_transfer = transfer_txn.sign(sender.private_key)
        txid = algod_client.send_transaction(signed_transfer)
        transaction.wait_for_confirmation(algod_client, txid, 4)

        print("✅ Transfer completed successfully!")
        print(f"📄 Transaction ID: {txid}")
        print(f"🔗 View on AlgoExplorer: https://testnet.algoexplorer.io/tx/{txid}")
        return txid

    except Exception as e:
        print(f"❌ Transfer failed: {e}")
        raise

def main() -> None:
    algod_address = "https://testnet-api.algonode.cloud"
    algod_client = algod.AlgodClient("", algod_address)

    try:
        print("🔐 Loading account from environment...")
        creator = get_account_from_env()
        print(f"✅ Using account: {creator.address}")

        account_info = algod_client.account_info(creator.address)
        balance = account_info.get('amount', 0) / 1e6
        print(f"💰 Balance: {balance} ALGO")

        if balance < 0.1:
            print("⚠️  Account balance is too low. Please fund via TestNet Dispenser:")
            print(f"🔗 https://bank.testnet.algorand.network/?account={creator.address}")
            return

        print("\n" + "="*50)
        print("🏦 Algorand Token Creator")
        print("="*50)

        asset_id = create_custom_asset(
            algod_client=algod_client,
            creator=creator,
            total=1_000_000,
            decimals=6,
            unit_name="HACK",
            asset_name="Hackathon Token",
            url="https://example.com/hack-token"
        )

        transfer_asset_to_receiver(
            algod_client,
            creator,
            creator.address,  # sending to self
            asset_id,
            amount=100_000
        )

        print("\n🎉 Token creation and transfer completed successfully!")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()