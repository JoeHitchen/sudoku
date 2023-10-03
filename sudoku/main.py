from .structures import Board
from .import strategies


def run_solver(board: Board, strategies_to_run: list[strategies.StrategyFunction]) -> None:

    previous_outputs: dict[str, list[strategies.StrategyOutput]] = {
        strategy.__name__: [] for strategy in strategies_to_run
    }
    for round in range(1, 16):

        if board.is_solved:
            print('Round {}; Solution is complete'.format(round))
            break

        for strategy in strategies_to_run:
            output = strategy(board)
            output_changed = output == previous_outputs[strategy.__name__]
            previous_outputs[strategy.__name__]

            print('Round {}; Found: {} {}(s){}'.format(
                round,
                len(output),
                strategies.tags[strategy.__name__],
                '' if output_changed else '--> Unchanged',
            ))
            if output and not output_changed:
                break

