 // Initialize variables
let socket;
let playerSymbol;
let playerName;
let gameBoard = ['', '', '', '', '', '', '', '', ''];
let isGameActive = false;
let scores = { X: 0, O: 0 };
let currentRoom = '';

// Initialize the game
function init() {
    const form = document.getElementById('setup-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const room = document.getElementById('room').value.trim();
        playerName = document.getElementById('player-name').value.trim();
        if (room && playerName) {
            connectToGame(room);
        }
    });
}

// Connect to the game server
function connectToGame(room) {
    currentRoom = room;
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to server');
        document.getElementById('setup-screen').style.display = 'none';
        document.getElementById('waiting-screen').style.display = 'block';
        socket.emit('join', { room: room, player_name: playerName });
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        showMessage('Disconnected from server', 'error');
    });

    socket.on('waiting_for_player', () => {
        document.getElementById('waiting-screen').style.display = 'block';
        document.getElementById('game-screen').style.display = 'none';
    });

    socket.on('waitlist', (data) => {
        document.getElementById('waiting-screen').style.display = 'block';
        document.getElementById('game-screen').style.display = 'none';
        showMessage(`You are in position ${data.position} in the waitlist`, 'info');
    });

    socket.on('game_start', (data) => {
        playerSymbol = data.symbol;
        document.getElementById('waiting-screen').style.display = 'none';
        document.getElementById('game-screen').style.display = 'block';
        document.getElementById('player-symbol').textContent = playerSymbol;
        document.getElementById('player-symbol').className = `player-symbol ${playerSymbol.toLowerCase()}`;
        isGameActive = true;
        updateBoard();
        showMessage(`Game started! You are player ${playerSymbol}`, 'info');
    });

    socket.on('game_state', (data) => {
        gameBoard = data.board;
        updateBoard();
        document.getElementById('current-player').textContent = data.current_player;
        document.getElementById('current-player').className = `current-player ${data.current_player.toLowerCase()}`;
        
        // Update game info and enable/disable cells based on turn
        const gameInfo = document.getElementById('game-info');
        if (data.current_player === playerSymbol) {
            gameInfo.textContent = "It's your turn!";
            gameInfo.className = 'your-turn';
            enableCells();
        } else {
            gameInfo.textContent = "Opponent's turn";
            gameInfo.className = 'opponent-turn';
            disableCells();
        }
    });

    socket.on('game_over', (data) => {
        isGameActive = false;
        updateScoreboard(data.scores);
        disableCells();
        
        if (data.winner) {
            const winningCombination = data.winning_combination;
            if (winningCombination) {
                // Animate winning combination
                winningCombination.forEach(index => {
                    const cell = document.querySelector(`[data-index="${index}"]`);
                    cell.classList.add('winning-cell');
                });
                
                // Show winner message
                const message = data.winner === playerSymbol ? 'You won!' : 'Opponent won!';
                showMessage(message, 'success');
                console.log(data.winner, data)
                
                // Reset board after animation
                setTimeout(() => {
                    winningCombination.forEach(index => {
                        const cell = document.querySelector(`[data-index="${index}"]`);
                        cell.classList.remove('winning-cell');
                    });
                }, 2000);
            }
        } else {
            // Animate tie game
            const cells = document.querySelectorAll('.cell');
            cells.forEach(cell => {
                cell.classList.add('tie-cell');
            });
            
            showMessage("It's a tie!", 'info');
            
            // Reset board after animation
            setTimeout(() => {
                cells.forEach(cell => {
                    cell.classList.remove('tie-cell');
                });
            }, 2000);
        }
    });

    socket.on('opponent_disconnected', () => {
        showMessage('Opponent disconnected', 'error');
        document.getElementById('game-screen').style.display = 'none';
        document.getElementById('waiting-screen').style.display = 'block';
    });

    socket.on('error', (data) => {
        showMessage(data.message, 'error');
    });
}

// Update the game board
function updateBoard() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        cell.textContent = gameBoard[index];
        cell.className = 'cell';
        if (gameBoard[index] === 'X') {
            cell.classList.add('x-cell');
        } else if (gameBoard[index] === 'O') {
            cell.classList.add('o-cell');
        }
    });
}

// Enable cells for current player
function enableCells() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        if (gameBoard[index] === '') {
            cell.onclick = () => makeMove(index);
            cell.style.cursor = 'pointer';
        }
    });
}

// Disable all cells
function disableCells() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.onclick = null;
        cell.style.cursor = 'not-allowed';
    });
}

// Update the scoreboard
function updateScoreboard(scores) {
    document.getElementById('score-x').textContent = scores.X;
    document.getElementById('score-o').textContent = scores.O;
}

// Handle player moves
function makeMove(index) {
    if (isGameActive && gameBoard[index] === '') {
        socket.emit('make_move', { room: currentRoom, index: index });
    }
}

// Show messages to the user
function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 3000);
}

// Leave the current room
function leaveRoom() {
    if (socket) {
        socket.disconnect();
    }
    document.getElementById('game-screen').style.display = 'none';
    document.getElementById('waiting-screen').style.display = 'none';
    document.getElementById('setup-screen').style.display = 'block';
    document.getElementById('room').value = '';
    document.getElementById('player-name').value = '';
    gameBoard = ['', '', '', '', '', '', '', '', ''];
    isGameActive = false;
    scores = { X: 0, O: 0 };
    currentRoom = '';
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', init);