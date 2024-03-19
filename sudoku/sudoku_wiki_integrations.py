from datetime import date
from xml.etree import ElementTree
import html

import requests

from .structures import Board, Token, KnownCell
from . import file_io


DAILY_TEMPLATE_URL = 'https://www.sudokuwiki.org/Print/Print_Daily_Sudoku.aspx?day={}{}'


def puzzle_number_from_date(date: date) -> int:
    return (date - date.fromisoformat('2008-01-01')).days


def puzzle_name_from_date(date: date) -> str:
    """Generates the puzzle name for a given date."""
    return 'wiki_daily_{}'.format(puzzle_number_from_date(date))


def daily_puzzle_reader(date: date) -> Board:
    """Loads the Sudoku Wiki Daily Puzzle for a given date, using a local cache if possible."""

    puzzle_number = puzzle_number_from_date(date)
    puzzle_name = puzzle_name_from_date(date)
    puzzle_string = 'Sudoku Wiki Daily Puzzle #{} ({})'.format(puzzle_number, date)

    try:
        puzzle = file_io.puzzle_loader(puzzle_name)
        print(f'Loaded {puzzle_string} from cache')

    except FileNotFoundError:
        puzzle = _daily_reader(DAILY_TEMPLATE_URL.format(date, ''))
        print(f'Retrieved {puzzle_string} from site')

        file_io.puzzle_writer(puzzle_name, puzzle)

    return puzzle


def daily_solution_reader(date: date) -> Board:
    """Retrieves the solution to the daily puzzle for a given date."""

    puzzle_number = puzzle_number_from_date(date)
    puzzle_name = puzzle_name_from_date(date)
    puzzle_string = 'Sudoku Wiki Daily Solution #{} ({})'.format(puzzle_number, date)

    try:
        solution = file_io.solution_loader(puzzle_name)
        print(f'Loaded {puzzle_string} from cache')

    except FileNotFoundError:
        solution = _daily_reader(DAILY_TEMPLATE_URL.format(date, '&solution=please'))
        print(f'Retrieved {puzzle_string} from site'.format())

        file_io.solution_writer(puzzle_name, solution)

    return solution


def _daily_reader(url: str) -> Board:
    """Performs the puzzle/solution retrieval and conversion."""

    response = requests.get(url)
    if not response.ok:
        response.raise_for_status()

    start_index = 67
    puzzle_string = ''.join(response.text.split('\r\n')[start_index:start_index + 102])
    puzzle_string = html.unescape(puzzle_string)
    puzzle_table = ElementTree.fromstring(puzzle_string)

    puzzle_cells: list[KnownCell] = []
    for i, row in enumerate(puzzle_table, start = 1):
        for j, cell in enumerate(row, start = 1):
            try:
                assert cell.text
                token = Token(cell.text)
                puzzle_cells.append({'cell': (i, j), 'value': token})
            except ValueError:
                continue

    board = Board()
    board.set_puzzle(puzzle_cells)
    return board

