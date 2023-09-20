# Sudoku Solver
A tool for solving Sudoku puzzles using constraint programming.

The constraint satisfaction method initially assumes that all cells can take any value.
As the puzzles cells are added, the constraints these cells introduce are propagated and the possibilities for remaining cells are reduced.
If at any point a cell has only one possibility left, then it can be solved and that new information propagated to all connected cells.

Once all the puzzle cells are placed, the solver iterates through various strategies to solve or further restrict cells.
When applying a strategy, the solver searches all possible applications of that strategy and then applies all the newly devised constraints/resolutions afterwards.
The strategies to be used are ordered, and the solver will only attempt a later (and implicitly, more complicated) strategy if earlier strategies have not yielded results.
If any strategy updates the board, the solver will break and start a new iteration with the first (and simplest) method.

## Strategies
1. **Naked Singles** are cells with only one possibility remaining, and the solver will immediately resolve naked singles when a cell becomes one, regardless of other strategies being pursued at the time.
1. **Last Remaining** cells are the only cell in a grouping which can still take a given value, and so must be resolved to that value.
1. **Naked Pairs** are pairs of cells within one grouping which can only take the same two values.
  Since these two cells must take both these values, these values can be removed from other cells in the same grouping.

If you have an example of a puzzle which cannot be solved with the current strategies, please raise an issue with the puzzle specification, since identifying these gaps will be the biggest motivator for further work on this project.

## How to Use
To use the solver, you need to place a JSON puzzle definition file in the `puzzles` directory with the `_puzzle` suffix (e.g. `puzzles/mysudoku_puzzle.json`).
The file contents should be a list of strings containing the known numbers or a `.` to indicate an unknown cell.
```
[
  "53..7....",
  "6..195...",
  ".98....6.",
  "8...6...3",
  "4..8.3..1",
  "7...2...6",
  ".6....28.",
  "...419..5",
  "....8..79"
]
```
With the puzzle file in place, the solver can be invoked using the name of the puzzle provided in the filename, e.g.
```
python solver.py mysudoku
```
If the solution is known, then it can be provided the same way as a puzzle but with the `_solution` suffix, and the output of the solver will be compared against it for accuracy.
When marking a solution like this, the following code is used:
* `Y` - A correctly solved cell
* `N` - An incorrectly solved cell
* `y` - A cell not solved, but still permitting the correct answer
* `n` - A cell not solved and not still permitting the correct answer
* `.` - A puzzle cell matching the solution
* `@` - A puzzle cell which does NOT match the solution


## Future Directions
* Expanding the range of strategies that can be applied - https://www.sudokuwiki.org/Strategy_Families is a detailed guide
* Idenfying a rights-free source of Sudoku puzzles to test the algorithm against harder puzzles.
* Generalising to varitions on the standard Sudoku puzzle.

