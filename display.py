from structures import Board, Cell, Token, Solution


def print_with_grid(rows: list[str]) -> None:
    """Prints a 9x9 board with major grid lines"""
    print('┌───┬───┬───┐')
    for row_number, row in enumerate(rows, start = 1):
        print('│{}│{}│{}│'.format(row[0:3], row[3:6], row[6:9]))
        if row_number == 3 or row_number == 6:
            print('├───┼───┼───┤')
    print('└───┴───┴───┘')


def initial(board: Board) -> None:
    """Prints the initial board"""
    rows = [
        ''.join(str(cell.value) if cell.initial else '.'for cell in row)
        for row in board.rows
    ]
    print_with_grid(rows)


def solved(board: Board) -> None:
    """Prints the solved cells"""
    rows = [
        ''.join(str(cell.value) if cell.solved else '.'for cell in row)
        for row in board.rows
    ]
    print_with_grid(rows)


def full_state(board: Board) -> None:
    """Prints prints the full cell states with both major gridlines and minor columns"""

    print('╔═════════╤═════════╤═════════╦═════════╤═════════╤═════════╦═════════╤═════════╤═════════╗')  # noqa: E501
    for row_number, row in enumerate(board.rows, start = 1):
        cell_strs = []
        for cell in row:
            if cell.initial:
                cell_strs.append('   <{}>   '.format(cell.value))
            elif cell.solved:
                cell_strs.append('    {}    '.format(cell.value))
            else:
                cell_strs.append('')
                for token in Token:
                    cell_strs[-1] += str(token) if token in cell.options else '-'
        print('║{}│{}│{}║{}│{}│{}║{}│{}│{}║'.format(*cell_strs))
        if row_number == 3 or row_number == 6:
            print('╠═════════╪═════════╪═════════╬═════════╪═════════╪═════════╬═════════╪═════════╪═════════╣')  # noqa: E501
    print('╚═════════╧═════════╧═════════╩═════════╧═════════╧═════════╩═════════╧═════════╧═════════╝')  # noqa: E501


def marking(board: Board, solution: Solution) -> None:
    """Prints the marking of the solution"""

    def cell_result_marker(board_cell: Cell, solution_value: Token) -> str:
        correct = solution_value in board_cell.options
        if board_cell.initial:
            return '.' if correct else '@'
        if board_cell.solved:
            return 'Y' if correct else 'N'
        return 'y' if correct else 'n'

    row_results = []
    for board_row, solution_row in zip(board.rows, solution):
        result_markers = [cell_result_marker(board_row[i], solution_row[i]) for i in range(0, 9)]
        row_results.append(''.join(result_markers))
    print_with_grid(row_results)

