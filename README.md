
- évolution de la population

- name callbacks after the event



## dash will complain about circular dependency. It is not.

@app.callback(
        Output("main-state", "data"),
        Input("url", "href"),
        State("main-state", "data")
    )
    def on_page_load(href: str, state: dict):
        if href == state["url"]["href"]:
            print("!! on_page_load")
            return dash.no_update

        print("!! on_page_load")
        return reduce(state, Action.SET_URL, href)