import os
from algokit_utils import get_algod_client, get_indexer_client
from algokit_utils.beta.account_manager import get_localnet_default_account
from algokit_utils.beta.algorand_client import AlgorandClient
from contract import NFTMarketplaceContract

admin_account = get_localnet_default_account()
algorand = AlgorandClient()
app_client = algorand.app(NFTMarketplaceContract(), signer=admin_account)

if app_client.app_id is None:
    app_client.create()
else:
    app_client.update()

print("Deployed App ID:", app_client.app_id)