# This defines the general layout your strategy method will inherit. Do not edit this.


from game.hello_world_response import HelloWorldResponse
from game.plane import PlaneType


class Strategy:
    def hello_world(self, message: str) -> HelloWorldResponse:
        """
        Test hello world method that should be deleted in the final release

        Return a hello world response
        """
        raise NotImplementedError("Must implement the decide_moves method!")
    
    def select_planes(self) -> list[dict[str, int]]:
        selected_planes = []
        '''
        Return a list of dictionaries of counts of selected plane types
        '''
        return selected_planes
