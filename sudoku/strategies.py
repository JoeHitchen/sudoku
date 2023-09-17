from .structures import Board, Cell, Token


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

