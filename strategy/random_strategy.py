import random
from game.hello_world_response import HelloWorldResponse
from strategy.strategy import Strategy
from game.plane import PlaneType

class RandomStrategy(Strategy):
    def hello_world(self, message: str) -> HelloWorldResponse:
        return HelloWorldResponse(True)
    
    def select_planes(self) -> dict[PlaneType, int]:
        return {PlaneType.BASIC: random.randint(5, 10)}
