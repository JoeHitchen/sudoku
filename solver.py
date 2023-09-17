from sudoku.structures import Board
from sudoku.file_io import puzzle_loader, solution_loader
from sudoku.strategies import resolve_singlets, resolve_doublets
from sudoku import display

puzzle_name = 'puzzler_028'
print('Puzzle {}'.format(puzzle_name))
initial_values = puzzle_loader(puzzle_name)

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
solution = solution_loader(puzzle_name)
display.marking(board, solution)

