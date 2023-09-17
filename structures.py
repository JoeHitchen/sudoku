from typing import TypedDict, Self
from math import floor
from enum import Enum


Solution = list[list['Token']]


class KnownCells(TypedDict):
    cell: tuple[int, int]
    value: 'Token'


class Token(Enum):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'

    def __str__(self) -> str:
        return self.value


class Cell():

    def __init__(self, row: list[Self], column: list[Self], square: list[Self]):

        self.row = row; row.append(self)  # noqa: E702
        self.column = column; column.append(self)  # noqa: E702
        self.square = square; square.append(self)  # noqa: E702

        self.solved = False
        self.initial = False
        self.options = set(Token)


    @property
    def value(self) -> Token | None:
        return list(self.options)[0] if self.solved else None


    def solve(self, value: Token, initial: bool = False) -> None:
        """Resolve a cell to a single value"""

        assert value in self.options

        self.solved = True
        self.initial = initial
        self.options = self.options.intersection({value})

        for cell in [*self.row, *self.column, *self.square]:
            if cell is not self and not cell.solved:
                cell.exclude(value)


    def exclude(self, value: Token) -> None:
        """Remove a specific value from the possibilities for a cell"""

        self.options.discard(value)
        if len(self.options) == 1:
            self.solve(list(self.options)[0])



class Board():

    def __init__(self) -> None:

        def square_index(row_number: int, column_number: int) -> int:
            return 3 * floor((row_number - 1) / 3) + floor((column_number - 1) / 3)

        self.cells: list[Cell] = []
        self.rows: list[list[Cell]] = [[] for _ in range(1, 10)]
        self.columns: list[list[Cell]] = [[] for _ in range(1, 10)]
        self.squares: list[list[Cell]] = [[] for _ in range(1, 10)]

        for row_number, row in enumerate(self.rows, start = 1):
            for column_number, column, in enumerate(self.columns, start = 1):
                self.cells.append(Cell(
                    row = row,
                    column = column,
                    square = self.squares[square_index(row_number, column_number)],
                ))

    @property
    def all_groups(self) -> list[list[Cell]]:
        """The collection of all possible groups"""
        return [*self.rows, *self.columns, *self.squares]

    def set_puzzle(self, initial_values: list[KnownCells]) -> None:
        """Adds known values from the puzzle selection to the board"""

        def cell_index(row_number: int, column_number: int) -> int:
            return 9 * (row_number - 1) + column_number - 1

        for initial_value in initial_values:
            active_index = cell_index(*initial_value['cell'])
            self.cells[active_index].solve(initial_value['value'], initial = True)


    @property
    def is_solved(self) -> bool:
        """Indicates if the board has been solved without error"""

        if not all(cell.solved for cell in self.cells):
            return False

        all_tokens = set(Token)
        for group in self.all_groups:
            if {cell.value for cell in group} != all_tokens:
                return False

        return True


