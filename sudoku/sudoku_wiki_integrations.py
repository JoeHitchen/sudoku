from datetime import date
from xml.etree import ElementTree
import html

import requests

from .structures import Board, Token, KnownCell


DAILY_TEMPLATE_URL = 'https://www.sudokuwiki.org/Print/Print_Daily_Sudoku.aspx?day={}{}'


def puzzle_name_from_date(date: date) -> str:
    """Generates the puzzle name for a given date."""
    return 'wiki_daily_{}'.format((date - date.fromisoformat('2008-01-01')).days)


def daily_puzzle_reader(date: date) -> Board:
    """Retrieves the daily puzzle for a given date."""
    return _daily_reader(DAILY_TEMPLATE_URL.format(date, ''))


def daily_solution_reader(date: date) -> Board:
    """Retrieves the solution to the daily puzzle for a given date."""
    return _daily_reader(DAILY_TEMPLATE_URL.format(date, '&solution=please'))


def _daily_reader(url: str) -> Board:
    """Performs the puzzle/solution retrieval and conversion."""

    response = requests.get(url)
    if not response.ok:
        response.raise_for_status()

    puzzle_string = ''.join(response.text.split('\r\n')[66:168])
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

