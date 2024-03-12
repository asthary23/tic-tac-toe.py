import copy
import random

default_board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]

def win_condition(board, player):
    wins_list = [
    [0,1,2], 
    [3,4,5], 
    [6,7,8], 
    [0,3,6], 
    [1,4,7], 
    [2,5,8], 
    [0,4,8], 
    [2,4,6]
    ]
    end = len(wins_list)
    i = 0
    while i < end:
        cond = all([board[cell] == player for cell in wins_list[i]])
        if cond:
            return cond
        i += 1
    return False

def valid_boards():
    # All 5478 valid board states under assumptions (see clauses)
    symbols = ["x", "o", "-"]
    all_boards = [[i, j, k, l, m, n, o, p, q] for i in symbols for j in symbols for k in symbols for l in symbols for m in symbols for n in symbols for o in symbols for p in symbols for q in symbols]
    possible = []
    for tests in all_boards:
        diff = sum(1 for x in tests if x == "x") - sum(1 for x in tests if x == "o")
        o_win = win_condition(tests, "o")
        x_win = win_condition(tests, "x")
        if diff == 0:
            if (o_win and not(x_win)) or (not(x_win) and not(o_win)):
                possible.append(tests)
        elif diff == 1:
            if (x_win and not(o_win)) or (not(x_win) and not(o_win)):
                possible.append(tests)
    return possible

#CLASSES:
class Board:
    # Initializing grid
    wins_list = [
    [0,1,2], 
    [3,4,5], 
    [6,7,8], 
    [0,3,6], 
    [1,4,7], 
    [2,5,8], 
    [0,4,8], 
    [2,4,6]
    ]

    def __init__(self, board):
        self.board = board
        self.x = sum([1 for x in self.board if x == "x"])
        self.o = sum([1 for o in self.board if o == "o"])
        self.turn = 1 if self.x == self.o else 0
        self.terminal = self.solve()
    
    def win_condition(self, player):
        end = len(self.wins_list)
        i = 0
        while i < end:
            if all([self.board[cell] == player for cell in self.wins_list[i]]):
                return True
            i += 1
        return False

    def generate(self):
        return [move for move in range(len(self.board)) if self.board[move] == "-"]
    
    def domove(self, cell): 
        new_board = list(self.board)
        new_board[cell] = "x" if self.turn else "o"
        return Board(new_board)

    def branches(self):
        branches = [self.domove(move) for move in self.generate()]
        leaves = [child.terminal for child in branches]
        return branches, leaves

    def primitive(self):
        return 1 if self.win_condition("x") else (-1 if self.win_condition("o") else (0 if "-" not in self.board else ""))

    def is_over(self):
        return type(self.primitive()) != str
    
    def solve(self):
        if self.is_over():
            return self.primitive()
        else:
            children, spread = self.branches()
            if self.turn:
                return 1 if 1 in spread else (0 if 0 in spread else -1)
            else:
                return -1 if -1 in spread else (0 if 0 in spread else 1)

class Remoteness(Board):
    # Calculate remoteness from terminal state

    def __init__(self, board, thus_far=0):
        super().__init__(board)
        self.thus_far = thus_far
        self.depth = self.search()

    def best_move(self):
        children, spread = self.branches()
        next_move = [child for child in children if child.is_over()]
        if self.is_over():
            return self.board
        elif len(next_move) and self.turn:
            primitives = [child.primitive() for child in next_move]
            if self.turn and 1 in primitives:
                return next_move[primitives.index(1)].board
            elif not self.turn and -1 in primitives:
                return next_move[primitives.index(-1)].board
        evaluate = [self.terminal + k for k in spread]
        best_value = max(evaluate) if self.turn else min(evaluate)
        if evaluate.count(best_value) > 1 and self.block():
            return children[self.block()].board
        return children[evaluate.index(best_value)].board
    
    def search(self):
        children, spread = self.branches()
        next_move = [child for child in children if child.is_over()]
        if self.is_over():
            return 0
        elif not self.terminal:
            return len([e for e in self.board if e == "-"])
        elif len(next_move) and self.turn:
            primitives = [child.primitive() for child in next_move]
            if self.turn and 1 in primitives:
                return 1
            elif not self.turn and -1 in primitives:
                return 1
        else:
            evaluate = [self.terminal + k for k in spread]
            best_value = max(evaluate) if self.turn else min(evaluate)
            if evaluate.count(best_value) > 1 and self.block():
                return 1 + Remoteness(children[self.block()].board).search()
            return 1 + Remoteness(children[evaluate.index(best_value)].board).search()

    def block(self):
        opponent_marker = "x" if not self.turn else "o"
        for i in self.generate():
            new_board = list(self.board)
            new_board[i] = opponent_marker
            if Remoteness(new_board).win_condition(opponent_marker):
                return self.generate().index(i)
        return False

class Play(Remoteness):
    # Simulate gameplay

    def __init__(self, board):
        super().__init__(board)
        self.difficulty = 0

    def __str__(self):
        rows = []
        for i in range(3):
            row = " ".join(self.board[i * 3:(i * 3) + 3])
            rows.append(row)
        return "\n".join(rows)

    def gameplay(self):
        print("Select an option:")
        print("Option 1: Random Move Bot")
        print("Option 2: Perfect Play Bot")
        print("Enter 1 or 2 for which difficulty you'd like to play.")

        difficulty = input("Difficulty: ")
        while not(difficulty.isnumeric() and int(difficulty) in [1,2]):
            print("Invalid move/command. See options above.")
            difficulty = input("Please enter a different cell number: ")
        if int(difficulty) == 1:
            Play.difficulty = int(difficulty)
            return self.play()
        elif int(difficulty) == 2:
            Play.difficulty = int(difficulty)
            return self.play()       
    
    def play(self):
        if type(self.primitive()) != str:
            print(str(self))
            print("Player (x) Wins!" if self.primitive() == 1 else ("Tie!" if self.primitive() == 0 else "Player (o) Wins!"))
        else:
            if Play.difficulty == 1:
                return self.user_play().play() if self.turn else Play(self.random_strat()).play() 
            else:
                return self.user_play().play() if self.turn else Play(self.best_move()).play()

    def user_play(self):
        print(str(self))

        options = [choice+1 for choice in self.generate()]
        print("Options: ", options)

        print(f"Player (x) Wins in: {self.depth} moves" if self.terminal == 1 else (f"Tie in: {self.depth} moves" if not self.terminal else f"Player (o) Wins in: {self.depth} moves"))

        ui = input("You will be Player (x). Please enter a cell number: ")
        while not(ui.isnumeric() and int(ui) in options):
            print("Invalid move/command. See options above.")
            ui = input("Please enter a different cell number: ")

        new_board = list(self.board)
        new_board[int(ui)-1] = "x"
        return Play(new_board)

    def random_strat(self):
        children, _ = self.branches()
        return random.choice(children).board

#To play, run this code snippet in your terminal in the file directory!
game = Play(default_board)
game.gameplay()
