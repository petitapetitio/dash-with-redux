from dash import Dash

from client import InMemoryClient
from pages.cities import register_page_cities
from pages.city import register_page_city
from pages.main_layout import register_main


def create_app() -> Dash:
    app = Dash(use_pages=True)

    cities_client = InMemoryClient()
    register_page_city(app, cities_client)
    register_page_cities(app, cities_client)
    register_main(app)

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
