import copy
import random
import math
import time

endgames = {"win": 0, "tie": 0, "lose": 0}
default_board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
outcomes = {}
memory = {} 
k = {}

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

#HASH FUNCTION:
def memoize(f): 
    # Decorator function can be implemented as pleased
    # This inner function has access to memory and 'f'
    def inner(num): 
        if num not in memory:          
            memory[num] = f.board(num) 
        return memory[num] 
    return inner

def fact(n):
    # n * (n-1) ... 1
    return 1 if n <= 1 else n * fact(n-1)

def c(n, k):
    # n choose k
    return fact(n)//fact(k)//fact(n-k)

# s = total number of available slots
# o = total number of Os
# x = total number of Xs
def rearrange(x, o, s):
    # Number of rearrangements for Xs and Os given S slots -- see alternative() for an alternative equivalent expression
    if (x < 0) or (o < 0):
        return 0
    return fact(s)//fact(o)//fact(x)//fact(s - x - o)

def alternative(x, o, s):
    # Another mathematically accurate formula for computing rearrangements
    return c(s, x + o) * c(x + o, x)

def xs_and_os(p):
    # Tuple of the number of Xs and Os, given P pieces
    return (math.ceil(p/2), math.floor(p/2))

def positions(s):
    #Total number of tictactoe positions, given S slots
    all_pos = [xs_and_os(p) for p in range(s + 1)]
    rearrangements = [rearrange(cross, naught, s) for cross, naught in all_pos]
    return sum(rearrangements)

def hashing(string, x, o, s):
    # Combinatorially perfect hash function 
    previous = [xs_and_os(p) for p in range(s-1)]
    biases = [rearrange(cross, naught, s) for cross, naught in previous]
    def condense(string, x, o, s):
        if string:
            first = string[0]
            if first == "-":
                return condense(string[1:], x, o, s-1)
            elif first == "o":
                offset = (0 if len(string) == 1 else (rearrange(x, o, s) - rearrange(x, o-1, s-1) - rearrange(x-1, o, s-1)))
                return offset + condense(string[1:], x, o-1, s-1)
            elif first == "x":
                offset = (0 if len(string) == 1 else (rearrange(x, o, s) - rearrange(x-1, o, s-1)))
                return offset + condense(string[1:], x-1, o, s-1)
        return 0
    return sum(biases) + condense(string, x, o, s) 

"""
Separate implementation of unhashing function (can be made compatible with current hashing format):
    def rearranger_unhash_o_only(s,o,i,bC,oC):
        "Return the unhashed board with S slots, O os, at index I with characters for blank-o bC oC"
        if s == 0:
            return ""
        elif s == o:
            return oC * s ## all os
        elif i < rearranger_o_only(s-1, o): ## no o cause #pos with o first not > i
            return bC + rearranger_unhash_o_only(s-1, o, i, bC, oC)
        else:
            return oC + rearranger_unhash_o_only(s-1, o-1, i-rearranger_o_only(s-1, o), bC, oC)

    def rearranger_unhash(s,o,x,i,bC,oC,xC):
        "Return the unhashed board with S slots, O os, X xs at index I with characters for blank-o-x bC oC xC"
        if s == 0:
            return ""
        elif (o == 0) and (x == 0): ## all blanks
            return bC * s           ## ...so return all blanks
        elif s == o:                ## all Os
            return oC * s           ## ...so return all Os
        elif s == x:                ## all Xs
            return xC * s           ## ...so return all Xs
        elif s == (o + x):          ## no blanks
            return rearranger_unhash_o_only(s,x,i,oC,xC) ## so treat like ox only
        elif o == 0:                ## no Os
            return rearranger_unhash_o_only(s,x,i,bC,xC) ## so treat like -x only
        elif x == 0:                ## no Xs
            return rearranger_unhash_o_only(s,o,i,bC,oC) ## so treat like -o only
        elif i < rearranger(s-1,o,x): ## index hasn't run out of blanks
            return bC + rearranger_unhash(s-1,o,x,i,bC,oC,xC) ## so put a blank there
        elif i < rearranger(s-1,o,x) + rearranger(s-1,o-1,x): ## index hasn't run out of os
            return oC + rearranger_unhash(s-1,o-1,x,i-rearranger(s-1,o,x),bC,oC,xC) ## so put an o there
        else: ## index is bigger than -s and os
            return xC + rearranger_unhash(s-1,o,x-1,i-rearranger(s-1,o,x)-rearranger(s-1,o-1,x),bC,oC,xC)
"""

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

    def primitive(self):
        return 1 if self.win_condition("x") else (-1 if self.win_condition("o") else (0 if "-" not in self.board else ""))

    def is_over(self):
        return type(self.primitive()) != str
    
    def solve(self):
        if type(self.primitive()) != str:
            return self.primitive()
        else:
            children = [self.domove(move) for move in self.generate()]
            spread = [child.terminal for child in children]
            if self.turn:
                return 1 if 1 in spread else (0 if 0 in spread else -1)
            else:
                return -1 if -1 in spread else (0 if 0 in spread else 1)

