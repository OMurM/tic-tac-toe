# Tic Tac Toe Game

This project is a simple implementation of a Tic Tac Toe game using Flask for the server and a Python client. The server manages the game lobby, handles game creation, and processes player moves, while the client allows players to join the game and make moves.

## Project Structure

```
tic-tac-toe-game
├── server
│   ├── server.py          
│   ├── requirements.txt   
│   └── .env               
├── client
│   ├── client.py          
│   ├── requirements.txt   
│   └── .env               
└── README.md
```

## Setup Instructions

### Server

1. Navigate to the `server` directory:
   ```
   cd server
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your MongoDB connection string in the `.env` file:
   ```
   CONNECTION_STRING=mongodb+srv://admin:<db_password>@cluster0.ik5c5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   ```

5. Run the server:
   ```
   python server.py
   ```

### Client

1. Navigate to the `client` directory:
   ```
   cd client
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the server URL in the `.env` file if needed.

5. Run the client:
   ```
   python client.py
   ```

## How to Play

1. Start the server first.
2. Run the client to join the game as player O.
3. Follow the prompts in the client to make your moves and interact with the game.

Enjoy playing Tic Tac Toe!