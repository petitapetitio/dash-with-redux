from enum import Enum, auto

INITIAL_STATE = {
    "country": None,
    "city-dropdown": {
        "options": [],
        "value": None,
        "disabled": True,
    },
    "city-id": None,
    "population": "",
    "comment": "",
    "submit-button": {
        "disabled": True,
    },
    "visualize-button": {
        "disabled": True,
    },
}

CITIES_BY_COUNTRY = {
    "France": ["Paris", "Lyon", "Marseille"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Japan": ["Tokyo", "Kyoto", "Osaka"],
}


class Action(Enum):
    SET_CITY_ID = auto()
    SELECT_COUNTRY = auto()
    SELECT_CITY = auto()
    SET_POPULATION = auto()
    SET_COMMENT = auto()


def reduce(state: dict, action: Action, payload=None) -> dict:
    if action == Action.SELECT_COUNTRY:
        country = payload
        if country == state["country"]:
            return state

        cities = CITIES_BY_COUNTRY[country]
        return state | {
            "country": country,
            "city-dropdown": {
                "options": [{"label": city, "value": city} for city in cities],
                "value": None,
                "disabled": False,
            },
        }
    if action == Action.SELECT_CITY:
        return state | {
            "city-dropdown": {
                **state["city-dropdown"],
                "value": payload,
            },
            "submit-button": {
                "disabled": False,
            },
            "visualize-button": {
                "disabled": False,
            },
        }

    if action == Action.SET_CITY_ID:
        return state | {"city_id": payload}

    if action == Action.SET_POPULATION:
        return state | {"population": payload}

    if action == Action.SET_COMMENT:
        return state | {"comment": payload}

    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
