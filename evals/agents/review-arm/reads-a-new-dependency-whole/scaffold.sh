#!/usr/bin/env bash
# Builds the workspace for this case: this case's files/ copied in first, so
# the shop fixture's main commit holds shop/history.py, whose price_history
# returns 503 on line 7 when price_log is None, eighteen lines above the 200
# branch that returns the product, called by nothing but its tests, and
# shop/app.py, which creates the PriceLog only when SHOP_TRACK_PRICES=1, with
# tests that always build it; then checks out branch shop-product-page with the
# bin wrappers the Makefile's review-arm target puts on the PATH and rewrites
# shop/app.py uncommitted, importing price_history for the first time and
# adding a product route that calls it for the product, so the route answers
# 503 whenever price tracking is off, as it is by default.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/files/." .
bash "$ROOT/evals/fixtures/setup.sh" shop shop-product-page wrappers
cat > shop/app.py <<'APP'
import os
from datetime import datetime, timezone

from shop.db import connect
from shop.handlers import list_products
from shop.history import price_history
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
    if route == "product":
        result = price_history(app["connection"], app["price_log"], params["id"], limit=1)
        if result["status"] != 200:
            return result
        return {"status": 200, "product": result["product"]}
    if route == "set-price":
        return set_price(app, params["id"], params["price"])
    return {"status": 404, "error": "no such route"}
APP
