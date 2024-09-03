import random

class Board:
    """A data type for a Connect Four board with arbitrary dimensions."""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.slots = [[' ']*self.width for _ in range(self.height)]

    def __repr__(self):
        """Returns a string that represents a Board object."""
        s = ''
        for row in range(self.height):
            s += '|' + '|'.join(self.slots[row]) + '|\n'
        s += '-' + '--' * self.width + '\n'
        s += ' ' + ' '.join(str(i % 10) for i in range(self.width))
        return s

    def add_checker(self, checker, col):
        """Adds the specified checker to the column with the specified index."""
        assert checker in 'XO'
        assert 0 <= col < self.width
        
        if not self.can_add_to(col):
            raise ValueError("Column is full or invalid")
        
        for row in reversed(range(self.height)):
            if self.slots[row][col] == ' ':
                self.slots[row][col] = checker
                return

    def reset(self):
        """Resets the board."""
        self.slots = [[' ']*self.width for _ in range(self.height)]

    def can_add_to(self, col):
        """Checks if a column is not full."""
        return 0 <= col < self.width and self.slots[0][col] == ' '

    def is_full(self):
        """Checks if the board is full."""
        return all(not self.can_add_to(col) for col in range(self.width))

    def remove_checker(self, col):
    # Validate column index
        if not (0 <= col < self.width):
            raise ValueError("Column index is out of bounds")
        
        # Find the highest checker in the column
        for row in range(self.height - 1, -1, -1):
            if self.slots[row][col] in 'XO':
                self.slots[row][col] = ' '
                return
        
        raise ValueError("Column is empty")

    def is_horizontal_win(self, checker):
        """Checks for a horizontal win."""
        for row in range(self.height):
            for col in range(self.width - 3):
                if all(self.slots[row][col + i] == checker for i in range(4)):
                    return True
        return False

    def is_vertical_win(self, checker):
        """Checks for a vertical win."""
        for row in range(self.height - 3):
            for col in range(self.width):
                if all(self.slots[row + i][col] == checker for i in range(4)):
                    return True
        return False

    def is_diagonal_down_win(self, checker):
        """Checks for a diagonal down win."""
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if all(self.slots[row + i][col + i] == checker for i in range(4)):
                    return True
        return False

    def is_diagonal_up_win(self, checker):
        """Checks for a diagonal up win."""
        for row in range(3, self.height):
            for col in range(self.width - 3):
                if all(self.slots[row - i][col + i] == checker for i in range(4)):
                    return True
        return False

    def is_win_for(self, checker):
        """Checks if there's a win for the specified checker."""
        return (self.is_horizontal_win(checker) or
                self.is_vertical_win(checker) or
                self.is_diagonal_down_win(checker) or
                self.is_diagonal_up_win(checker))


class Player:
    """ Represents a player in the Connect Four game. """
    
    def __init__(self, checker):
        """ Initializes player """
        assert checker in 'XO'
        self.checker = checker
        self.num_moves = 0
        
    def __repr__(self):
        """ Represents player as a string """
        return f"Player {self.checker}"
   
    def opponent_checker(self):
        """ Returns the opponent's checker """
        return 'O' if self.checker == 'X' else 'X'
    
    def next_move(self, b):
        """ Puts the checker in the place the user wants """
        while True:
            try:
                userinput = int(input("Enter a column: "))
                if b.can_add_to(userinput):
                    b.add_checker(self.checker, userinput)
                    self.num_moves += 1
                    return self.num_moves
                else:
                    print("Column is full or invalid. Try Again!")
            except ValueError:
                print("Invalid input. Enter a number.")

class RandomPlayer(Player):
    """ A player that makes random moves. """
    def next_move(self, b):
        free_cols = [col for col in range(b.width) if b.can_add_to(col)]
        userinput = random.choice(free_cols)
        if b.can_add_to(userinput):
            b.add_checker(self.checker, userinput)
            self.num_moves += 1
            return self.num_moves

