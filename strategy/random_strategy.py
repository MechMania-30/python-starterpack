import random
from game.hello_world_response import HelloWorldResponse
from strategy.strategy import Strategy

class RandomStrategy(Strategy):
    def hello_world(self, message: str) -> HelloWorldResponse:
        return HelloWorldResponse(True)
