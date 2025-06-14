from algosdk.transaction import MultisigTransaction, MultisigAccount

def is_2_of_3_multisig(txn: MultisigTransaction) -> bool:
    return txn.msig.threshold == 2 and len(txn.msig.subsigs) == 3