import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
import threading
import time

# Server URL
SERVER_URL = "http://localhost:5000"

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        
        # Game state
        self.game_id = None
        self.player_symbol = None
        self.game_active = False
        
        # Create UI
        self.create_start_screen()
    
    def create_start_screen(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        # Title
        tk.Label(frame, text="Tic Tac Toe", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Buttons
        tk.Button(frame, text="Create New Game", 
                 command=self.create_game, width=20, height=2).pack(pady=5)
        
        tk.Button(frame, text="Join Game", 
                 command=self.join_game, width=20, height=2).pack(pady=5)
    
    def create_game(self):
        # Get player name
        name = simpledialog.askstring("Name", "Enter your name:", parent=self.root)
        if not name:
            return
        
        try:
            # Create game on server
            response = requests.post(f"{SERVER_URL}/new", 
                                   json={"name": name, "symbol": "X"})
            
            if response.status_code == 200:
                data = response.json()
                self.game_id = data["game_id"]
                self.player_symbol = "X"
                
                # Show game ID
                messagebox.showinfo("Game Created", 
                                  f"Your game ID is: {self.game_id}\nShare this with the other player")
                
                # Start game UI
                self.create_game_board()
                self.game_active = True
                self.start_polling()
            else:
                messagebox.showerror("Error", "Failed to create game")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def join_game(self):
        # Get game ID and player name
        game_id = simpledialog.askstring("Game ID", "Enter the game ID:", parent=self.root)
        if not game_id:
            return
            
        name = simpledialog.askstring("Name", "Enter your name:", parent=self.root)
        if not name:
            return
        
        try:
            # Join game on server
            response = requests.post(f"{SERVER_URL}/join/{game_id}", 
                                   json={"name": name})
            
            if response.status_code == 200:
                self.game_id = game_id
                self.player_symbol = "O"
                
                # Start game UI
                self.create_game_board()
                self.game_active = True
                self.start_polling()
            else:
                messagebox.showerror("Error", "Failed to join game")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def create_game_board(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create game frame
        game_frame = tk.Frame(self.root, padx=20, pady=20)
        game_frame.pack(expand=True)
        
        # Status label
        self.status_label = tk.Label(game_frame, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Game board
        board_frame = tk.Frame(game_frame)
        board_frame.pack()
        
        # Create buttons for the board
        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_frame, text="", width=5, height=2, font=("Arial", 14, "bold"),
                          command=lambda pos=i: self.make_move(pos))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)
        
        # Game ID display
        tk.Label(game_frame, text=f"Game ID: {self.game_id}").pack(pady=(15, 5))
        tk.Label(game_frame, text=f"You are playing as {self.player_symbol}").pack()
    
    def make_move(self, position):
        try:
            response = requests.post(f"{SERVER_URL}/move", 
                                   json={
                                       "game_id": self.game_id,
                                       "position": position,
                                       "symbol": self.player_symbol
                                   })
            
            if response.status_code == 200:
                self.update_board(response.json())
            else:
                data = response.json()
                print(f"Move error: {data.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Connection error: {str(e)}")
    
    def start_polling(self):
        def poll_game_state():
            while self.game_active:
                try:
                    response = requests.get(f"{SERVER_URL}/game/{self.game_id}")
                    if response.status_code == 200:
                        self.root.after(0, lambda: self.update_board(response.json()))
                    time.sleep(1)
                except Exception:
                    time.sleep(2)  # Wait longer on error
        
        # Start polling in background
        threading.Thread(target=poll_game_state, daemon=True).start()
    
    def update_board(self, game_data):
        # Update buttons with current board state
        board = game_data["board"]
        for i, symbol in enumerate(board):
            text = symbol if symbol else ""
            self.buttons[i].config(text=text)
            
            # Disable filled cells
            if symbol:
                self.buttons[i].config(state="disabled")
        
        # Update game status
        winner = game_data.get("winner")
        if winner:
            self.game_active = False
            if winner == "Draw":
                self.status_label.config(text="Game ended in a draw!")
            elif winner == self.player_symbol:
                self.status_label.config(text="You win!")
            else:
                self.status_label.config(text="You lose!")
                
            # Disable all buttons
            for btn in self.buttons:
                btn.config(state="disabled")
        else:
            # Update turn information
            current_turn = game_data["turn"]
            if current_turn == self.player_symbol:
                self.status_label.config(text="Your turn")
                # Enable empty cells
                for i, symbol in enumerate(board):
                    if not symbol:
                        self.buttons[i].config(state="normal")
            else:
                self.status_label.config(text="Opponent's turn")
                # Disable all buttons while waiting
                for btn in self.buttons:
                    btn.config(state="disabled")

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("350x400")
    game = TicTacToeGame(root)
    root.mainloop()