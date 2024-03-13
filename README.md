Assumptions for this implementation: 

1. User/first player is always Player (x)
2. A board state in which a win condition for Player (x) or (o) is met is a primitive "win" for the respective player
3. All terminal state/remoteness values are permuted under perfect gameplay from both players
4. Minimax algorithm asserts Player (x) as the "maximizer" and Player (o) as the "minimizer"

Prompt: 

<img width="534" alt="Screenshot 2024-03-11 at 6 34 33 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/b6f2171b-5087-4bfd-ae1b-ade75903e686"> 

Interactive user play (perfect play bot shown):

<img width="393" alt="Screenshot 2024-03-13 at 11 32 23 AM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/618f2f9f-f814-4757-a603-6fcc8ef6040b">

--------------

Terminal state and associated remoteness values per board (w/o symmetries): 

<img width="245" alt="Screenshot 2024-03-12 at 4 24 24 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/6b7402a7-f229-47ee-9a2a-f6873e3fcaa4">

Terminal state and associated remoteness vlues per board (w/ symmetries): 

<img width="254" alt="Screenshot 2024-03-12 at 4 21 41 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/e68e6a46-ea40-4567-9c73-a2113907758d">

--------------

Hash function: 

<img width="256" alt="Screenshot 2024-03-11 at 6 46 08 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/62a1e1ed-36fc-42de-8394-34dc42e2b54c">
