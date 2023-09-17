import argparse

from sudoku.structures import Board
from sudoku.file_io import puzzle_loader, solution_loader
from sudoku.strategies import resolve_singlets, resolve_doublets
from sudoku import display


parser = argparse.ArgumentParser(
    description = 'This program solves Sudoku puzzles',
)
parser.add_argument('puzzle_name', help = 'The puzzle identifier within the `puzzles` directory')
script_args = parser.parse_args()


print('Puzzle {}'.format(script_args.puzzle_name))
initial_values = puzzle_loader(script_args.puzzle_name)

board = Board()
board.set_puzzle(initial_values)
display.initial(board)
display.full_state(board)


# Solve
for i in range(0, 15):

    if board.is_solved:
        print('Round {}; Solution is complete'.format(i + 1))
        break

    # Resolve singlets
    num_singlets = resolve_singlets(board)
    print('Round {}; Found: {} singlet(s)'.format(i + 1, num_singlets))
    if num_singlets:
        continue

    # Resolve doublets
    num_doublets = resolve_doublets(board)
    print('Round {}; Found: {} doublet(s)'.format(i + 1, num_doublets))
    if num_doublets:
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

