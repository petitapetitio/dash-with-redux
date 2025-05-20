import dash
from dash import register_page, html, Dash, Input, Output, State

import pages.main_state as main
import routes


def register_page_cities(app: Dash):
    register_page(
        "cities",
        path=routes.CITIES,
        layout=html.Div(
            [
                html.H1("Cities"),
                html.Div(id="cities-array"),
                html.Button(id="add-city", children="Add a city"),
            ]
        ),
    )

    @app.callback(
        Output("main-state", "data", allow_duplicate=True),
        Input("add-city", "n_clicks"),
        State("main-state", "data"),
        prevent_initial_call=True,
    )
    def on_add_city_clicked(n_clicks: int | None, main_state: dict):
        if n_clicks is None:
            return dash.no_update

        return main.reduce(main_state, main.Action.SET_URL, routes.CITY)

    @app.callback(
        Output("cities-array", "children"),
        Input("main-state", "data"),
    )
    def on_state_updated(state: dict):
        print("cities:on_state_updated", state)
        if len(state["cities"]) == 0:
            return ""

        rows = [
            html.Tr(
                [
                    html.Th("Country"),
                    html.Th("City"),
                    html.Th("Population", style={"text-align": "right"}),
                ]
            )
        ]
        for city in state["cities"]:
            rows.append(
                html.Tr(
                    [
                        html.Td(city["country"]),
                        html.Td(city["name"]),
                        html.Td(city["population"], style={"text-align": "right"}),
                    ]
                )
            )

        return html.Table(rows)
