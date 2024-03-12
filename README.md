Assumptions for this implementation: 
1. User/first player is always Player (x)
2. A board state in which a win condition for Player (x) or (o) is met is a primitive "win" for the respective player
3. All terminal state/remoteness values are permuted under perfect gameplay from both players
4. Minimax algorithm asserts Player (x) as the "maximizer" and Player (o) as the "minimizer"

Interactive User Play (Perfect Play Bot shown):

<img width="534" alt="Screenshot 2024-03-11 at 6 34 33 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/b6f2171b-5087-4bfd-ae1b-ade75903e686">
<img width="530" alt="Screenshot 2024-03-11 at 6 35 12 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/97cca371-e1fe-4b8b-ba75-2d4ca68b5469">
<img width="533" alt="Screenshot 2024-03-11 at 6 35 48 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/dc982ed2-640b-40ed-9702-1dbeb8b6edf9">

--------------

Associated Remoteness/Depth and Terminal States under aforementioned assumptions: 

<img width="245" alt="Screenshot 2024-03-12 at 4 24 24 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/6b7402a7-f229-47ee-9a2a-f6873e3fcaa4">

Associated Remoteness/Depth and Terminal States (with symmetries) under aforementioned assumptions: 

<img width="254" alt="Screenshot 2024-03-12 at 4 21 41 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/e68e6a46-ea40-4567-9c73-a2113907758d">

--------------

Hash Function: 

<img width="256" alt="Screenshot 2024-03-11 at 6 46 08 PM" src="https://github.com/asthary23/tic-tac-toe.py/assets/154309720/62a1e1ed-36fc-42de-8394-34dc42e2b54c">
