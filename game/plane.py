from dataclasses import dataclass
from enum import Enum

from game.plane_data import PLANE_TYPE_TO_STATS, PlaneStats, PlaneType, Position

@dataclass
class Plane:
    id: str
    team: str
    type: PlaneType
    position: Position
    angle: float
    health: int
    stats: PlaneStats

    def deserialize(blob: object) -> "Plane":
        try:
            plane = Plane(
                blob["id"],
                blob["team"],
                PlaneType[blob["type"]],
                Position.deserialize(blob["position"]),
                blob["angle"],
                blob["health"],
                PLANE_TYPE_TO_STATS[PlaneType[blob["type"]]]
            )
        except:
            print("Failed to validate plane json")
            raise

        return plane
