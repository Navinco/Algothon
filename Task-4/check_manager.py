from algosdk import account, mnemonic

# The manager address we need to match
TARGET_MANAGER = "IAPGHDFZUHEBQ2C5E6GSE75UWOPLNUFGLHVAOVBSQYBORV6URBN2GTGWXA"

# The mnemonic you provided
MNEMONIC = "heart spice twin lyrics tumble guide chief interest fault left equip stadium impact judge sketch seven place purpose shell habit planet decade swamp able first"

try:
    private_key = mnemonic.to_private_key(MNEMONIC)
    address = account.address_from_private_key(private_key)
    
    print(f"Mnemonic decodes to address: {address}")
    print(f"Target manager address:     {TARGET_MANAGER}")
    
    if address == TARGET_MANAGER:
        print("✅ This is the correct manager mnemonic!")
        
        # Save to .env for later use
        with open('manager.env', 'w') as f:
            f.write(f"MANAGER_MNEMONIC=\"{MNEMONIC}\"\n")
            f.write(f"MANAGER_PRIVATE_KEY=\"{private_key}\"\n")
            f.write(f"MANAGER_ADDRESS=\"{address}\"\n")
        print("✅ Manager credentials saved to manager.env")
    else:
        print("❌ This is NOT the manager mnemonic")
        
except Exception as e:
    print(f"Error: {e}")
