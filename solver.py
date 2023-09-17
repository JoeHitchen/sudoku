from sudoku.file_io import puzzle_loader, solution_loader
from sudoku.structures import Board, Cell, Token
from sudoku import display

puzzle_name = 'puzzler_028'
print('Puzzle {}'.format(puzzle_name))
initial_values = puzzle_loader(puzzle_name)

board = Board()
board.set_puzzle(initial_values)
display.initial(board)
display.full_state(board)


# Solve
def resolve_singlets(board: Board) -> int:
    """A singlet is a the only cell in a group which can take a specific value, so must do so."""

    singlets: set[tuple[Cell, Token]] = set()
    for grouping in board.all_groups:
        for token in Token:
            possible_cells = []
            for cell in grouping:
                if not cell.solved and token in cell.options:
                    possible_cells.append(cell)

            if len(possible_cells) == 1:
                singlets.add((possible_cells[0], token))

    for singlet in singlets:
        singlet[0].solve(singlet[1])

    return len(singlets)


def resolve_doublets(board: Board) -> int:
    """A doublet is a pair of cells within a grouping which both only take the same pair of values.
    Since these two cells MUST take these values, they are excluded from other cells in the group.

    This method implicity checks for triplets and higher order combinations too.
    """

    def options_key(options: set[Token]) -> str:
        return ''.join(str(token) for token in options)

    doublets: list[tuple[list[Cell], list[Cell]]] = []
    for group in board.all_groups:

        cell_options_map: dict[str, list[Cell]] = {}
        for cell in group:
            if cell.solved:
                continue

            cell_options_map_key = options_key(cell.options)
            if cell_options_map_key not in cell_options_map:
                cell_options_map[cell_options_map_key] = []
            cell_options_map[cell_options_map_key].append(cell)

        doublets.extend(
            (doublet, group)
            for options, doublet in cell_options_map.items()
            if len(doublet) == len(options)  # Length 1 sets should be disallowed by 'solved' check
        )

    for doublet, group in doublets:
        for cell in group:
            if cell in doublet or cell.solved:
                continue
            for value in doublet[0].options:
                cell.exclude(value)

    return len(doublets)


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

