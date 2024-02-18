from dataclasses import dataclass
from enum import Enum

@dataclass
class Position:
    x: float
    y: float

    def deserialize(blob: object) -> "Position":
        try:
            pos = Position(blob["x"], blob["y"])
        except:
            print("Failed to validate plane json")
            raise

        return pos

class PlaneType(Enum):
    BASIC = "BASIC"

@dataclass
class Plane:
    id: str
    team: str
    type: PlaneType
    position: Position
    angle: float

    def deserialize(blob: object) -> "Plane":
        try:
            plane = Plane(
                blob["id"],
                blob["team"],
                PlaneType[blob["type"]],
                Position.deserialize(blob["position"]),
                blob["angle"]
            )
        except:
            print("Failed to validate plane json")
            raise

        return plane
