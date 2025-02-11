import tkinter as tk
import requests

API_URL = "http://127.0.0.1:5000"

class TicTacToe:
    def __init__(self, root, session_id, player):
        self.root = root
        self.session_id = session_id
        self.player = player
        self.buttons = []
        self.create_board()
        self.update_board()

    def create_board(self):
        for i in range(9):
            btn = tk.Button(self.root, text="", font=("Arial", 20), width=5, height=2,
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

    def make_move(self, position):
        response = requests.post(f"{API_URL}/make_move", json={"session_id": self.session_id, "position": position, "player": self.player})
        if response.status_code == 200:
            self.update_board()

    def update_board(self):
        response = requests.get(f"{API_URL}/get_game/{self.session_id}")
        if response.status_code == 200:
            game_data = response.json()
            board = game_data["board"]
            for i, value in enumerate(board):
                self.buttons[i]["text"] = value
            if game_data["winner"]:
                tk.Label(self.root, text=f"Winner: {game_data['winner']}").grid(row=3, columnspan=3)

if __name__ == "__main__":
    session_id = input("Enter session ID: ")
    player = input("Enter X or O: ")

    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    app = TicTacToe(root, session_id, player)
    root.mainloop()
