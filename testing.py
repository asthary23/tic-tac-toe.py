from tictactoe import *
from collections import defaultdict

endgames = {"win": 0, "tie": 0, "lose": 0}
outcomes = defaultdict(int)
symmetries = []

def cousins(board):
    c5 = [board[i] for i in [2,1,0,5,4,3,8,7,6]] 
    c4 = [board[i] for i in [6,7,8,3,4,5,0,1,2]] 
    c6 = [board[i] for i in [8,5,2,7,4,1,6,3,0]] 
    c7 = [board[i] for i in [0,3,6,1,4,7,2,5,8]] 
    c2 = [board[i] for i in [8,7,6,5,4,3,2,1,0]] 
    c1 = [board[i] for i in [6,3,0,7,4,1,8,5,2]] 
    c3 = [board[i] for i in [2,5,8,1,4,7,0,3,6]] 
    return [board, c1, c2, c3, c4, c5, c6, c7]

# To see the total number of possible wins, loses, or ties, enable this code in the tictactoe.py file!

for board in valid_boards():
    value = Board(board).terminal # or Remoteness(board).depth to produce all remoteness values
    if value == 1:
        endgames["win"] += 1
    elif not value:
        endgames["tie"] += 1
    else:
        endgames["lose"] += 1

def enable_symmetries():
    for board in valid_boards:
        # Check if any symmetry exists
        if any([sym in symmetries for sym in cousins(board)]):
            continue  # If symmetry exists, move to next board
        else:
            # If no symmetry exists, hash the board and store outcome
            symmetries.append(board)
            outcomes[f"{Board(board).terminal}, {Remoteness(board).depth}"] += 1

def without_symmetries():
    for board in valid_boards:
        outcomes[f"{Board(board).terminal}, {Remoteness(board).depth()}"] += 1


# All combinations of remoteness and terminal state values (printing could vary):
def output(valid_boards):
  #insert without_symmetries() to disregard symmetries else call enable_symmetries()

  print("Depth", "Win  ", "Lose  ", "Tie ", "Total")
  print("-" * 32)  # Print 32 hyphens for consistent line length

  for rem in range(10):
    win_str = f"{outcomes[f'1, {rem}']}"  # String representation of win count
    lose_str = f"{outcomes[f'-1, {rem}']}"  # String representation of lose count
    tie_str = f"{outcomes[f'0, {rem}']}"  # String representation of tie count
    total_str = f"{outcomes[f'1, {rem}'] + outcomes[f'-1, {rem}'] + outcomes[f'0, {rem}']}"  # String representation of total count
    # Calculate spaces needed based on string length
    win_spaces = max(0, 4 - len(win_str))  # Minimum 4 spaces, adjust based on string length
    lose_spaces = max(0, 4 - len(lose_str))
    tie_spaces = max(0, 4 - len(tie_str))
    total_spaces = max(0, 5 - len(total_str))  # Minimum 5 spaces for total
    print(f"{rem:3}", win_spaces*" ", win_str, lose_spaces*" ", lose_str, tie_spaces*" ", tie_str, total_spaces*" ", total_str)
    print("-" * 32)  # Print 32 hyphens for consistent line length
