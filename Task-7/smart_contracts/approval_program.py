from pyteal import *

def approval_program(admin: str):
    on_create = Seq([
        Assert(Txn.sender() == Addr(admin)),
        Return(Int(1))
    ])

    on_buy = Seq([
        Assert(Global.group_size() == Int(2)),  # 2 multisig signed Txn
        App.globalPut(Bytes("NFT_Bought"), Int(1)),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, on_buy]
    )

    return program
