import argparse

from sudoku.file_io import puzzle_loader, solution_loader
from sudoku.strategies import resolve_last_remaining, resolve_naked_pairs
from sudoku import display


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
solution = solution_loader(script_args.puzzle_name)
display.marking(board, solution)

