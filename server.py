from flask import Flask, request, jsonify
from Flask_cors import CORS 
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("CONNECTION_STRING")

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_URI)
db = client["tic_tac_toe"]
games = db["games"]

@app.route("/create_game", methods=["POST"])
def create_game():
    data = request.json
    session_id = data["session_id"]
    
    if games.find_one({"_id": session_id}):
        return jsonify({"error": "Session ID already exists"}), 400
    
    game_data = {
        "_id": session_id,
        "playerX": data["playerX"],
        "playerO": None,
        "board": ["", "", "", "", "", "", "", "", ""],
        "turn": "X",
        "winner": None,
        "status": "waiting"
    }
    games.insert_one(game_data)
    return jsonify({"message": "Game created", "session_id": session_id})

@app.route("/join_game", methods=["POST"])
def join_game():
    data = request.json
    session_id = data["session_id"]
    
    game = games.find_one({"_id": session_id})
    if not game:
        return jsonify({"error": "Session not found"}), 404
    
    if game["playerO"]:
        return jsonify({"error": "Game already full"}), 400
    
    games.update_one({"_id": session_id}, {"$set": {"playerO": data["playerO"], "status": "ongoing"}})
    return jsonify({"message": "Joined game", "session_id": session_id})

@app.route("/make_move", methods=["POST"])
def make_move():
    data = request.json
    session_id = data["session_id"]
    position = data["position"]
    player = data["player"]
    
    game = games.find_one({"_id": session_id})
    if not game:
        return jsonify({"error": "Session not found"}), 404

    if game["turn"] != player:
        return jsonify({"error": "Not your turn"}), 400
    
    if game["board"][position] != "":
        return jsonify({"error": "Invalid move"}), 400
    
    game["board"][position] = player
    game["turn"] = "O" if player == "X" else "X"
    
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if game["board"][combo[0]] == game["board"][combo[1]] == game["board"][combo[2]] and game["board"][combo[0]] != "":
            game["winner"] = game["board"][combo[0]]
            game["status"] = "finished"
            break
    
    games.update_one({"_id": session_id}, {"$set": game})
    return jsonify({"message": "Move registered", "board": game["board"], "turn": game["turn"], "winner": game["winner"]})

@app.route("/get_game/<session_id>", methods=["GET"])
def get_game(session_id):
    game = games.find_one({"_id": session_id}, {"_id": 0})
    if not game:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(game)

if __name__ == "__main__":
    app.run(debug=True)
