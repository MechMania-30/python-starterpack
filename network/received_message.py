from dataclasses import dataclass
from enum import Enum


class ReceivedMessagePhase(Enum):
    PLANE_SELECT = "PLANE_SELECT"
    HELLO_WORLD = "HELLO_WORLD"
    INPUT = "INPUT"
    FINISH = "FINISH"


@dataclass
class ReceivedMessage:
    phase: ReceivedMessagePhase
    data: object

    def deserialize(blob: object) -> "ReceivedMessage":
        try:
            message = ReceivedMessage(ReceivedMessagePhase[blob["phase"]], blob["data"])
        except:
            print("Failed to validate ReceivedMessage json")
            raise

        return message
