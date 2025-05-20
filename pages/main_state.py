import urllib.parse
from enum import Enum, auto

import routes
from city import City

INITIAL_STATE = {
    "url": {
        "href": routes.CITIES,
        "base": "",
    },
    "cities": [],
}


class Action(Enum):
    SET_URL = auto()
    ADD_CITY = auto()


def reduce(state: dict, action: Action, payload=None) -> dict:
    print("main:reduce", action, payload, state)
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

    if action == Action.ADD_CITY:
        city: City = payload
        return state | {"cities": state["cities"] + [city.to_json()]}

    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
