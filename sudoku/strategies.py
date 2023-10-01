from .structures import Board, Cell, Token


LastRemaining = tuple[Cell, Token]
NakedPair = tuple[list[Cell], list[Cell]]


def resolve_last_remaining(board: Board) -> list[LastRemaining]:
    """A cell that is the only cell in a group which can still take a given value must do so."""

    last_remaining_cells: list[LastRemaining] = []
    for grouping in board.all_groups:
        for token in Token:
            possible_cells = []
            for cell in grouping:
                if not cell.solved and token in cell.options:
                    possible_cells.append(cell)

            if len(possible_cells) == 1:
                last_remaining_cells.append((possible_cells[0], token))

    for last_remaining_cell in last_remaining_cells:
        last_remaining_cell[0].solve(last_remaining_cell[1])

    return last_remaining_cells


def resolve_naked_pairs(board: Board) -> list[NakedPair]:
    """A naked pair is a pair of cells which can only take the same two values.
    Since these two cells MUST take these values, they are excluded from other cells in the group.

    This method implicity checks for triplets and higher order combinations that take exactly the
    same set of numbers. It does not perform a full check for naked triples/quads with differing
    sets of numbers in the cells.
    """

    def options_key(options: set[Token]) -> str:
        return ''.join(str(token) for token in options)

    naked_pairs: list[NakedPair] = []
    for group in board.all_groups:

        cell_options_map: dict[str, list[Cell]] = {}
        for cell in group:
            if cell.solved:
                continue

            cell_options_map_key = options_key(cell.options)
            if cell_options_map_key not in cell_options_map:
                cell_options_map[cell_options_map_key] = []
            cell_options_map[cell_options_map_key].append(cell)

        naked_pairs.extend(
            (option_pairing, group)
            for options, option_pairing in cell_options_map.items()
            if len(option_pairing) == len(options)
        )

    for option_pairing, group in naked_pairs:
        for cell in group:
            if cell in option_pairing or cell.solved:
                continue
            for value in option_pairing[0].options:
                cell.exclude(value)

    return naked_pairs

