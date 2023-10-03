from datetime import date
import argparse

from sudoku import sudoku_wiki_integrations
from sudoku import strategies, display
from sudoku.main import run_solver


parser = argparse.ArgumentParser(
    description = 'This program solves the Sudoku Wiki Daily puzzles',
)
parser.add_argument(
    'puzzle_date',
    type = lambda d: date.fromisoformat(d),
    help = 'The date of the puzzle to be solved',
)
script_args = parser.parse_args()

board = sudoku_wiki_integrations.daily_puzzle_reader(script_args.puzzle_date)
display.initial(board)
display.full_state(board)


# Solve
strategies_to_run: list[strategies.StrategyFunction] = [
    strategies.resolve_last_remaining,
    strategies.resolve_naked_pairs,
    strategies.resolve_intersections,
    strategies.resolve_y_wings,
]
run_solver(board, strategies_to_run)


# Result Checking
print('')
print('Solution')
display.solved(board)
display.full_state(board)

print('')
print('Marking')
solution = sudoku_wiki_integrations.daily_solution_reader(script_args.puzzle_date)
display.marking(board, solution)

