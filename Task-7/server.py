from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def load_json_file(filename):
    """Load and return JSON data from a file with error handling."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'data', filename)
        logger.info(f"Loading data from {file_path}")
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {filename}")
        return None
    except Exception as e:
        logger.error(f"Error loading {filename}: {str(e)}")
        return None

@app.route('/create_nft', methods=['POST'])
def create_nft():
    try:
        subprocess.run(['.venv\Scripts\python.exe', './scripts/create_nft.py'])
        return jsonify({"message": "NFT Created"})
    except Exception as e:
        logger.error(f"Error creating NFT: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/check_whitelist/<team_id>', methods=['GET'])
def check_whitelist(team_id):
    try:
        level_data = load_json_file('player_levels.json')
        teams = load_json_file('teams.json')
        
        if not level_data or not teams:
            return jsonify({"error": "Failed to load required data"}), 500
            
        members = teams.get(team_id)
        if not members:
            return jsonify({"message": "Team not found"})
            
        try:
            from smart_contracts.whitelist_logic import is_whitelisted
        except ImportError as e:
            logger.error(f"Import Error: {e}")
            logger.error(f"Current directory: {os.getcwd()}")
            logger.error(f"Python path: {sys.path}")
            return jsonify({"error": "Failed to import whitelist logic"}), 500
            
        eligible = is_whitelisted(members, level_data)
        return jsonify({"message": "Eligible" if eligible else "Not eligible"})
    except Exception as e:
        logger.error(f"Error in check_whitelist: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/buy_nft', methods=['POST'])
def buy_nft():
    try:
        # Validate request data
        data = request.get_json()
        logger.info(f"Received buy_nft request with data: {data}")
        
        if not data or 'mnemonics' not in data or len(data['mnemonics']) != 2:
            return jsonify({"error": "Invalid request data. Expected 2 mnemonics."}), 400

        m1, m2 = data['mnemonics'][0], data['mnemonics'][1]

        # Validate mnemonics format
        try:
            from algosdk import mnemonic
            mnemonic.to_private_key(m1)
            mnemonic.to_private_key(m2)
        except Exception as e:
            logger.error(f"Invalid mnemonic format: {str(e)}")
            return jsonify({"error": "Invalid mnemonic format"}), 400

        # Create a temporary script with the mnemonics
        script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        script_path = os.path.join(script_dir, 'tmp_buy.py')
        source_script = os.path.join(script_dir, 'simulate_multisig_buy.py')

        logger.info(f"Reading source script from: {source_script}")
        with open(source_script, 'r', encoding='utf-8') as f:
            code = f.read()

        # Replace the mnemonics in the code
        code = code.replace('mnemonic1 = "mnemonic1"', f'mnemonic1 = "{m1}"')
        code = code.replace('mnemonic2 = "mnemonic2"', f'mnemonic2 = "{m2}"')

        logger.info(f"Writing temporary script to: {script_path}")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(code)

        try:
            # Run the script using the virtual environment's Python
            venv_python = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'python.exe')
            logger.info(f"Running script with Python: {venv_python}")
            
            # Set PYTHONIOENCODING to ensure proper encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            result = subprocess.run(
                [venv_python, script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env,
                check=True
            )
            
            logger.info(f"Script output: {result.stdout}")
            
            # Clean up the temporary file
            if os.path.exists(script_path):
                os.remove(script_path)
                logger.info("Temporary script file cleaned up")
            
            return jsonify({
                "message": "NFT bought with multisig!",
                "details": result.stdout.strip()
            })
        except subprocess.CalledProcessError as e:
            logger.error(f"Script execution failed: {e.stderr}")
            return jsonify({
                "message": "Failed to execute NFT purchase, make sure your team signed for the same",
                "details": e.stderr.strip()
            }), 200
        finally:
            # Ensure temporary file is cleaned up even if there's an error
            if os.path.exists(script_path):
                os.remove(script_path)
                logger.info("Temporary script file cleaned up in finally block")

    except Exception as e:
        logger.error(f"Error in buy_nft: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
