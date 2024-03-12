from tictactoe import *
from collections import defaultdict

endgames = {"win": 0, "tie": 0, "lose": 0}
outcomes = {}

# To see the total number of possible wins, loses, or ties, enable this code in the tictactoe.py file!

for board in valid_boards():
    value = Board(board).terminal # or Remoteness(board).depth to produce all remoteness values
    if value == 1:
        endgames["win"] += 1
    elif not value:
        endgames["tie"] += 1
    else:
        endgames["lose"] += 1


# All combinations of remoteness and terminal state values (printing could vary):
def output(valid_boards):
  outcomes = defaultdict(int)
  for board in valid_boards:
    outcomes[f"{Board(board).terminal}, {Remoteness(board).depth()}"] += 1

  print("Depth", "Win  ", "Lose  ", "Tie  ", "Total")
  print("-" * 36)  # Print 36 hyphens for consistent line length

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
    print("-" * 36)  # Print 36 hyphens for consistent line length
