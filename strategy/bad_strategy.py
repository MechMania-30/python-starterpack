import random
from game.hello_world_response import HelloWorldResponse
from strategy.strategy import Strategy
from game.plane import Plane, PlaneType

class BadStrategy(Strategy):
    my_counter = 0
    my_steers = dict()
    
    def select_planes(self) -> dict[PlaneType, int]:
        return {PlaneType.BASIC: random.randint(5, 10)}
    
    def steer_input(self, planes: dict[str, Plane]) -> dict[str, int]:
        response = dict()

        print(planes)

        for id, plane in planes.items():
            if plane.team != self.team:
                continue

            if self.my_counter < 5:
                response[id] = 0
            else:
                if id not in self.my_steers:
                    self.my_steers[id] = random.random() * 2 - 1
                response[id] = self.my_steers[id]


        self.my_counter += 1

        return response
