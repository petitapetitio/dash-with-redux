from dash import register_page, html, dcc, Output, Input, State, dash

import routes
from city import City
from client import Client
from pages.city_state import INITIAL_STATE, reduce, Action
import pages.main_state as main

CITIES_BY_COUNTRY = {
    "France": ["Paris", "Lyon", "Marseille"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Japan": ["Tokyo", "Kyoto", "Osaka"],
}


def register_page_city(app, cities_client: Client):
    register_page(
        "city",
        path=routes.CITY,
        layout=html.Div(
            [
                dcc.Store(id="city-state", data=INITIAL_STATE),
                html.H1("Select Location", className="mb-4"),
                html.Form(
                    [
                        html.Label("Country"),
                        dcc.Dropdown(
                            id="country-dropdown",
                            options=[
                                {"label": c, "value": c} for c in CITIES_BY_COUNTRY
                            ],
                            placeholder="Select a country",
                            clearable=False,
                        ),
                        html.Label("City"),
                        dcc.Dropdown(
                            id="city-dropdown",
                            placeholder="Select a city",
                            disabled=True,
                            clearable=False,
                        ),
                    ]
                ),
                html.Button(
                    "Visualize",
                    id="submit-button",
                    className="mt-3",
                    disabled=True,
                ),
                html.Button(
                    "Submit",
                    id="submit-button",
                    className="mt-3",
                    disabled=True,
                ),
                html.Div(id="result-output"),
            ]
        ),
    )

    @app.callback(
        Output("city-state", "data", allow_duplicate=True),
        Input("country-dropdown", "value"),
        State("city-state", "data"),
        prevent_initial_call=True,
    )
    def on_select_country(selected_country, state: dict):
        return reduce(state, Action.SELECT_COUNTRY, selected_country)

    @app.callback(
        Output("city-state", "data", allow_duplicate=True),
        Input("city-dropdown", "value"),
        State("city-state", "data"),
        prevent_initial_call=True,
    )
    def on_select_city(selected_city: str | None, state: dict):
        if selected_city is None:
            return dash.no_update

        return reduce(state, Action.SELECT_CITY, selected_city)

    @app.callback(
        Output("main-state", "data", allow_duplicate=True),
        Input("submit-button", "n_clicks"),
        State("city-state", "data"),
        State("main-state", "data"),
        prevent_initial_call=True,
    )
    def on_click_submit_form(n_clicks: int | None, state: dict, main_state: dict):
        if n_clicks is None:
            return dash.no_update

        city = City(
            name=state["city-dropdown"]["value"],
            country=state["country"],
            population=100,
        )
        cities_client.add_city(city)

        main_state = main.reduce(main_state, main.Action.ADD_CITY, city)
        main_state = main.reduce(main_state, main.Action.SET_URL, routes.CITIES)
        return main_state

    @app.callback(
        Output("city-dropdown", "options"),
        Output("city-dropdown", "value"),
        Output("city-dropdown", "disabled"),
        Output("submit-button", "disabled"),
        Output("result-output", "children"),
        Input("city-state", "data"),
    )
    def on_update_state(state: dict):
        print("city:on_update_state")
        return (
            state["city-dropdown"]["options"],
            state["city-dropdown"]["value"],
            state["city-dropdown"]["disabled"],
            state["submit-button"]["disabled"],
            state["result"],  # TODO : plot on "visualize"
        )
