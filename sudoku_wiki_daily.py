from datetime import date
import argparse

from sudoku import sudoku_wiki_integrations
from sudoku.strategies import resolve_last_remaining, resolve_naked_pairs
from sudoku import display


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
for i in range(0, 15):

    if board.is_solved:
        print('Round {}; Solution is complete'.format(i + 1))
        break

    # Resolve last remaining
    num_last_remaining = resolve_last_remaining(board)
    print('Round {}; Found: {} last remaining cell(s)'.format(i + 1, num_last_remaining))
    if num_last_remaining:
        continue

    # Resolve naked pairs
    num_naked_pairs = resolve_naked_pairs(board)
    print('Round {}; Found: {} doublet(s)'.format(i + 1, num_naked_pairs))
    if num_naked_pairs:
        continue

    print('Round {}; Strategies exhausted'.format(i + 1))
    break



# Result Checking
print('')
print('Solution')
display.solved(board)

print('')
print('Marking')
solution = sudoku_wiki_integrations.daily_solution_reader(script_args.puzzle_date)
display.marking(board, solution)

