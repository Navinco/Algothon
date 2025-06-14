from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import sys
import os
import logging
import traceback

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global error handler
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return jsonify({"error": "Internal server error"}), 500

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
        logger.debug("Starting buy_nft endpoint")
        # Validate request data
        data = request.get_json()
        logger.debug(f"Received request data: {data}")
        
        if not data:
            logger.error("No data received in request")
            return jsonify({"error": "No data received"}), 400
            
        if 'mnemonics' not in data:
            logger.error("No mnemonics in request data")
            return jsonify({"error": "No mnemonics provided"}), 400
            
        if len(data['mnemonics']) != 2:
            logger.error(f"Invalid number of mnemonics: {len(data['mnemonics'])}")
            return jsonify({"error": "Expected exactly 2 mnemonics"}), 400

        m1, m2 = data['mnemonics'][0], data['mnemonics'][1]
        logger.debug("Mnemonics received, validating format")

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

        logger.debug(f"Checking if source script exists: {source_script}")
        if not os.path.exists(source_script):
            logger.error(f"Source script not found: {source_script}")
            return jsonify({"error": "Required script file not found"}), 500

        logger.debug("Reading source script")
        try:
            with open(source_script, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            logger.error(f"Error reading source script: {str(e)}")
            return jsonify({"error": "Failed to read source script"}), 500

        # Replace the mnemonics in the code
        code = code.replace('mnemonic1 = "mnemonic1"', f'mnemonic1 = "{m1}"')
        code = code.replace('mnemonic2 = "mnemonic2"', f'mnemonic2 = "{m2}"')

        logger.debug(f"Writing temporary script to: {script_path}")
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(code)
        except Exception as e:
            logger.error(f"Error writing temporary script: {str(e)}")
            return jsonify({"error": "Failed to write temporary script"}), 500

        try:
            # Run the script using the virtual environment's Python
            venv_python = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'python.exe')
            logger.debug(f"Checking Python executable: {venv_python}")
            
            if not os.path.exists(venv_python):
                logger.error(f"Python executable not found at: {venv_python}")
                return jsonify({"error": "Python environment not properly configured"}), 500

            logger.debug("Setting up environment variables")
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            logger.debug("Running subprocess")
            result = subprocess.run(
                [venv_python, script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env,
                check=False  # Don't raise exception on non-zero exit
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip()
                logger.error(f"Script execution failed with error: {error_msg}")
                if "Invalid number of signatures" in error_msg:
                    return jsonify({
                        "error": "Transaction signing failed. Please ensure both mnemonics are correct and the accounts have sufficient funds."
                    }), 400
                elif "Network error" in error_msg:
                    return jsonify({
                        "error": "Failed to connect to Algorand network. Please try again later."
                    }), 503
                else:
                    return jsonify({
                        "error": f"Transaction failed: {error_msg}"
                    }), 400
            
            logger.debug(f"Script output: {result.stdout}")
            
            # Clean up the temporary file
            if os.path.exists(script_path):
                os.remove(script_path)
                logger.debug("Temporary script file cleaned up")
            
            return jsonify({
                "message": "NFT bought with multisig!",
                "details": result.stdout.strip()
            })
        except subprocess.CalledProcessError as e:
            logger.error(f"Script execution failed: {e.stderr}")
            return jsonify({
                "error": "Failed to execute NFT purchase. Please try again."
            }), 500
        finally:
            # Ensure temporary file is cleaned up even if there's an error
            if os.path.exists(script_path):
                os.remove(script_path)
                logger.debug("Temporary script file cleaned up in finally block")

    except Exception as e:
        logger.error(f"Unexpected error in buy_nft: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting Flask server...")
        app.run(debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
