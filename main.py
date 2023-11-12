import argparse
from enum import Enum
import json
import os
import traceback
import sys

from network.client import Client
from network.received_message import ReceivedMessage, ReceivedMessagePhase
from strategy.choose_strategy import choose_strategy

raw_debug_env = os.environ.get("DEBUG")
DEBUG = raw_debug_env == "1" or raw_debug_env == "true"


# A argument parser that will also print help upon error
class HelpArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class RunOpponent(Enum):
    SELF = "self"
    HUMAN_COMPUTER = "humanComputer"
    ZOMBIE_COMPUTER = "zombieComputer"


COMMANDS_FOR_OPPONENT: dict[RunOpponent, list[tuple[str, str]]] = {
    RunOpponent.SELF: [
        ("Engine", "java -jar engine/engine.jar 9001 9002"),
        ("Human", "python main.py serve 9001"),
        ("Zombie", "python main.py serve 9002"),
    ],
    RunOpponent.HUMAN_COMPUTER: [
        ("Engine", "java -jar engine/engine.jar 0 9002"),
        ("Zombie", "python main.py serve 9002"),
    ],
    RunOpponent.ZOMBIE_COMPUTER: [
        ("Engine", "java -jar engine/engine.jar 9001 0"),
        ("Human", "python main.py serve 9001"),
    ],
}


def run(opponent: RunOpponent):
    raise NotImplementedError()


def serve(port: int):
    print(f"Connecting to server on port {port}...")

    client = Client(port)

    client.connect()

    print(f"Connected to server on port {port}")

    while True:
        raw_received = client.read()

        if raw_received:
            try:
                received = json.loads(raw_received)
                received_message = ReceivedMessage.deserialize(received)
                phase = received_message.phase
                data = received_message.data
                strategy = choose_strategy()

                if phase == ReceivedMessagePhase.HELLO_WORLD:
                    response = strategy.hello_world(data["message"])

                    response_str = json.dumps(response.serialize())

                    client.write(response_str)
                elif phase == ReceivedMessagePhase.PLANE_SELECT:
                    response = strategy.select_planes()

                    serialized_response = dict()

                    for type, count in response.items():
                        serialized_response[type.value] = count

                    response_str = json.dumps(serialized_response)

                    client.write(response_str)
                elif phase == ReceivedMessagePhase.FINISH:
                    print("Finished")

                    break
                else:
                    raise RuntimeError(f"Unknown phase type {phase}")

                if DEBUG:
                    print(f"Sent response to {phase} phase to server!")

            except Exception as e:
                print(f"Something went wrong running your bot: {e}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                client.write("null")


def main():
    parser = HelpArgumentParser(description="MechMania 30 bot runner")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    serve_parser = subparsers.add_parser(
        "serve",
        help="Serves your bot to an engine on the port passed, requires engine to be running there",
    )
    serve_parser.add_argument("port", type=int, help="Port to connect to")

    run_parser = subparsers.add_parser("run", help="Run your bot against an opponent")
    run_parser.add_argument(
        "opponent",
        choices=list(map(lambda opponent: opponent.value, list(RunOpponent))),
        help="Opponent to put your bot against, where self is your own bot or computer is against a simple computer bot",
    )

    args = parser.parse_args()

    # Match to a valid command
    if args.command == "serve":
        return serve(args.port)
    elif args.command == "run":
        for opponent in list(RunOpponent):
            if opponent.value == args.opponent:
                return run(opponent)

    # If no valid command, print help
    parser.print_help()


if __name__ == "__main__":
    main()
