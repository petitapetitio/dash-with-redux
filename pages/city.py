from dash import register_page, html

_cities_by_countries = {
    "France": ["Paris", "Lyon", "Marseille"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Japan": ["Tokyo", "Kyoto", "Osaka"],
}


def register_page_city(app):
    register_page("city", path="/city", layout=html.Div("City"))
