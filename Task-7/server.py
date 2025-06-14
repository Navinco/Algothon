from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/create_nft', methods=['POST'])
def create_nft():
    subprocess.run(['.venv\Scripts\python.exe', './scripts/create_nft.py'])
    return jsonify({"message": "NFT Created"})

@app.route('/check_whitelist/<team_id>', methods=['GET'])
def check_whitelist(team_id):
    with open('data/player_levels.json') as f:
        level_data = json.load(f)
    with open('data/teams.json') as f:
        teams = json.load(f)
    try:
        from smart_contracts.whitelist_logic import is_whitelisted
    except ImportError as e:
        print(f"Import Error: {e}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        raise
    members = teams.get(team_id)
    if not members:
        return jsonify({"message": "Team not found"})
    eligible = is_whitelisted(members, level_data)
    return jsonify({"message": "Eligible" if eligible else "Not eligible"})

@app.route('/buy_nft', methods=['POST'])
def buy_nft():
    data = request.get_json()
    m1, m2 = data['mnemonics'][0], data['mnemonics'][1]
    with open("scripts/simulate_multisig_buy.py", "r") as f:
        code = f.read().replace("mnemonic1", f'"{m1}"').replace("mnemonic2", f'"{m2}"')
    with open("scripts/tmp_buy.py", "w") as f:
        f.write(code)
    #subprocess.run(["python3", "scripts/tmp_buy.py"])
    subprocess.run([r"venv\Scripts\python.exe", "scripts/create_nft.py"])

    return jsonify({"message": "NFT bought with multisig!"})

if __name__ == '__main__':
    app.run(debug=True)
