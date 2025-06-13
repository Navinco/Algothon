from pyteal import *

def approval_program():
    # Define global state keys
    total_supply_key = Bytes("TotalSupply")
    admin_key = Bytes("Admin")
    whitelist_key = Bytes("Whitelist")
    asa_id_key = Bytes("ASA_ID")
    
    # Define local state keys
    balance_key = Bytes("Balance")
    
    # Operations
    mint = Bytes("mint")
    transfer = Bytes("transfer")
    add_to_whitelist = Bytes("add_to_whitelist")
    remove_from_whitelist = Bytes("remove_from_whitelist")
    opt_in = Bytes("opt_in")
    get_info = Bytes("get_info")  # New operation to get contract info
    
    # Helper functions
    def is_admin():
        return Txn.sender() == App.globalGet(admin_key)
    
    def get_balance(account):
        return App.localGet(account, balance_key)
    
    def set_balance(account, amount):
        return App.localPut(account, balance_key, amount)
    
    def is_whitelisted(account):
        return App.globalGet(Concat(whitelist_key, account))
    
    # Program logic
    program = Cond(
        # On creation
        [Txn.application_id() == Int(0),
            Seq([
                App.globalPut(total_supply_key, Int(0)),
                App.globalPut(admin_key, Txn.sender()),
                App.globalPut(asa_id_key, Int(741148236)),
                # Add creator to whitelist
                App.globalPut(Concat(whitelist_key, Txn.sender()), Int(1)),
                Log(Concat(Bytes("Contract created with ASA ID: "), Itob(Int(741148236)))),
                Return(Int(1))
            ])
        ],
        
        # Get info operation
        [Txn.application_args[0] == get_info,
            Seq([
                Log(Concat(Bytes("Total Supply: "), Itob(App.globalGet(total_supply_key)))),
                Log(Concat(Bytes("Admin: "), Txn.sender())),
                Log(Concat(Bytes("ASA ID: "), Itob(App.globalGet(asa_id_key)))),
                Return(Int(1))
            ])
        ],
        
        # Opt-in operation
        [Txn.application_args[0] == opt_in,
            Seq([
                Assert(Txn.application_args.length() == Int(1)),
                # Verify ASA opt-in transaction
                Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
                Assert(Gtxn[1].asset_receiver() == Txn.sender()),
                Assert(Gtxn[1].asset_amount() == Int(0)),
                Assert(Gtxn[1].xfer_asset() == App.globalGet(asa_id_key)),
                Log(Concat(Bytes("User opted in: "), Txn.sender())),
                Return(Int(1))
            ])
        ],
        
        # Mint operation
        [Txn.application_args[0] == mint,
            Seq([
                Assert(is_admin()),
                Assert(Txn.application_args.length() == Int(3)),
                Assert(Btoi(Txn.application_args[2]) > Int(0)),
                # Verify ASA transfer transaction
                Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
                Assert(Gtxn[1].asset_receiver() == Txn.accounts[1]),
                Assert(Gtxn[1].asset_amount() == Btoi(Txn.application_args[2])),
                Assert(Gtxn[1].xfer_asset() == App.globalGet(asa_id_key)),
                App.globalPut(total_supply_key, 
                    App.globalGet(total_supply_key) + Btoi(Txn.application_args[2])),
                set_balance(Txn.accounts[1], 
                    get_balance(Txn.accounts[1]) + Btoi(Txn.application_args[2])),
                Log(Concat(Bytes("Minted "), Txn.application_args[2], Bytes(" tokens to "), Txn.accounts[1])),
                Return(Int(1))
            ])
        ],
        
        # Transfer operation
        [Txn.application_args[0] == transfer,
            Seq([
                Assert(Txn.application_args.length() == Int(3)),
                Assert(Btoi(Txn.application_args[2]) > Int(0)),
                Assert(get_balance(Txn.sender()) >= Btoi(Txn.application_args[2])),
                # Check if sender is whitelisted
                Assert(is_whitelisted(Txn.sender())),
                # Check if receiver is whitelisted
                Assert(is_whitelisted(Txn.accounts[1])),
                # Verify ASA transfer transaction
                Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
                Assert(Gtxn[1].asset_sender() == Txn.sender()),
                Assert(Gtxn[1].asset_receiver() == Txn.accounts[1]),
                Assert(Gtxn[1].asset_amount() == Btoi(Txn.application_args[2])),
                Assert(Gtxn[1].xfer_asset() == App.globalGet(asa_id_key)),
                set_balance(Txn.sender(), 
                    get_balance(Txn.sender()) - Btoi(Txn.application_args[2])),
                set_balance(Txn.accounts[1], 
                    get_balance(Txn.accounts[1]) + Btoi(Txn.application_args[2])),
                Log(Concat(Bytes("Transferred "), Txn.application_args[2], Bytes(" tokens from "), Txn.sender(), Bytes(" to "), Txn.accounts[1])),
                Return(Int(1))
            ])
        ],

        # Add to whitelist operation
        [Txn.application_args[0] == add_to_whitelist,
            Seq([
                Assert(is_admin()),
                Assert(Txn.application_args.length() == Int(2)),
                App.globalPut(Concat(whitelist_key, Txn.accounts[1]), Int(1)),
                Log(Concat(Bytes("Added to whitelist: "), Txn.accounts[1])),
                Return(Int(1))
            ])
        ],

        # Remove from whitelist operation
        [Txn.application_args[0] == remove_from_whitelist,
            Seq([
                Assert(is_admin()),
                Assert(Txn.application_args.length() == Int(2)),
                App.globalDel(Concat(whitelist_key, Txn.accounts[1])),
                Log(Concat(Bytes("Removed from whitelist: "), Txn.accounts[1])),
                Return(Int(1))
            ])
        ]
    )
    
    return program

def clear_state_program():
    return Return(Int(1))

if __name__ == "__main__":
    # Compile the program
    with open("approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=6)
        f.write(compiled)
        print("Generated approval.teal with logging enabled")
    
    with open("clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=6)
        f.write(compiled)
        print("Generated clear.teal")
    
    print("\nContract Operations:")
    print("1. get_info - Get contract information")
    print("2. opt_in - Opt into the ASA")
    print("3. mint - Mint new tokens (admin only)")
    print("4. transfer - Transfer tokens between whitelisted addresses")
    print("5. add_to_whitelist - Add address to whitelist (admin only)")
    print("6. remove_from_whitelist - Remove address from whitelist (admin only)") 