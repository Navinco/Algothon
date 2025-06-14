from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game states
games = {}
# Store waiting players
waiting_players = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    # Clean up any rooms the player was in
    for room in games:
        if request.sid in games[room]['players']:
            handle_player_disconnect(room)

@socketio.on('join')
def on_join(data):
    room = data['room']
    player_name = data['player_name']

    if room not in games:
        # Create new game
        games[room] = {
            'board': ['', '', '', '', '', '', '', '', ''],
            'current_player': 'X',
            'players': {request.sid: {'symbol': 'X', 'name': player_name}},
            'scores': {'X': 0, 'O': 0},
            'waitlist': []
        }
        join_room(room)
        emit('waiting_for_player', room=room)
    elif len(games[room]['players']) < 2:
        # Join existing game
        symbol = 'O' if 'X' in [p['symbol'] for p in games[room]['players'].values()] else 'X'
        games[room]['players'][request.sid] = {'symbol': symbol, 'name': player_name}
        join_room(room)
        
        if len(games[room]['players']) == 2:
            # Start game
            for sid, player_info in games[room]['players'].items():
                emit('game_start', {'symbol': player_info['symbol']}, to=sid)
            
            emit('game_state', {
                'board': games[room]['board'],
                'current_player': games[room]['current_player'],
                'scores': games[room]['scores']
            }, room=room)
    else:
        # Room is full, add to waitlist
        if room not in waiting_players:
            waiting_players[room] = []
        waiting_players[room].append({'sid': request.sid, 'name': player_name})
        join_room(room)
        emit('waitlist', {'position': len(waiting_players[room])}, room=room)

def handle_player_disconnect(room):
    if room in games:
        if request.sid in games[room]['players']:
            # Notify other player
            emit('opponent_disconnected', room=room)
            # Clean up game
            del games[room]
            # Check waitlist
            if room in waiting_players and waiting_players[room]:
                next_player = waiting_players[room].pop(0)
                emit('game_start', {'symbol': 'X'}, room=room, to=next_player['sid'])

@socketio.on('make_move')
def on_move(data):
    room = data['room']
    index = data['index']
    
    if room in games and request.sid in games[room]['players']:
        player = games[room]['players'][request.sid]
        if player['symbol'] == games[room]['current_player'] and games[room]['board'][index] == '':
            # Make move
            games[room]['board'][index] = player['symbol']
            
            # Check for winner
            winner = check_winner(games[room]['board'])
            if winner:
                games[room]['scores'][winner] += 1
                emit('game_over', {
                    'winner': winner,
                    'scores': games[room]['scores'],
                    'winning_combination': get_winning_combination(games[room]['board'])
                }, room=room)
                # Reset board for next game
                games[room]['board'] = ['', '', '', '', '', '', '', '', '']
                games[room]['current_player'] = 'X'

                # players = games[room]['players']
                # for _, player_data in players.values():
                    

            elif '' not in games[room]['board']:
                # Tie game
                emit('game_over', {
                    'winner': None,
                    'scores': games[room]['scores']
                }, room=room)
                # Reset board for next game
                games[room]['board'] = ['', '', '', '', '', '', '', '', '']
                games[room]['current_player'] = 'X'
            else:
                # Switch turns
                games[room]['current_player'] = 'O' if games[room]['current_player'] == 'X' else 'X'
            
            # Update game state
            emit('game_state', {
                'board': games[room]['board'],
                'current_player': games[room]['current_player'],
                'scores': games[room]['scores']
            }, room=room)

def check_winner(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] and board[i] == board[i + 1] == board[i + 2]:
            return board[i]
    
    # Check columns
    for i in range(3):
        if board[i] and board[i] == board[i + 3] == board[i + 6]:
            return board[i]
    
    # Check diagonals
    if board[0] and board[0] == board[4] == board[8]:
        return board[0]
    if board[2] and board[2] == board[4] == board[6]:
        return board[2]
    
    return None

def get_winning_combination(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] and board[i] == board[i + 1] == board[i + 2]:
            return [i, i + 1, i + 2]
    
    # Check columns
    for i in range(3):
        if board[i] and board[i] == board[i + 3] == board[i + 6]:
            return [i, i + 3, i + 6]
    
    # Check diagonals
    if board[0] and board[0] == board[4] == board[8]:
        return [0, 4, 8]
    if board[2] and board[2] == board[4] == board[6]:
        return [2, 4, 6]
    
    return None

if __name__ == '__main__':
    socketio.run(app, debug=True)