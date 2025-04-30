import unittest
from mancala import (
    MancalaGame,
    PLAYER1_STORE)

class TestMancalaGame(unittest.TestCase):
    def test_initial_board(self):
        game = MancalaGame()
        self.assertEqual(game.get_board(), [6]*6 + [0] + [6]*6 + [0])

    def test_valid_move(self):
        game = MancalaGame()
        self.assertTrue(game.take_turn(0))

    def test_invalid_move(self):
        game = MancalaGame()
        self.assertIsInstance(game.take_turn(7), list)

    def test_capture_rule(self):
        game = MancalaGame()
        game.board = [0, 0, 0, 1, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0]
        game.take_turn(3)
        self.assertEqual(game.board[PLAYER1_STORE], 7)

    def test_game_over_detection(self):
        game = MancalaGame()
        game.board = [0]*6 + [0] + [1]*6 + [0]
        self.assertTrue(game.is_game_over())


if __name__ == "__main__":
    unittest.main()
