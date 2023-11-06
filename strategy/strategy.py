# This defines the general layout your strategy method will inherit. Do not edit this.


from game.hello_world_response import HelloWorldResponse
from game.plane_type import PlaneType
from typing import Dict


class Strategy:
    def select_planes(self) -> Dict[str, int]: # str: plane_type, int: count
        selected_planes = {}
        # Logic for player to select planes
        # Sample choice
        ''' 
        selected_planes = {
            PlaneType.BASIC: 10,
        }
        '''
        return selected_planes
    
    def hello_world(self, message: str) -> HelloWorldResponse:
        """
        Test hello world method that should be deleted in the final release

        Return a hello world response
        """
        raise NotImplementedError("Must implement the decide_moves method!")