class AIPlayer(Player):
    """AI player who wins or ties always."""
    def __init__(self, checker, tiebreak, lookahead):
        """Initialize the AI player with a checker, tiebreak strategy, and lookahead depth."""
        assert checker in 'XO'
        assert tiebreak in ('LEFT', 'RIGHT', 'RANDOM')
        assert lookahead >= 0
        self.tiebreak = tiebreak
        self.lookahead = lookahead
        super().__init__(checker)

    def max_score_column(self, scores):
        """Return the index of the column with the maximum score, considering tiebreak strategy."""
        candidates = [i for i, score in enumerate(scores) if score == max(scores)]
        if self.tiebreak == "LEFT":
            return candidates[0]
        elif self.tiebreak == "RIGHT":
            return candidates[-1]
        elif self.tiebreak == "RANDOM":
            return random.choice(candidates)

    def __repr__(self):
        """Display player info."""
        return f"Player {self.checker} ({self.tiebreak}, {self.lookahead})"
    

    def scores_for(self, b):
        """Evaluate board state and return scores for possible moves."""
        scores = [0] * b.width
        
        for col in range(b.width):
            if b.can_add_to(col):
                # Create a temporary board state for move simulation
                temp_board = Board(b.height, b.width)
                temp_board.slots = [row.copy() for row in b.slots]
                
                # Simulate adding the AI's checker
                temp_board.add_checker(self.checker, col)
                
                if temp_board.is_win_for(self.checker):
                    scores[col] = 100  # High score for a winning move
                else:
                    if self.lookahead > 0:
                        # Create an opponent AI player
                        opp = AIPlayer(self.opponent_checker(), "RIGHT", self.lookahead - 1)
                        
                        # Get scores from the opponent's perspective
                        opp_scores = opp.scores_for(temp_board)
                        
                        if 100 in opp_scores:
                            scores[col] = 0  # Block the opponent's winning move
                        elif 0 in opp_scores:
                            scores[col] = 50  # Prevent the opponent from gaining advantage
                        else:
                            scores[col] = 50
                    else:
                        scores[col] = 50

                # No need to remove checker from temp_board, as it doesn't affect the real board state
            else:
                scores[col] = -1
        
        # Debug output for final scores
        print(f"Final scores: {scores}")
        
        return scores






        
   




    def next_move(self, b):
        """Make the next move based on the highest score."""
        userinput = self.max_score_column(self.scores_for(b))
        if b.can_add_to(userinput):
            b.add_checker(self.checker, userinput)
            self.num_moves += 1
            return self.num_moves



def connect_four(p1, p2):
    """ Plays a game of Connect Four between the two specified players. """
    if p1.checker not in 'XO' or p2.checker not in 'XO' or p1.checker == p2.checker:
        print('Need one X player and one O player.')
        return None

    print('Welcome to Connect Four!')
    print()
    b = Board(6, 7)
    print(b)

    while True:
        if process_move(p1, b):
            return b
        if process_move(p2, b):
            return b

def process_move(p, b):
    """ Processes a move and checks for a win. """
    print(f"Player {p.checker}'s turn")
    p.next_move(b)
    print(b)
        
    if b.is_win_for(p.checker):
        print(f"Player {p.checker} wins in {p.num_moves} moves.\nCongratulations!")
        return True
    return False

def main():
    """ Main function to start the game """
    print("Connect Four")
    print("Choose player types:")
    print("1: Human")
    print("2: Random")
    print("3: AI")

    p1_type = input("Choose type for Player X: ")
    p2_type = input("Choose type for Player O: ")

    if p1_type == '1':
        p1 = Player('X')
    elif p1_type == '2':
        p1 = RandomPlayer('X')
    elif p1_type == '3':
        tiebreak = input("Choose tiebreak strategy for AI X (LEFT, RIGHT, RANDOM): ")
        lookahead = int(input("Choose lookahead depth for AI X: "))
        p1 = AIPlayer('X', tiebreak, lookahead)
    else:
        print("Invalid choice. Defaulting to Human player.")
        p1 = Player('X')

    if p2_type == '1':
        p2 = Player('O')
    elif p2_type == '2':
        p2 = RandomPlayer('O')
    elif p2_type == '3':
        tiebreak = input("Choose tiebreak strategy for AI O (LEFT, RIGHT, RANDOM): ")
        lookahead = int(input("Choose lookahead depth for AI O: "))
        p2 = AIPlayer('O', tiebreak, lookahead)
    else:
        print("Invalid choice. Defaulting to Human player.")
        p2 = Player('O')

    connect_four(p1, p2)

if __name__ == "__main__":
    main()
