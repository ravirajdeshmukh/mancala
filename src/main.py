from typing import List
import json
import os
from datetime import datetime as dt

from src.mancala import (
    NUM_PITS_PER_PLAYER,
    PLAYER1_STORE,
    PLAYER2_STORE,
    MancalaGame
)
from src.bot import BotPlayer


def print_board(board: List[int]) -> None:
    """Print the current game board in a readable format."""
    print("==================================")
    top_row = ' '.join(f"{board[i]:^3}" for i in reversed(range(0, NUM_PITS_PER_PLAYER)))
    bottom_row = ' '.join(f"{board[i]:^3}" for i in range(PLAYER1_STORE + 1, PLAYER2_STORE))
    print("              Player 1           ")
    print(f"     {top_row}      ")
    print(f"{board[PLAYER1_STORE]:^3}{' '*27}{board[PLAYER2_STORE]:^3}")
    print(f"     {bottom_row}    ")
    print("              Player 2           ")
    print("==================================")
def play() -> None:
    """Main function to run the command-line Mancala game."""
    game = MancalaGame()
    bot = BotPlayer()
    print("Welcome to Mancala!")
    mode = input("Enter '1' to play against AI, or '2' for 2-player game: ").strip()
    play_vs_ai = mode == '1'

    while not game.is_game_over():
        print_board(game.get_board())
        player = game.get_current_player()

        if play_vs_ai and player == 1:
            pit = bot.choose_move(game)
            print(f"Bot chooses pit {pit - (PLAYER1_STORE + 1)}")
        else:
            try:
                pit = int(input(f"Player {player + 1}, choose a pit (0-5): "))
                if player == 1:
                    pit += PLAYER1_STORE + 1
            except ValueError:
                print("Please enter a valid number.")
                continue

        result = game.take_turn(pit)
        if result is not True:
            print("Invalid move. Valid pits:", result)
            continue

    game.finalize_game()
    print_board(game.get_board())
    print("Game over!")
    p1_score, p2_score = game.get_scores()
    print(f"Player 1 store: {p1_score}")
    print(f"Player 2 store: {p2_score}")
    if p1_score > p2_score:
        print("Player 1 wins!")
    elif p2_score > p1_score:
        print("Player 2 wins!" if not play_vs_ai else "AI wins!")
    else:
        print("It's a tie!")
    
    # logging game moves   
    log_path=os.path.join(os.getcwd(),f"game_log_{dt.now().strftime('%Y%m%d%H%M%S')}.json") 
    with open(log_path, "w+") as f:
        json.dump({
            "moves": game.move_log,
            "winner": 1 if p1_score > p2_score 
                        else
                      2 if p2_score > p1_score
                        else 0
        }, f, indent=2)
        
    print(f"Move log can be found at {log_path}")

if __name__ == "__main__":
    play()