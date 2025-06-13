from algosdk import account, mnemonic

def generate_account():
    # Generate a new account
    private_key = account.generate_account()[0]
    address = account.address_from_private_key(private_key)
    mnemonic_phrase = mnemonic.from_private_key(private_key)
    
    print("\n=== New Algorand Account Generated ===")
    print(f"Address: {address}")
    print("\nMnemonic (25 words):")
    print(mnemonic_phrase)
    print("\nIMPORTANT: Save these details securely!")
    print("You'll need them to deploy and interact with the contract.")
    print("\nNext steps:")
    print("1. Go to https://bank.testnet.algorand.network/")
    print("2. Paste your address to get testnet ALGOs")
    print("3. Copy the mnemonic and update it in deploy.py")
    
    return address, mnemonic_phrase

if __name__ == "__main__":
    generate_account() 