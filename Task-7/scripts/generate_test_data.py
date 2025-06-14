from algosdk import account
import json
import os

def generate_test_data():
    # Generate 9 test accounts
    accounts = [account.generate_account() for _ in range(9)]
    
    # Create teams data
    teams = {
        "team1": [accounts[0][0], accounts[1][0], accounts[2][0]],  # Using public keys
        "team2": [accounts[3][0], accounts[4][0], accounts[5][0]],
        "team3": [accounts[6][0], accounts[7][0], accounts[8][0]]
    }
    
    # Create player levels data
    levels = {
        accounts[0][0]: 0,  # team1 members
        accounts[1][0]: 0,
        accounts[2][0]: 0,
        accounts[3][0]: 40,  # team2 members
        accounts[4][0]: 50,
        accounts[5][0]: 60,
        accounts[6][0]: 70,  # team3 members
        accounts[7][0]: 80,
        accounts[8][0]: 90
    }
    
    # Save to files
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(data_dir, 'teams.json'), 'w') as f:
        json.dump(teams, f, indent=4)
    
    with open(os.path.join(data_dir, 'player_levels.json'), 'w') as f:
        json.dump(levels, f, indent=4)
    
    # Print mnemonics for testing
    print("\nTest Account Mnemonics:")
    for i, (_, mnemonic) in enumerate(accounts):
        print(f"\nAccount {i+1}:")
        print(mnemonic)

if __name__ == "__main__":
    generate_test_data() 