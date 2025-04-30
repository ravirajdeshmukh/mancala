"""
Mancala Game Logic

This module implements the basic logic for a 2-player Mancala game.
It includes board setup, turn-taking, capturing, and end-game finalization.
Designed for easy integration with any user interface.

Classes:
    MancalaGame: Handles all game functionality including turns, board updates, and win condition checking.
"""

from typing import List, Tuple, Union

# Constants
NUM_PITS_PER_PLAYER = 6
TOTAL_PITS = 14
PLAYER1_STORE = 6
PLAYER2_STORE = 13

class MancalaGame:
    def __init__(self) -> None:
        """Initialize the game board and current player."""
        self.board: List[int] = [6] * NUM_PITS_PER_PLAYER + [0] + [6] * NUM_PITS_PER_PLAYER + [0]
        self.current_player: int = 0  # 0 for Player 1, 1 for Player 2
        self.move_log=[] # optional for logging moves.

    def __repr__(self) -> str:
        """String representation of the game state."""
        return f"MancalaGame(board={self.board}, current_player={self.current_player})"

    def get_board(self) -> List[int]:
        """Return a copy of the current board."""
        return self.board.copy()

    def get_current_player(self) -> int:
        """Return the current player (0 or 1)."""
        return self.current_player

    def get_valid_pits(self) -> List[int]:
        """Return a list of valid pit indices for the current player (as user-facing indices 0–5)."""
        if self.current_player == 0:
            return [i for i in range(0, NUM_PITS_PER_PLAYER) if self.board[i] > 0]
        else:
            return [i - (PLAYER1_STORE + 1) for i in range(PLAYER1_STORE + 1, PLAYER2_STORE) if self.board[i] > 0]

    def is_game_over(self) -> bool:
        """Return True if the game is over (either side has all pits empty)."""
        return all(stone == 0 for stone in self.board[0:NUM_PITS_PER_PLAYER]) or \
               all(stone == 0 for stone in self.board[PLAYER1_STORE + 1:PLAYER2_STORE])

    def finalize_game(self) -> None:
        """Move all remaining stones to the appropriate stores at the end of the game."""
        self.board[PLAYER1_STORE] += sum(self.board[0:NUM_PITS_PER_PLAYER])
        self.board[PLAYER2_STORE] += sum(self.board[PLAYER1_STORE + 1:PLAYER2_STORE])
        for i in range(0, NUM_PITS_PER_PLAYER):
            self.board[i] = 0
        for i in range(PLAYER1_STORE + 1, PLAYER2_STORE):
            self.board[i] = 0

    def take_turn(self, pit_index: int) -> Union[bool, List[int]]:
        """
        Execute a move for the current player from the given pit index.

        Args:
            pit_index (int): Internal board index selected by the player.

        Returns:
            Union[bool, List[int]]: True if move is valid, list of valid user-facing pit indices if not.
        """
        if self.current_player == 0 and not (0 <= pit_index < NUM_PITS_PER_PLAYER):
            return self.get_valid_pits()
        if self.current_player == 1 and not (PLAYER1_STORE + 1 <= pit_index < PLAYER2_STORE):
            return self.get_valid_pits()
        if self.board[pit_index] == 0:
            return self.get_valid_pits()

        stones = self.board[pit_index]
        self.board[pit_index] = 0
        i = pit_index

        while stones > 0:
            i = (i + 1) % TOTAL_PITS
            if self.current_player == 0 and i == PLAYER2_STORE:
                continue
            if self.current_player == 1 and i == PLAYER1_STORE:
                continue
            self.board[i] += 1
            stones -= 1

        # Capture condition
        if self.current_player == 0 and (0 <= i < NUM_PITS_PER_PLAYER) and self.board[i] == 1:
            opposite = 12 - i
            self.board[PLAYER1_STORE] += self.board[opposite] + 1
            self.board[i] = self.board[opposite] = 0
        elif self.current_player == 1 and (PLAYER1_STORE + 1 <= i < PLAYER2_STORE) and self.board[i] == 1:
            opposite = 12 - i
            self.board[PLAYER2_STORE] += self.board[opposite] + 1
            self.board[i] = self.board[opposite] = 0

        # Extra turn condition
        if (self.current_player == 0 and i == PLAYER1_STORE) or (self.current_player == 1 and i == PLAYER2_STORE):
            return True
        else:
            self.current_player = 1 - self.current_player
            
        self.move_log.append({
            "player": self.current_player,
            "pit_index": pit_index,
            "valid": True or False,
            "board": self.board.copy()
        })

        return True

    def get_scores(self) -> Tuple[int, int]:
        """Return the current score (stones in store) of both players."""
        return self.board[PLAYER1_STORE], self.board[PLAYER2_STORE]