from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import threading
import tkinter as tk
from tkinter import simpledialog
import requests
import uuid

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://admin:<db_password>@cluster0.ik5c5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.tic_tac_toe

# Initialize game state
def initialize_game(player_x):
    session_id = str(uuid.uuid4())
    game_state = {
        "session_id": session_id,
        "board": [""] * 9,
        "playerX": player_x,
        "playerO": None,
        "turn": "X",
        "winner": None
    }
    db.games.insert_one(game_state)
    return game_state

# Check for a winner
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]]
    return None

@app.route("/create_game", methods=["POST"])
def create_game():
    data = request.json
    player_x = data["playerX"]
    game_state = initialize_game(player_x)
    return jsonify(game_state)

@app.route("/make_move", methods=["POST"])
def make_move():
    data = request.json
    session_id = data["session_id"]
    player = data["player"]
    position = data["position"]

    game_state = db.games.find_one({"session_id": session_id})
    if game_state["board"][position] == "" and game_state["turn"] == player:
        game_state["board"][position] = player
        game_state["turn"] = "O" if player == "X" else "X"
        game_state["winner"] = check_winner(game_state["board"])
        db.games.update_one({"session_id": session_id}, {"$set": game_state})
    return jsonify(game_state)

@app.route("/game_state/<session_id>", methods=["GET"])
def game_state(session_id):
    game_state = db.games.find_one({"session_id": session_id})
    return jsonify(game_state)

def run_server():
    app.run(debug=True)

def start_server_gui():
    root = tk.Tk()
    root.title("Tic Tac Toe Server")

    def create_game():
        player_x = simpledialog.askstring("Player X Name", "Enter Player X Name:")
        response = requests.post("http://localhost:5000/create_game", json={"playerX": player_x})
        game_state = response.json()
        session_id = game_state["session_id"]
        tk.Label(root, text=f"Game created with Session ID: {session_id}").pack()

    tk.Button(root, text="Create Game", command=create_game).pack()
    root.mainloop()

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    start_server_gui()