class Remoteness(Board):
    # Calculate remoteness from terminal state

    def branches(self):
        branches = [self.domove(move) for move in self.generate()]
        leaves = [child.terminal for child in branches]
        return branches, leaves

    def best_move(self):
        if self.is_over():
            return self.board
        children, spread = self.branches()
        evaluate = [self.terminal + k for k in spread]
        best_value = max(evaluate) if self.turn else min(evaluate)
        if evaluate.count(best_value) > 1:
            if self.block():
                return children[self.block()].board
        return children[evaluate.index(best_value)].board
    
    def depth(self):
        if self.is_over():
            return 0
        elif not self.terminal:
            return len([e for e in self.board if e == "-"])
        children, spread = self.branches()
        evaluate = [self.terminal + k for k in spread]
        best_value = max(evaluate) if self.turn else min(evaluate)
        if evaluate.count(best_value) > 1:
            if self.block():
                return 1 + Remoteness(children[self.block()].board).depth()
        return 1 + Remoteness(children[evaluate.index(best_value)].board).depth()

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

    difficulty = 0

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

        print(f"Player (x) Wins in: {self.depth()} moves" if self.terminal == 1 else (f"Tie in: {self.depth()} moves" if not self.terminal else f"Player (o) Wins in: {self.depth()} moves"))

        ui = input("You will be Player (x). Please enter a cell number: ")
        while not(ui.isnumeric() and int(ui) in options):
            print("Invalid move/command. See options above.")
            ui = input("Please enter a different cell number: ")

        new_board = list(self.board)
        new_board[int(ui)-1] = "x"
        return Play(new_board)

    def random_strat(self):
        children = [self.domove(move) for move in self.generate()]
        return random.choice(children).board


"""
To play, run this code snippet in your terminal in the file directory!
    game = Play(default_board)
    game.gameplay()
"""

# OPTIONAL:

"""
To see the total number of possible wins, loses, or ties, enable this code in this file!

for board in valid_boards():
    value = Board(board).terminal
    if value == 1:
        endgames["win] += 1
    elif not value:
        endgames["tie"] += 1
    else:
        endgames["lose"] += 1
"""

"""
All combinations of remoteness and terminal state values (printing could vary):
    def output():
        for i in valid_boards:
            string = f"{Board(i).terminal}, {Remoteness(i).depth()}"
            if string in outcomes:
                outcomes[string] += 1
            else:
                outcomes[string] = 1
        all_combs = [f"{i}, {k}" for i in range(-1, 2) for k in range(10)]
        for item in all_combs:
            if item not in outcomes:
                outcomes[item] = 0
        print("Remote", " Win ", " Lose ", " Tie ", " Total")
        print("----------------------------------")
        print("9      ", 
        str(outcomes["1, 9"]) + "    ", 
        str(outcomes["-1, 9"]) + "     ", 
        str(outcomes["0, 9"]) + "    ", 
        str(outcomes["1, 9"]+outcomes["-1, 9"]+outcomes["0, 9"]))
        print("8      ", 
        str(outcomes["1, 8"]) + "    ", 
        str(outcomes["-1, 8"]) + "     ", 
        str(outcomes["0, 8"]) + "    ", 
        str(outcomes["1, 8"]+outcomes["-1, 8"]+outcomes["0, 8"]))
        print("7      ", 
        str(outcomes["1, 7"]) + "    ", 
        str(outcomes["-1, 7"]) + "     ", 
        str(outcomes["0, 7"]) + "   ", 
        str(outcomes["1, 7"]+outcomes["-1, 7"]+outcomes["0, 7"]))
        print("6      ", 
        str(outcomes["1, 6"]) + "    ", 
        str(outcomes["-1, 6"]) + "     ", 
        str(outcomes["0, 6"]) + "  ", 
        str(outcomes["1, 6"]+outcomes["-1, 6"]+outcomes["0, 6"]))
        print("5      ", 
        str(outcomes["1, 5"]) + "  ", 
        str(outcomes["-1, 5"]) + "    ", 
        str(outcomes["0, 5"]) + "  ", 
        str(outcomes["1, 5"]+outcomes["-1, 5"]+outcomes["0, 5"]))
        print("4      ", 
        str(outcomes["1, 4"]) + "  ", 
        str(outcomes["-1, 4"]) + "    ", 
        str(outcomes["0, 4"]) + "  ", 
        str(outcomes["1, 4"]+outcomes["-1, 4"]+outcomes["0, 4"]))
        print("3      ", 
        str(outcomes["1, 3"]) + "  ", 
        str(outcomes["-1, 3"]) + "    ", 
        str(outcomes["0, 3"]) + "  ", 
        str(outcomes["1, 3"]+outcomes["-1, 3"]+outcomes["0, 3"]))
        print("2      ", 
        str(outcomes["1, 2"]) + "  ", 
        str(outcomes["-1, 2"]) + "   ", 
        str(outcomes["0, 2"]) + "  ", 
        str(outcomes["1, 2"]+outcomes["-1, 2"]+outcomes["0, 2"]))
        print("1      ", 
        str(outcomes["1, 1"]) + " ", 
        str(outcomes["-1, 1"]) + "   ", 
        str(outcomes["0, 1"]) + "   ", 
        str(outcomes["1, 1"]+outcomes["-1, 1"]+outcomes["0, 1"]))
        print("0      ", 
        str(outcomes["1, 0"]) + "  ", 
        str(outcomes["-1, 0"]) + "   ", 
        str(outcomes["0, 0"]) + "   ", 
        str(outcomes["1, 0"]+outcomes["-1, 0"]+outcomes["0, 0"]))
        print("----------------------------------")
"""

