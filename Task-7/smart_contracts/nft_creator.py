from pyteal import *

def nft_creator_approval(admin_address: str):
    return And(
        Txn.application_id() == Int(0),
        Txn.sender() == Addr(admin_address)  # Only admin can create NFT
    )

def nft_creator_clear():
    return Return(Int(1))
