from dash import Dash

from pages.cities import register_page_cities
from pages.city import register_page_city
from pages.main_layout import register_main


def create_app() -> Dash:
    app = Dash(use_pages=True)

    register_page_city(app)
    register_page_cities(app)
    register_main(app)

    return app


if __name__ == "__main__":
    import logging

    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.ERROR)

    create_app().run(debug=False)
