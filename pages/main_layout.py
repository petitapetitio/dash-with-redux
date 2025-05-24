import dash
from dash import Dash, html, dcc, Output, Input, State

from pages.main_state import INITIAL_STATE, reduce, Action


def register_main(app: Dash):

    app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=True),
            dcc.Store(id="main-state", storage_type="session", data=INITIAL_STATE),
            html.Div(dash.page_container, id="page-container"),
            html.Div(
                id="toast",
                children=INITIAL_STATE["toast"]["content"],
                style={"opacity": 0},
            ),
        ]
    )

    @app.callback(
        Output("main-state", "data", allow_duplicate=True),
        Input("toast", "n_clicks"),
        State("main-state", "data"),
        prevent_initial_call=True,
    )
    def on_click_toast(n: str | None, state: dict):
        if n is None:
            return dash.no_update

        return reduce(state, Action.CLOSE_TOAST)

    @app.callback(
        Output("main-state", "data"),
        Input("url", "href"),
        State("main-state", "data"),
    )
    def on_page_load(href: str, state: dict):
        if href == state["url"]["href"]:
            return dash.no_update

        return reduce(state, Action.SET_URL, href)

    @app.callback(
        Output("url", "href", allow_duplicate=True),
        Output("toast", "style"),
        Output("toast", "children"),
        Input("main-state", "data"),
        prevent_initial_call=True,
    )
    def on_update_state(state: dict):
        return (
            state["url"]["href"],
            {"opacity": 1} if state["toast"]["visible"] else {"opacity": 0},
            state["toast"]["content"],
        )
