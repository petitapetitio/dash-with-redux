
- évolution de la population

- name callbacks after the event

- composable actions


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

## Common mistakes

Forgetting `prevent_initial_call=True` on the main downstream callback.

```python
    @app.callback(
        Output("url", "href"),
        Input("main-state", "data"),
        prevent_initial_call=True,  # <-- HERE
    )
    def on_state_updated(state: dict):
        return state["url"]["href"]
```

Forgetting ` allow_duplicate=True` for `Output("url", "href")` on the main downstream callback.

```python
    @app.callback(
        Output("url", "href", allow_duplicate=True),  # <-- HERE
        Input("main-state", "data"),
        State("main-state", "modified_timestamp"),
        prevent_initial_call=True,
    )
    def on_update_state(state: dict, ts):
        return state["url"]["href"]
```

Using an in-memory store instead of a session store (for the main state)

Updating with the path only (instead of the full url).

Mixer Button(href=...) et state["url"]["href"].

## Location in the state or not

- advantages : homogènité
- points de vigilance
- inconvénients 
  - callback for each url
  - you cannot navigate through direct url then (this is in facts very inconvenient)

## Benefits

- Testability
- Clear intent (actions are focused and express the intent)
- Simplify form validation and the logic associated to user feedbacks
- Decouple the state from the layout

Dash recommended approach is fine for prototypes.

When the app get richer, you may want to use this pattern to keep the logic clear.

If you know from start you are building a rich app, you may want to start with another technology from the beginning.