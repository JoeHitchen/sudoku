from unittest import TestCase

from .structures import Board, Token
from . import strategies


class Test_Strategies(TestCase):

    def test__last_remaining(self) -> None:

        puzzle_board = Board()
        puzzle_board.set_puzzle([
            {'cell': (1, 1), 'value': Token.ONE},
            {'cell': (2, 4), 'value': Token.ONE},
            {'cell': (3, 7), 'value': Token.SEVEN},
            {'cell': (3, 8), 'value': Token.EIGHT},
        ])

        strategies.resolve_last_remaining(puzzle_board)

        resolved_board = Board()
        resolved_board.set_puzzle([
            {'cell': (1, 1), 'value': Token.ONE},
            {'cell': (2, 4), 'value': Token.ONE},
            {'cell': (3, 7), 'value': Token.SEVEN},
            {'cell': (3, 8), 'value': Token.EIGHT},
            {'cell': (3, 9), 'value': Token.ONE},
        ])

        self.assertEqual(
            [cell.options for cell in puzzle_board.cells],
            [cell.options for cell in resolved_board.cells],
        )

    def test__naked_pairs(self) -> None:

        puzzle_board = Board()
        puzzle_board.set_puzzle([
            {'cell': (1, 1), 'value': Token.ONE},
            {'cell': (1, 2), 'value': Token.TWO},
            {'cell': (1, 3), 'value': Token.THREE},
            {'cell': (1, 4), 'value': Token.FOUR},
            {'cell': (1, 5), 'value': Token.FIVE},
            {'cell': (1, 6), 'value': Token.SIX},
            {'cell': (1, 7), 'value': Token.SEVEN},
            {'cell': (2, 4), 'value': Token.ONE},
            {'cell': (2, 5), 'value': Token.TWO},
            {'cell': (2, 6), 'value': Token.THREE},
            {'cell': (3, 1), 'value': Token.FOUR},
            {'cell': (3, 2), 'value': Token.FIVE},
            {'cell': (3, 3), 'value': Token.SIX},
            {'cell': (4, 7), 'value': Token.ONE},
            {'cell': (4, 8), 'value': Token.FOUR},
            {'cell': (5, 7), 'value': Token.TWO},
            {'cell': (5, 8), 'value': Token.SIX},
            {'cell': (7, 7), 'value': Token.FOUR},
            {'cell': (7, 8), 'value': Token.ONE},
            {'cell': (8, 7), 'value': Token.FIVE},
            {'cell': (8, 8), 'value': Token.THREE},
        ])

        strategies.resolve_naked_pairs(puzzle_board)

        resolved_board = Board()
        resolved_board.set_puzzle([
            {'cell': (1, 1), 'value': Token.ONE},
            {'cell': (1, 2), 'value': Token.TWO},
            {'cell': (1, 3), 'value': Token.THREE},
            {'cell': (1, 4), 'value': Token.FOUR},
            {'cell': (1, 5), 'value': Token.FIVE},
            {'cell': (1, 6), 'value': Token.SIX},
            {'cell': (1, 7), 'value': Token.SEVEN},
            {'cell': (2, 4), 'value': Token.ONE},
            {'cell': (2, 5), 'value': Token.TWO},
            {'cell': (2, 6), 'value': Token.THREE},
            {'cell': (2, 7), 'value': Token.SIX},
            {'cell': (2, 8), 'value': Token.FIVE},
            {'cell': (2, 9), 'value': Token.FOUR},
            {'cell': (3, 1), 'value': Token.FOUR},
            {'cell': (3, 2), 'value': Token.FIVE},
            {'cell': (3, 3), 'value': Token.SIX},
            {'cell': (3, 7), 'value': Token.THREE},
            {'cell': (3, 8), 'value': Token.TWO},
            {'cell': (3, 9), 'value': Token.ONE},
            {'cell': (4, 7), 'value': Token.ONE},
            {'cell': (4, 8), 'value': Token.FOUR},
            {'cell': (5, 7), 'value': Token.TWO},
            {'cell': (5, 8), 'value': Token.SIX},
            {'cell': (7, 7), 'value': Token.FOUR},
            {'cell': (7, 8), 'value': Token.ONE},
            {'cell': (8, 7), 'value': Token.FIVE},
            {'cell': (8, 8), 'value': Token.THREE},
        ])

        self.assertEqual(
            [cell.options for cell in puzzle_board.cells],
            [cell.options for cell in resolved_board.cells],
        )

