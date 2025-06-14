# AlgoThon - Algorand Hackathon Project

Welcome to the AlgoThon project! This repository contains various tasks and projects related to Algorand blockchain development, including a Tic-Tac-Toe game and an NFT marketplace with team-based mechanics.

NFTs and gaming have been highly for degen community. NFTs have become a way to show your gaming status. Introducing an NFT marketplace dedicated to gamers. Here, team can NFT all together, based on their level. For example : we can have a particular avatar not unlocked until a particular average level is reached by the team.

The transaction can't be done with a single team member. It need to be signed by multiple members. Also, we exploring the integration of dynamic NFT with the average increase in level of the team (would need to think out the way for this)
## 🏗️ Project Structures

```
AlgoThon/
├── Task-1/                    # Task 1: Basic ASA Token Creation
│   └── projects/
│       └── HackToken/
│           └── scripts/
│               ├── create_asset.py
│               ├── check_balance.py
│               └── generate_mnemonic.py
│
├── Task-2/                    # Task 2: Advanced Asset Controls & Metadata
│   └── projects/
│       └── HackToken/
│           └── scripts/
│               └── configure_asset.py
│
├── Task-7/                    # Task 7: NFT Marketplace with Team Mechanics
│   ├── algokit_project/       # Algorand smart contracts
│   ├── data/                  # Player and team data
│   ├── frontend/              # Web interface
│   ├── scripts/               # Utility scripts
│   ├── smart_contracts/       # Smart contract code
│   ├── tests/                 # Test cases
│   └── utils/                 # Helper utilities
│
└── tictactoe/                # Real-time Tic-Tac-Toe Game
    ├── static/               # Frontend assets
    │   ├── script.js
    │   └── style.css
    └── templates/            # HTML templates
        └── index.html
```

## 🚀 Featured Projects

### 🎮 Tic-Tac-Toe Game
A real-time multiplayer Tic-Tac-Toe game built with Flask and Socket.IO.

**Features:**
- Real-time gameplay with WebSockets
- Score tracking
- Multiple game rooms
- Player matching system

**How to run:**
```bash
cd tictactoe
pip install -r requirements.txt
python server.py
```
Then open `http://localhost:5000` in your browser.

### 🖼️ Task 7: NFT Marketplace with Team Mechanics
A comprehensive NFT marketplace with team-based mechanics and whitelisting functionality.

**Features:**
- Multi-signature NFT purchases
- Team-based whitelisting
- Player leveling system
- Frontend interface for interaction

**How to run:**
```bash
cd Task-7
python -m venv venv7
source venv7/bin/activate  # On Windows: venv7\Scripts\activate
pip install -r requirements.txt
python server.py
```

## 📋 All Tasks

### 1. Task 1: Basic ASA Token
- Created a custom token on Algorand TestNet
- Implemented scripts for token creation and management
- [View Task 1 Details](Task-1/README.md)

### 2. Task 2: Advanced Asset Controls & Metadata
- Added ARC-53 compliant metadata (IPFS, description, MIME type)
- Implemented asset roles (Manager, Reserve, Freeze, Clawback)
- Added freeze and clawback functionality
- [View Task 2 Details](Task-2/README.md)

### 3. Task 7: NFT Marketplace with Team Mechanics (Featured Above)
- Multi-signature NFT purchases
- Team-based whitelisting
- Player leveling system
- [View Task 7 Details](Task-7/README.md)

## ⚙️ Prerequisites

- Python 3.8+
- Node.js (for frontend development)
- Algorand SDK (`pip install py-algorand-sdk`)
- A funded Algorand TestNet account (get ALGOs from the [TestNet Dispenser](https://bank.testnet.algorand.network/))
- Python-dotenv (`pip install python-dotenv`)
- Flask (`pip install flask`)
- Flask-SocketIO (`pip install flask-socketio`)

## 🔧 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Navinco/Algothon.git
   cd Algothon
   ```

2. Navigate to the task directory and install dependencies:
   ```bash
   cd Task-1  # or Task-2
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` to `.env` and add your mnemonic phrase

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
