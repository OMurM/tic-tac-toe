import tkinter as tk
import requests

# Flask API URL (assuming the Flask API is running on localhost:5000)
API_URL = "http://localhost:5000"

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TicTacToe")
        self.board = [None] * 9  # Holds the game state (board)
        self.current_player = "X"
        self.game_id = None  # Will store the game ID
        
        # Create buttons for the TicTacToe grid
        self.buttons = [tk.Button(self.root, text=" ", font=("Arial", 24), width=10, height=3, command=lambda i=i: self.make_move(i)) for i in range(9)]
        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row=row, column=col)
        
        # Create Start Button
        self.start_button = tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=3)

    def start_game(self):
        """Start a new game by calling the Flask API."""
        response = requests.post(f"{API_URL}/start_game")
        if response.status_code == 200:
            data = response.json()
            self.game_id = data["game_id"]
            self.reset_board()

    def reset_board(self):
        """Reset the board for a new game."""
        for i in range(9):
            self.board[i] = " "
            self.buttons[i].config(text=" ")
        self.current_player = "X"

    def make_move(self, index):
        """Make a move by clicking a button."""
        if self.board[index] == " " and self.game_id:
            # Call the API to make the move
            response = requests.post(f"{API_URL}/make_move/{self.game_id}", json={"position": index})
            if response.status_code == 200:
                data = response.json()
                self.board = data["game_state"]["board"]
                self.update_board()
                self.current_player = "O" if self.current_player == "X" else "X"

    def update_board(self):
        """Update the board with the latest game state."""
        for i in range(9):
            self.buttons[i].config(text=self.board[i])

def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
