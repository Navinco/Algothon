from algosdk import account, mnemonic

private_key, address = account.generate_account()
phrase = mnemonic.from_private_key(private_key)

print(f"🔐 Address: {address}")
print(f"🔑 Mnemonic: {phrase}")
