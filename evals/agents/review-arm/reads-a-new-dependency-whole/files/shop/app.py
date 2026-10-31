import os
from datetime import datetime, timezone

from shop.db import connect
from shop.handlers import list_products
from shop.price_log import PriceLog


def load_settings(environ=os.environ):
    return {
        "database": environ.get("SHOP_DATABASE", ":memory:"),
        "track_prices": environ.get("SHOP_TRACK_PRICES") == "1",
    }


def build_app(settings):
    connection = connect(settings["database"])
    price_log = None
    if settings["track_prices"]:
        price_log = PriceLog(connection)
    return {"connection": connection, "price_log": price_log}


def set_price(app, product_id, price):
    app["connection"].execute("UPDATE products SET price = ? WHERE id = ?", (price, product_id))
    if app["price_log"] is not None:
        app["price_log"].record(product_id, price, datetime.now(timezone.utc).isoformat())
    return {"status": 200}


def handle(app, route, params):
    if route == "products":
        result = list_products(app["connection"], page=params.get("page", 1))
        return {"status": 200, **result}
    if route == "set-price":
        return set_price(app, params["id"], params["price"])
    return {"status": 404, "error": "no such route"}
