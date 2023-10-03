import argparse

from sudoku.file_io import puzzle_loader, solution_loader
from sudoku import strategies, display
from sudoku.main import run_solver


parser = argparse.ArgumentParser(
    description = 'This program solves Sudoku puzzles',
)
parser.add_argument('puzzle_name', help = 'The puzzle identifier within the `puzzles` directory')
script_args = parser.parse_args()


print('Puzzle {}'.format(script_args.puzzle_name))
board = puzzle_loader(script_args.puzzle_name)
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

print('')
print('Marking')
solution = solution_loader(script_args.puzzle_name)
display.marking(board, solution)

