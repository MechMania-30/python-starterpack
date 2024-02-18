# This defines the general layout your strategy method will inherit. Do not edit this.

from game.plane import Plane, PlaneType
from game.hello_world_response import HelloWorldResponse


class Strategy:
    team: str

    def __init__(self, team: str) -> None:
        self.team = team
    
    def select_planes(self) -> dict[PlaneType, int]:
        '''
        Return a dictionary mapping PlaneType to int
        '''
        raise NotImplementedError("Must implement select_planes method!")

    def steer_input(self, planes: list[Plane]) -> dict[str, int]:
        '''
        Return a dictionary mapping each plane id to the amount they will steer [-1, 1], where positive is clockwise
        '''
        raise NotImplementedError("Must implement steer_input method!")
