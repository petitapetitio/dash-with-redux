import urllib.parse
from enum import Enum, auto

import routes

INITIAL_STATE = {"url": {"href": routes.CITIES}}


class Action(Enum):
    SET_URL = auto()


def reduce(state: dict, action: Action, payload=None) -> dict:
    print("main:reduce", action, payload)
    if action == Action.SET_URL:
        href: str = payload
        if href.startswith("/"):
            href = state["url"]["base"] + href

        url = urllib.parse.urlparse(href)

        return state | {
            "url": {
                "href": href,
                "base": f"{url.scheme}://{url.netloc}",
            }
        }
    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
