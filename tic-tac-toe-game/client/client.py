import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
import os

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:5000")

class TicTacToeClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe Client")
        self.session_id = None
        self.player = "O"
        self.board = [""] * 9
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            button = tk.Button(self.root, text="", width=10, height=3, command=lambda i=i: self.make_move(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)
        self.session_id = simpledialog.askstring("Session ID", "Enter Session ID:")
        self.update_board()

    def make_move(self, position):
        response = requests.post(f"{SERVER_URL}/make_move", json={"session_id": self.session_id, "player": self.player, "position": position})
        game_state = response.json()
        self.update_board(game_state)

    def update_board(self, game_state=None):
        if game_state is None:
            response = requests.get(f"{SERVER_URL}/game_state/{self.session_id}")
            game_state = response.json()
        self.board = game_state["board"]
        for i in range(9):
            self.buttons[i].config(text=self.board[i])
        if game_state["winner"]:
            messagebox.showinfo("Game Over", f"Player {game_state['winner']} wins!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeClient(root)
    root.mainloop()