import argparse

from sudoku.file_io import puzzle_loader, solution_loader
from sudoku import strategies, display


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
previous_last_remaining: list[strategies.LastRemaining] = []
previous_naked_pairs: list[strategies.NakedPair] = []
previous_intersections: list[strategies.Intersection] = []
previous_y_wings: list[strategies.YWing] = []
for i in range(0, 15):

    if board.is_solved:
        print('Round {}; Solution is complete'.format(i + 1))
        break

    # Resolve last remaining
    last_remaining = strategies.resolve_last_remaining(board)
    print('Round {}; Found: {} last remaining cell(s)'.format(i + 1, len(last_remaining)))
    if last_remaining and not last_remaining == previous_last_remaining:
        previous_last_remaining = last_remaining
        continue
    previous_last_remaining = last_remaining

    # Resolve naked pairs
    naked_pairs = strategies.resolve_naked_pairs(board)
    print('Round {}; Found: {} naked pair(s)'.format(i + 1, len(naked_pairs)))
    if naked_pairs and not naked_pairs == previous_naked_pairs:
        previous_naked_pairs = naked_pairs
        continue
    previous_naked_pairs = naked_pairs

    # Resolve intersections
    intersections = strategies.resolve_intersections(board)
    print('Round {}; Found: {} intersection(s)'.format(i + 1, len(intersections)))
    if intersections and not intersections == previous_intersections:
        previous_intersections = intersections
        continue
    previous_intersections = intersections

    # Resolve Y-wings
    y_wings = strategies.resolve_y_wings(board)
    print('Round {}; Found: {} y-wing(s)'.format(i + 1, len(y_wings)))
    if y_wings and not y_wings == previous_y_wings:
        previous_y_wings = y_wings
        continue
    previous_y_wings = y_wings

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

