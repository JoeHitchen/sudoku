import json

from .structures import Board, Token, KnownCells


def puzzle_loader(puzzle_name: str) -> Board:
    with open('puzzles/{}_puzzle.json'.format(puzzle_name)) as file:
        raw = json.load(file)

    known_cells: list[KnownCells] = []
    for i, row in enumerate(raw):
        for j, cell in enumerate(row):
            if cell == '.':
                continue
            known_cells.append({'cell': (i + 1, j + 1), 'value': Token(cell)})

    board = Board()
    board.set_puzzle(known_cells)
    return board


def solution_loader(puzzle_name: str) -> Board:
    with open('puzzles/{}_solution.json'.format(puzzle_name)) as file:
        raw = json.load(file)

    solution: list[KnownCells] = []
    for row_number, row in enumerate(raw, start = 1):
        for column_number, value in enumerate(row, start = 1):
            solution.append({'cell': (row_number, column_number), 'value': Token(value)})

    board = Board()
    board.set_puzzle(solution)
    return board

