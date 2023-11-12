# This defines the general layout your strategy method will inherit. Do not edit this.

from game.plane import PlaneType
from game.hello_world_response import HelloWorldResponse


class Strategy:
    def hello_world(self, message: str) -> HelloWorldResponse:
        """
        Test hello world method that should be deleted in the final release

        Return a hello world response
        """
        raise NotImplementedError("Must implement the decide_moves method!")
    
    def select_planes(self) -> dict[PlaneType, int]:
        '''
        Return a dictionary mapping PlaneType to int
        '''
        raise NotImplementedError("Must implement select_planes method!")
