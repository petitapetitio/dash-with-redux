Guidelines / remarks
- name callbacks after the event
- ask gpt to improve the story (use case, ...)
+ avoid global states, allows dependency injection in each pages

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


## Benefits

Simplify form validation and the logic associated to user feedbacks

If you know from start you are building a rich app, you may want to start with another technology from the beginning.

I'm very open to change my mind. and please prove me I'm wrong. But if find it lacks building custom components easily.