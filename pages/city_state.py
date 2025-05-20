from enum import Enum, auto

INITIAL_STATE = {
    # DISPLAY_RESULT needs to know the selected country.
    # It's easy to persist the value provided by Action.SELECT_COUNTRY
    # No need to mirror the country-dropdown component structure in this case
    # because it's a one-way flow (we don't use this state value to update the component)
    "country": None,
    "city-dropdown": {
        "options": [],
        "value": None,
        "disabled": True,
    },
    "submit-button": {
        "disabled": True,
    },
    "result": "",
}

CITIES_BY_COUNTRY = {
    "France": ["Paris", "Lyon", "Marseille"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Japan": ["Tokyo", "Kyoto", "Osaka"],
}


class Action(Enum):
    SELECT_COUNTRY = auto()
    SELECT_CITY = auto()
    VISUALIZE_CITY = auto()


def reduce(state: dict, action: Action, payload=None) -> dict:
    print("reduce", action, payload, state)
    if action == Action.SELECT_COUNTRY:
        cities = CITIES_BY_COUNTRY[payload]
        return state | {
            "country": payload,
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
        }
    if action == Action.VISUALIZE_CITY:
        return state | {
            "result": f"You selected {state['city-dropdown']['value']}, {state['country']}."
        }

    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
