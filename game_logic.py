class TicTacToe:
    def __init__(self):
        # Initialize an empty game board
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def get_board(self):
        """Returns the current state of the board."""
        return self.board

    def get_current_player(self):
        """Returns the current player."""
        return self.current_player

    def make_move(self, position):
        """Makes a move on the board."""
        if self.board[position] == " ":
            self.board[position] = self.current_player
            return True
        return False

    def switch_player(self):
        """Switches the player after a move."""
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Checks if there is a winner."""
        # Winning combinations
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                return self.board[combo[0]]  # Return the winner (X or O)
        
        # Check for a draw
        if " " not in self.board:
            return "Draw"
        
        return None  # No winner yet
