from dash import Dash

from pages.cities import register_page_cities
from pages.city import register_page_city
from pages.main import register_main


def create_app() -> Dash:
    app = Dash(use_pages=True)

    register_page_city(app)
    register_page_cities(app)
    register_main(app)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
