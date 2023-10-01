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

    def test__y_wings__row_column(self) -> None:

        puzzle_board = Board()
        puzzle_board.set_puzzle([
            {'cell': (1, 5), 'value': Token.ONE},
            {'cell': (1, 9), 'value': Token.SEVEN},
            {'cell': (2, 5), 'value': Token.TWO},
            {'cell': (3, 5), 'value': Token.THREE},
            {'cell': (4, 7), 'value': Token.TWO},
            {'cell': (4, 8), 'value': Token.THREE},
            {'cell': (4, 9), 'value': Token.NINE},
            {'cell': (5, 1), 'value': Token.FOUR},
            {'cell': (5, 2), 'value': Token.FIVE},
            {'cell': (5, 3), 'value': Token.SIX},
            {'cell': (4, 4), 'value': Token.SEVEN},
            {'cell': (7, 4), 'value': Token.FIVE},
            {'cell': (7, 7), 'value': Token.EIGHT},
            {'cell': (7, 8), 'value': Token.TWO},
            {'cell': (7, 9), 'value': Token.SIX},
            {'cell': (8, 4), 'value': Token.SIX},
            {'cell': (8, 7), 'value': Token.THREE},
            {'cell': (9, 1), 'value': Token.SEVEN},
            {'cell': (9, 4), 'value': Token.NINE},
            {'cell': (9, 7), 'value': Token.FIVE},
        ])

        y_wings = strategies.resolve_y_wings(puzzle_board)

        target_y_wing = (puzzle_board.cells[80], puzzle_board.cells[44], puzzle_board.cells[76])
        self.assertEqual(y_wings, [(target_y_wing, Token.EIGHT)])

        resolved_board = Board()
        resolved_board.set_puzzle([
            {'cell': (1, 5), 'value': Token.ONE},
            {'cell': (1, 9), 'value': Token.SEVEN},
            {'cell': (2, 5), 'value': Token.TWO},
            {'cell': (3, 5), 'value': Token.THREE},
            {'cell': (4, 7), 'value': Token.TWO},
            {'cell': (4, 8), 'value': Token.THREE},
            {'cell': (4, 9), 'value': Token.NINE},
            {'cell': (5, 1), 'value': Token.FOUR},
            {'cell': (5, 2), 'value': Token.FIVE},
            {'cell': (5, 3), 'value': Token.SIX},
            {'cell': (5, 5), 'value': Token.NINE},
            {'cell': (4, 4), 'value': Token.SEVEN},
            {'cell': (7, 4), 'value': Token.FIVE},
            {'cell': (7, 7), 'value': Token.EIGHT},
            {'cell': (7, 8), 'value': Token.TWO},
            {'cell': (7, 9), 'value': Token.SIX},
            {'cell': (8, 4), 'value': Token.SIX},
            {'cell': (8, 7), 'value': Token.THREE},
            {'cell': (9, 1), 'value': Token.SEVEN},
            {'cell': (9, 4), 'value': Token.NINE},
            {'cell': (9, 7), 'value': Token.FIVE},
        ])

        self.assertEqual(
            [cell.options for cell in puzzle_board.cells],
            [cell.options for cell in resolved_board.cells],
        )

    def test__y_wings__squares(self) -> None:

        puzzle_board = Board()
        puzzle_board.set_puzzle([
            {'cell': (1, 1), 'value': Token.SEVEN},
            {'cell': (1, 2), 'value': Token.NINE},
            {'cell': (1, 5), 'value': Token.FIVE},
            {'cell': (1, 6), 'value': Token.EIGHT},
            {'cell': (2, 1), 'value': Token.EIGHT},
            {'cell': (2, 4), 'value': Token.SIX},
            {'cell': (2, 6), 'value': Token.NINE},
            {'cell': (3, 2), 'value': Token.FIVE},
            {'cell': (3, 3), 'value': Token.SIX},
            {'cell': (3, 6), 'value': Token.SEVEN},
            {'cell': (5, 3), 'value': Token.TWO},
            {'cell': (5, 4), 'value': Token.ONE},
            {'cell': (6, 3), 'value': Token.FOUR},
            {'cell': (6, 4), 'value': Token.TWO},
            {'cell': (8, 2), 'value': Token.THREE},
            {'cell': (8, 5), 'value': Token.FOUR},
            {'cell': (9, 2), 'value': Token.FOUR},
            {'cell': (9, 5), 'value': Token.ONE},
        ])

        y_wings = strategies.resolve_y_wings(puzzle_board)

        target_y_wing_1 = (puzzle_board.cells[10], puzzle_board.cells[2], puzzle_board.cells[13])
        target_y_wing_2 = (puzzle_board.cells[10], puzzle_board.cells[11], puzzle_board.cells[13])
        target_y_wing_3 = (puzzle_board.cells[11], puzzle_board.cells[10], puzzle_board.cells[13])
        target_y_wing_4 = (puzzle_board.cells[13], puzzle_board.cells[10], puzzle_board.cells[11])
        self.assertEqual(
            y_wings,
            [
                (target_y_wing_1, Token.THREE),
                (target_y_wing_2, Token.THREE),
                (target_y_wing_3, Token.TWO),
                (target_y_wing_4, Token.ONE),
            ],
        )

        resolved_board = Board()
        resolved_board.set_puzzle([
            {'cell': (1, 1), 'value': Token.SEVEN},
            {'cell': (1, 2), 'value': Token.NINE},
            {'cell': (1, 5), 'value': Token.FIVE},
            {'cell': (1, 6), 'value': Token.EIGHT},
            {'cell': (2, 1), 'value': Token.EIGHT},
            {'cell': (2, 2), 'value': Token.TWO},
            {'cell': (2, 4), 'value': Token.SIX},
            {'cell': (2, 6), 'value': Token.NINE},
            {'cell': (3, 2), 'value': Token.FIVE},
            {'cell': (3, 3), 'value': Token.SIX},
            {'cell': (3, 6), 'value': Token.SEVEN},
            {'cell': (5, 3), 'value': Token.TWO},
            {'cell': (5, 4), 'value': Token.ONE},
            {'cell': (6, 3), 'value': Token.FOUR},
            {'cell': (6, 4), 'value': Token.TWO},
            {'cell': (8, 2), 'value': Token.THREE},
            {'cell': (8, 5), 'value': Token.FOUR},
            {'cell': (9, 2), 'value': Token.FOUR},
            {'cell': (9, 5), 'value': Token.ONE},
        ])

        self.assertEqual(
            [cell.options for cell in puzzle_board.cells],
            [cell.options for cell in resolved_board.cells],
        )

