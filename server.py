from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
from game_logic import TicTacToe
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB connection string from environment variable
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.get_database()

# MongoDB collection for storing game states
games_collection = db.games

@app.route('/')
def home():
    return jsonify(message="Welcome to the TicTacToe API!")

@app.route('/start_game', methods=["POST"])
def start_game():
    """Starts a new game."""
    game = TicTacToe()
    # Store the initial game state in MongoDB
    game_data = {
        "board": game.get_board(),
        "current_player": game.get_current_player()
    }
    result = games_collection.insert_one(game_data)
    return jsonify(message="New game started", game_id=str(result.inserted_id))

@app.route('/game/<game_id>', methods=["GET"])
def get_game_state(game_id):
    """Fetches the current state of a game from the database."""
    game = games_collection.find_one({"_id": game_id})
    if game:
        return dumps(game)
    else:
        return jsonify(message="Game not found"), 404

@app.route('/make_move/<game_id>', methods=["POST"])
def make_move(game_id):
    """Makes a move in the game and updates the game state."""
    position = request.json.get("position")
    game_data = games_collection.find_one({"_id": game_id})

    if not game_data:
        return jsonify(message="Game not found"), 404

    # Initialize the TicTacToe object with the current board and player
    game = TicTacToe()
    game.board = game_data["board"]
    game.current_player = game_data["current_player"]

    # Make the move
    if game.make_move(position):
        # Switch player
        game.switch_player()
        winner = game.check_winner()
        if winner:
            game_data["winner"] = winner
        # Update game state in MongoDB
        game_data["board"] = game.get_board()
        game_data["current_player"] = game.get_current_player()
        games_collection.update_one({"_id": game_id}, {"$set": game_data})

        return jsonify(message="Move made", game_state=game_data)
    else:
        return jsonify(message="Invalid move"), 400

@app.route('/reset_game/<game_id>', methods=["POST"])
def reset_game(game_id):
    """Resets the game to its initial state."""
    game_data = games_collection.find_one({"_id": game_id})
    if not game_data:
        return jsonify(message="Game not found"), 404

    # Reset the game
    game = TicTacToe()
    game_data["board"] = game.get_board()
    game_data["current_player"] = game.get_current_player()
    game_data["winner"] = None  # Reset winner
    games_collection.update_one({"_id": game_id}, {"$set": game_data})

    return jsonify(message="Game reset", game_state=game_data)

if __name__ == "__main__":
    app.run(debug=True)
