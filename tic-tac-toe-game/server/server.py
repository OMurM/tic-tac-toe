from flask import Flask, request, jsonify
import uuid
import threading
import tkinter as tk
from tkinter import scrolledtext

# Create Flask app
app = Flask(__name__)

# Game storage - simple dictionary
games = {}

# Create a new game
@app.route('/new', methods=['POST'])
def new_game():
    game_id = str(uuid.uuid4())[:8]  # Short ID for simplicity
    games[game_id] = {
        'board': [None] * 9,
        'turn': 'X',
        'winner': None,
        'players': {'X': None, 'O': None}
    }
    
    # Set player name
    data = request.json
    player_symbol = data.get('symbol', 'X')
    player_name = data.get('name', 'Player X')
    games[game_id]['players'][player_symbol] = player_name
    
    print(f"New game created: {game_id}")
    return jsonify({'game_id': game_id})

# Join existing game
@app.route('/join/<game_id>', methods=['POST'])
def join_game(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    player_name = data.get('name', 'Player O')
    games[game_id]['players']['O'] = player_name
    
    print(f"Player {player_name} joined game {game_id}")
    return jsonify({'status': 'joined'})

# Get game state
@app.route('/game/<game_id>', methods=['GET'])
def get_game(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    return jsonify(games[game_id])

# Make a move
@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    game_id = data.get('game_id')
    position = data.get('position')
    symbol = data.get('symbol')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    # Check if move is valid
    if (game['turn'] != symbol or 
            position < 0 or position > 8 or 
            game['board'][position] is not None or 
            game['winner']):
        return jsonify({'error': 'Invalid move'}), 400
    
    # Make the move
    game['board'][position] = symbol
    
    # Check for winner
    game['winner'] = check_winner(game['board'])
    
    # Switch turns if no winner
    if not game['winner']:
        game['turn'] = 'O' if symbol == 'X' else 'X'
    
    print(f"Move in game {game_id}: {symbol} at position {position}")
    return jsonify(game)

def check_winner(board):
    # Winning patterns
    patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    # Check for a winner
    for pattern in patterns:
        if (board[pattern[0]] is not None and
                board[pattern[0]] == board[pattern[1]] == board[pattern[2]]):
            return board[pattern[0]]
    
    # Check for draw
    if None not in board:
        return 'Draw'
    
    return None

# GUI for server monitoring
def start_gui():
    root = tk.Tk()
    root.title("Tic Tac Toe Server")
    root.geometry("400x300")
    
    # Log area
    log = scrolledtext.ScrolledText(root)
    log.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Games list
    games_label = tk.Label(root, text="Active Games:")
    games_label.pack(anchor="w", padx=10)
    
    games_list = tk.Listbox(root, height=5)
    games_list.pack(fill="x", padx=10, pady=(0, 10))
    
    # Update function
    def update_ui():
        games_list.delete(0, tk.END)
        for id, game in games.items():
            status = f"Winner: {game['winner']}" if game['winner'] else f"Turn: {game['turn']}"
            games_list.insert(tk.END, f"{id} - {status}")
        root.after(1000, update_ui)
    
    # Start updates
    update_ui()
    
    # Override print function to log to GUI
    old_print = print
    def new_print(*args, **kwargs):
        old_print(*args, **kwargs)
        message = " ".join(str(arg) for arg in args)
        log.insert(tk.END, message + "\n")
        log.see(tk.END)
    
    # Replace print function
    import builtins
    builtins.print = new_print
    
    print("Server started")
    root.mainloop()

# Start server
if __name__ == '__main__':
    # Start GUI in a thread
    threading.Thread(target=start_gui, daemon=True).start()
    
    # Start Flask
    print("Starting server on http://localhost:5000")
    app.run(debug=False)