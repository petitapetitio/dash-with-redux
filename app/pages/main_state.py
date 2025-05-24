import urllib.parse
from enum import Enum, auto

from app import routes
from app.city import City

INITIAL_STATE = {
    "url": {
        "href": routes.CITIES,
        "base": "",
    },
    "cities": [],
    "toast": {
        "visible": False,
        "content": "",
    },
}


class Action(Enum):
    SET_URL = auto()
    ADD_CITY = auto()

    OPEN_TOAST = auto()
    CLOSE_TOAST = auto()


def reduce(state: dict, action: Action, payload=None) -> dict:
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
        return state | {"cities": state["cities"] + [city.to_dict()]}

    if action == Action.OPEN_TOAST:
        return state | {
            "toast": {
                "visible": True,
                "content": payload,
            },
        }

    if action == Action.CLOSE_TOAST:

        return state | {
            "toast": {
                "visible": False,
                "content": "",
            },
        }

    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
