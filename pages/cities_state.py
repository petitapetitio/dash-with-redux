from enum import Enum

INITIAL_STATE = {"cities": []}


class Action(Enum): ...


def reduce(state: dict, action: Action, payload=None) -> dict:
    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
