from mancala import MancalaGame, PLAYER1_STORE
import random

class BotPlayer:
    """A simple AI player that selects the first valid move."""
    def choose_move(self, game: MancalaGame) -> int:
        valid_pits = game.get_valid_pits()
        if not valid_pits:
            return -1
        return random.choice(valid_pits) + (PLAYER1_STORE + 1 if game.get_current_player() == 1 else 0)