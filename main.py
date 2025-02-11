import os
import threading
import time
import tkinter as tk
from pymongo import MongoClient, errors
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

# Connect to MongoDB Atlas
client = MongoClient(connection_string)

# Get the default database from the connection string.
# If the connection string does not include a default database,
# you can fall back to a specified name.
try:
    db = client.get_default_database()
    print("Using default database from connection string:", db.name)
except errors.ConfigurationError:
    # Fallback: explicitly specify a database name
    fallback_db_name = "test"
    print("No default database defined; using fallback:", fallback_db_name)
    db = client[fallback_db_name]

# Define the collection name for the game.
collection_name = "tic_tac_toe_OMM"

# Check if the collection exists; if not, explicitly create it.
if collection_name not in db.list_collection_names():
    try:
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created successfully.")
    except errors.CollectionInvalid as e:
        print(f"Error creating collection: {e}")
else:
    print(f"Collection '{collection_name}' already exists.")

# Get the collection
collection = db[collection_name]

# --- Game State ---
# Initialize an empty 3x3 board.
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'

# --- Function: Update the Board from the Database ---
def update_board_from_db():
    """
    Polls the MongoDB collection for moves and updates the local board and GUI.
    This function runs in a background thread.
    """
    while True:
        try:
            # Retrieve all moves sorted by insertion order
            moves = list(collection.find().sort("_id"))
            for move in moves:
                row = move.get("row")
                col = move.get("col")
                player = move.get("player")
                # Only update if the cell is still empty locally
                if board[row][col] == '':
                    board[row][col] = player
                    buttons[row][col].config(text=player)
            time.sleep(2)  # Poll every 2 seconds
        except Exception as e:
            print("Error while updating board:", e)
            time.sleep(2)

# --- Function: Handle a User Click ---
def handle_click(row, col):
    global current_player
    # Only register a move if the cell is empty
    if board[row][col] == '':
        board[row][col] = current_player
        buttons[row][col].config(text=current_player)
        # Record the move in the database
        move = {"row": row, "col": col, "player": current_player}
        try:
            collection.insert_one(move)
        except Exception as e:
            print("Error inserting move:", e)
        # Toggle the player (simple local turn switch)
        current_player = 'O' if current_player == 'X' else 'X'

# --- Setup the Tkinter GUI ---
root = tk.Tk()
root.title("Tic Tac Toe Multiplayer (Atlas)")

buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        btn = tk.Button(root, text='', width=10, height=4,
                        command=lambda r=i, c=j: handle_click(r, c))
        btn.grid(row=i, column=j)
        row_buttons.append(btn)
    buttons.append(row_buttons)

# --- Start the Background Thread for Database Polling ---
poll_thread = threading.Thread(target=update_board_from_db, daemon=True)
poll_thread.start()

# --- Run the Tkinter Main Loop ---
root.mainloop()
