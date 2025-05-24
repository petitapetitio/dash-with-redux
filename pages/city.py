import urllib.parse

from dash import register_page, html, dcc, Output, Input, State, dash

import pages.main_state as main
import routes
from city import City
from pages.city_state import INITIAL_STATE, reduce, Action

CITIES_BY_COUNTRY = {
    "France": ["Paris", "Lyon", "Marseille"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Japan": ["Tokyo", "Kyoto", "Osaka"],
}


def register_page_city(app):
    register_page(
        "city",
        path=routes.CITY,
        layout=html.Div(
            [
                dcc.Store(id="city-state", data=INITIAL_STATE),
                html.H1("Select Location", className="mb-4"),
                html.Form(
                    [
                        dcc.Dropdown(
                            id="country-dropdown",
                            options=[
                                {"label": c, "value": c} for c in CITIES_BY_COUNTRY
                            ],
                            placeholder="Select a country",
                            clearable=False,
                        ),
                        dcc.Dropdown(
                            id="city-dropdown",
                            placeholder="Select a city",
                            disabled=True,
                            clearable=False,
                        ),
                        dcc.Input(
                            id="comment-input",
                            placeholder="Free comment",
                            value=INITIAL_STATE["comment"],
                            debounce=0.5,
                        ),
                        dcc.Input(
                            id="population-input",
                            placeholder="Population",
                            value=INITIAL_STATE["population"],
                            pattern=r"\d*",
                            debounce=0.5,
                        )
                    ]
                ),
                html.Button(
                    "Visualize",
                    id="visualize-button",
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
        if selected_country == state["country"]:
            return dash.no_update

        return reduce(state, Action.SELECT_COUNTRY, selected_country)

    @app.callback(
        Output("city-state", "data", allow_duplicate=True),
        Input("city-dropdown", "value"),
        State("city-state", "data"),
        prevent_initial_call=True,
    )
    def on_select_city(selected_city: str | None, state: dict):
        if selected_city == state["city-dropdown"]["value"]:
            return dash.no_update

        return reduce(state, Action.SELECT_CITY, selected_city)

    @app.callback(
        Output("city-state", "data", allow_duplicate=True),
        Input("comment-input", "value"),
        State("city-state", "data"),
        prevent_initial_call=True,
    )
    def on_type_comment(comment: str, state: dict):
        if comment == state["comment"]:
            return dash.no_update

        return reduce(state, Action.SET_COMMENT, comment)

    @app.callback(
        Output("city-state", "data", allow_duplicate=True),
        Input("population-input", "value"),
        State("city-state", "data"),
        prevent_initial_call=True,
    )
    def on_enter_population(population: str, state: dict):
        if population == state["population"]:
            return dash.no_update

        return reduce(state, Action.SET_POPULATION, population)

    @app.callback(
        Output("main-state", "data", allow_duplicate=True),
        Input("visualize-button", "n_clicks"),
        State("city-state", "data"),
        State("main-state", "data"),
        prevent_initial_call=True,
    )
    def on_click_visualize(n_clicks: int | None, state: dict, main_state: dict):
        if n_clicks is None:
            return dash.no_update

        return main_state

    @app.callback(
        Output("main-state", "data", allow_duplicate=True),
        Input("submit-button", "n_clicks"),
        State("city-state", "data"),
        State("main-state", "data"),
        prevent_initial_call=True,
    )
    def on_click_submit(n_clicks: int | None, state: dict, main_state: dict):
        if n_clicks is None:
            return dash.no_update

        try:
            population = int(state["population"])
        except ValueError:
            return main.reduce(main_state, main.Action.OPEN_TOAST, "Population should be a sequence of digits")

        city = City(
            name=state["city-dropdown"]["value"],
            country=state["country"],
            population=population,
            comment=state["comment"],
        )

        main_state = main.reduce(main_state, main.Action.ADD_CITY, city)
        main_state = main.reduce(main_state, main.Action.CLOSE_TOAST, city)
        main_state = main.reduce(main_state, main.Action.SET_URL, routes.CITIES)
        return main_state

    @app.callback(
        Output("city-state", "data"),
        Input("url", "href"),
        State("city-state", "data"),
        State("main-state", "data"),
        prevent_initial_call=True,
    )
    def on_page_load(href: str, state: dict, main_state: dict):
        url = urllib.parse.urlparse(href)
        if url.path != routes.CITY:
            return dash.no_update

        if url.query == "":
            return dash.no_update

        print("city:on_page_load")
        index = int(url.query.split("index=")[1])
        city = main_state["cities"][index]

        state = reduce(state, Action.SELECT_COUNTRY, city["country"])
        state = reduce(state, Action.SELECT_CITY, city["name"])
        state = reduce(state, Action.SET_POPULATION, city["population"])
        state = reduce(state, Action.SET_COMMENT, city["comment"])
        return state

    @app.callback(
        Output("country-dropdown", "value"),
        Output("city-dropdown", "options"),
        Output("city-dropdown", "value"),
        Output("city-dropdown", "disabled"),
        Output("population-input", "value"),
        Output("comment-input", "value"),
        Output("submit-button", "disabled"),
        Output("result-output", "children"),
        Input("city-state", "data"),
    )
    def on_update_state(state: dict):
        print("city:on_update_state")
        return (
            state["country"],
            state["city-dropdown"]["options"],
            state["city-dropdown"]["value"],
            state["city-dropdown"]["disabled"],
            state["population"],
            state["comment"],
            state["submit-button"]["disabled"],
            state["result"],  # TODO : plot on "visualize"
        )
