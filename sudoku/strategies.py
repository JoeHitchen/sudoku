from typing import Callable

from .structures import Board, Cell, Token


LastRemaining = tuple[Cell, Token]
NakedPair = tuple[list[Cell], list[Cell]]
Intersection = tuple[list[Cell], Token, list[Cell]]
YWing = tuple[tuple[Cell, Cell, Cell], Token]

StrategyOutput = LastRemaining | NakedPair | Intersection | YWing
StrategyFunction = (
    Callable[[Board], list[LastRemaining]]
    | Callable[[Board], list[NakedPair]]
    | Callable[[Board], list[Intersection]]
    | Callable[[Board], list[YWing]]
)


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


def resolve_intersections(board: Board) -> list[Intersection]:

    intersections: list[Intersection] = []

    for group in board.all_groups:

        token_locations_map: dict[Token, list[Cell]] = {token: [] for token in Token}

        for cell in group:
            if cell.solved:
                continue
            for token in cell.options:
                token_locations_map[token].append(cell)

        token_locations_map = {
            token: locations
            for token, locations in token_locations_map.items()
            if len(locations) > 1
        }

        for token, locations in token_locations_map.items():

            row = locations[0].row if locations[0].row != group else None
            column = locations[0].column if locations[0].column != group else None
            square = locations[0].square if locations[0].square != group else None

            for cell in locations[1:]:
                if row and not cell.row == row:
                    row = None
                if column and not cell.column == column:
                    column = None
                if square and not cell.square == square:
                    square = None

            if row:
                intersections.append((locations, token, row))
            if column:
                intersections.append((locations, token, column))
            if square:
                intersections.append((locations, token, square))


    for main_cells, value, target_cells in intersections:
        for target_cell in target_cells:
            if target_cell not in main_cells:
                target_cell.exclude(value)

    return intersections


def resolve_y_wings(board: Board) -> list[YWing]:

    two_option_cells = [cell for cell in board.cells if len(cell.options) == 2]

    y_wings: list[YWing] = []

    for pivot in two_option_cells:
        for index, branch_1 in enumerate(two_option_cells[:-1]):

            if branch_1 == pivot:
                continue

            if not (
                branch_1.row == pivot.row
                or branch_1.column == pivot.column
                or branch_1.square == pivot.square
            ):
                continue

            intersect_pivot_1 = branch_1.options.intersection(pivot.options)
            if not len(intersect_pivot_1) == 1:
                continue

            for branch_2 in two_option_cells[index + 1:]:

                if branch_2 == pivot or branch_2 == branch_1:
                    continue

                if not (
                    branch_2.row == pivot.row
                    or branch_2.column == pivot.column
                    or branch_2.square == pivot.square
                ):
                    continue

                intersect_pivot_2 = branch_2.options.intersection(pivot.options)
                if not len(intersect_pivot_2) == 1:
                    continue

                intersect_1_2 = branch_2.options.intersection(branch_1.options)
                if not len(intersect_1_2) == 1:
                    continue

                if intersect_pivot_1 == intersect_pivot_2:
                    continue

                if ((pivot, branch_2, branch_1), list(intersect_1_2)[0]) in y_wings:
                    continue

                y_wings.append(((pivot, branch_1, branch_2), list(intersect_1_2)[0]))


    for y_wing, token in y_wings:

        branch_1 = y_wing[1]
        branch_2 = y_wing[2]
        branch_2_cover = [*branch_2.row, *branch_2.column, *branch_2.square]
        for cell in [*branch_1.row, *branch_1.column, *branch_1.square]:
            if cell in y_wing:
                continue
            if cell not in branch_2_cover:
                continue
            cell.exclude(token)

    return y_wings


tags = {
    resolve_last_remaining.__name__: 'last remaining cell',
    resolve_naked_pairs.__name__: 'naked pair',
    resolve_intersections.__name__: 'intersection',
    resolve_y_wings.__name__: 'y-wing',
}

