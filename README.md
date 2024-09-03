# Connect Four Game

This is a Python implementation of the classic Connect Four game. The game can be played between two players, where each player can either be a human, a random AI, or an advanced AI that uses a tiebreak strategy and lookahead depth to make decisions.

## Table of Contents

- Installation
- How to Play
- Player Types
- AI Strategies
- Usage
- Example
- License

## Installation

To run the Connect Four game, ensure you have Python installed on your system. You can clone this repository or download the script directly.

How to Play
The game is played on a board with 6 rows and 7 columns. Players take turns dropping their checkers into one of the columns. The first player to align four of their checkers horizontally, vertically, or diagonally wins the game.

Player Types
You can choose different types of players when starting the game:

Human Player: You manually input the column number where you want to drop your checker.
Random AI Player: The computer randomly selects a column to drop its checker.
AI Player: An advanced AI that makes decisions based on a tiebreak strategy and lookahead depth.
AI Strategies
When selecting the AI player, you can configure the following:

Tiebreak Strategy:

LEFT: In case of a tie in scores, the AI chooses the leftmost column.
RIGHT: In case of a tie, the AI chooses the rightmost column.
RANDOM: In case of a tie, the AI randomly selects among the tied columns.
Lookahead Depth: The AI can look ahead a certain number of moves to evaluate potential outcomes and make more informed decisions.

Usage
To start the game, simply run the connect_four.py script:

bash
Copy code
python connect_four.py
You will be prompted to choose the player types for Player X and Player O. Follow the on-screen instructions to play the game.

Example
Here’s a sample of what the game looks like when playing:

plaintext
Copy code
Connect Four
Choose player types:
1: Human
2: Random
3: AI

Choose type for Player X: 1
Choose type for Player O: 3
Choose tiebreak strategy for AI O (LEFT, RIGHT, RANDOM): LEFT
Choose lookahead depth for AI O: 2
The game will then proceed with Player X as a human and Player O as an AI with a LEFT tiebreak strategy and a lookahead depth of 2.
