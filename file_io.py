import json

from structures import Token, Solution, KnownCells


def puzzle_loader(puzzle_name: str) -> list[KnownCells]:
    with open('puzzles/{}_puzzle.json'.format(puzzle_name)) as file:
        raw = json.load(file)

    known_cells: list[KnownCells] = []
    for i, row in enumerate(raw):
        for j, cell in enumerate(row):
            if cell == '.':
                continue
            known_cells.append({'cell': (i + 1, j + 1), 'value': Token(cell)})

    return known_cells


def solution_loader(puzzle_name: str) -> Solution:
    with open('puzzles/{}_solution.json'.format(puzzle_name)) as file:
        raw = json.load(file)

    return [[Token(cell) for cell in row] for row in raw]

