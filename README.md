# Introduction: 👋
This is a simple implementation of the Mancala game. In this version of the game - it is made as a two player game. Something to note - the original requirement was to create this game using Java and develop a UI in the form of a web application but I am more comfortable writing code in Python although I can manage some java backend development. The UI of the game is a simple representation done in the terminal using numbers.

# What does the board look like? 🎲
Since we could only manage a backend friendly UI - we have used the power of terminal to create a representation of the board. When executed the board looks like the following:

```text
         Player1     
    6  6  6  6  6  6
  
 0                     0
  
    6  6  6  6  6  6
         Player2    
```

# How is this board handled on the backend?
On the inside we are using a python array to mimic the board and also for managing the sequential movement of the stones. With their ability of accessing elements are specific indices - we are able to manage the skipping of opponents store while moving stones. The above board when represented in an array would look like the following:

```text
            Player 1 side
    ╔════╦════╦════╦════╦════╦════╗
    ║ 5  ║ 4  ║  3 ║  2 ║  1 ║  0 ║
    ╚════╩════╩════╩════╩════╩════╝

[6] ← P1 Store                       [13] ← P2 Store

    ╔════╦════╦════╦════╦════╦════╗
    ║  7 ║  8 ║  9 ║ 10 ║ 11 ║ 12 ║
    ╚════╩════╩════╩════╩════╩════╝
            Player 2 side
```

In the above representation, index 6 and 13 houses the stores for both the players 1 and 2 respectively.

# What rules are coded into this version of the game and how? 🕵️

- **6 pits** per player with **6 stones** each initially.
  - With the ```NUM_PITS_PER_PLAYER``` we control the number of pits per player and with 
    ```
    [6]*NUM_PITS_PER_PLAYER + [0] + [6]*NUM_PITS_PER_PLAYER + [0]
    ```
  - We control the number of stone per pit with ```[6]``` being number of stones and ```[0]``` being the empty stores per player.
- Players sow stones **counter-clockwise**.
  - We are doing this using the following line in the ```take_turn()```.
  ```
    i = (i + 1) % TOTAL_PITS
  ```
- **Skip opponent’s store** when sowing.
  - We are doing this using the following lines in the ```take_turn()```.
  ```
    if self.current_player == 0 and i == PLAYER2_STORE:
                continue
    if self.current_player == 1 and i == PLAYER1_STORE:
        continue
  ```
- **Free extra turn** if last stone lands in own store.
  - Again this is being handled in the ```take_turn()``` using the following lines:
  ```
    # Check for extra turn
        if (self.current_player == 0 and i == PLAYER1_STORE) or (self.current_player == 1 and i == PLAYER2_STORE):
            return True  # Player gets another turn
        else:
            self.current_player = 1 - self.current_player
  ```
- **Capture rule** if last stone lands in empty own pit.
  - For this we are checking for the current player if the current index is within his range of pits and has count of 1, then we calculate the index opponent's index directly opposite to the current index -> make its count 0 and add the sum of its last value and 1 to the current player's store. This can be seen in the snippet below( for player 1):
  ```
    if self.current_player == 0 and (0 <= i < NUM_PITS_PER_PLAYER) and self.board[i] == 1:
        opposite = 12 - i
        self.board[PLAYER1_STORE] += self.board[opposite] + 1
        self.board[i] = self.board[opposite] = 0
  ```
- **Game ends** when one side is empty.
  - The following condition checks if either of the players' (all)pits are empty.
  ```
    all(stone == 0 for stone in self.board[0:NUM_PITS_PER_PLAYER]) or \
               all(stone == 0 for stone in self.board[PLAYER1_STORE + 1:PLAYER2_STORE])
  ```
- **Winner** is the player with the most stones in their store.
  - Once either of the players' pits are empty we add up the stones for their respective pits and compare them to declare the winner by unanimous decision.  🥊

# What is the project structure?
```
MANCALA/
├── src/
│   ├── __init__.py
│   ├── mancala.py         # MancalaGame and AIPlayer classes
│   └── main.py            # Entry point
├── test_mancala.py        # Unit tests
├── Dockerfile
├── requirements.txt
└── README.md
```

# Do I need to install any requirements for this?
No. The application has been dockerised. So all the requirements(tho nothing specific) are taken care of in the dockerfile.
Since the original requirement was posted in Java and I have developed the solution in Python - dockerising would ensure smooth and hastlefree experience.

# How do I play the game?
There are 2 ways to play the game:
1. Building -> Running the docker container. To do this:
```
docker build -t mancala-game .

docker run -it mancala-game
```
2. Running the code locally 
```
# Run the game
python main.py

# Run tests
python -m unittest discover -s test
```

# How do you ensure the game works as programmed? 🤔
For this, we have added test cases which can be further expanded to cover more scenarios. Right now we are checking the following conditions:
 - initial board setup 🎲
 - valid move check ✅
 - invalid move check ❌
 - capture rule check 🛡️
 - game over detection 🏁

# What are the highlights of your solution? 
Inorder to make the solution unique we have tried to follow best practises and implemented some software engineering principles:
 - Separation of concerns.
 - Type hints and docstrings 
 - Single responsibility principle
 - Test-Driven Development with unittest

Apart from this the implementation has some cool features like:
 - Bot player to practise and master the game.💪🐐
 - move logging to learn from previous games to potentially build an ML model.😉


# Future improvements:
- having a more fancier UI.
- using ML and the move logs to make the bot smarter.
- add support for multi player( more than 2) games.