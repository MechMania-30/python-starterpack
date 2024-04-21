from strategy.bad_strategy import BadStrategy
from strategy.strategy import Strategy


def choose_strategy(team: int) -> Strategy:
    # Modify what is returned here to select the strategy your bot will use

    return BadStrategy(team)
