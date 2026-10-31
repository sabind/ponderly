import unittest

from shop.app import build_app, handle


def tracked_app():
    app = build_app({"database": ":memory:", "track_prices": True})
    app["connection"].execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    app["connection"].execute("INSERT INTO products (name, price) VALUES ('lamp', 20.0)")
    return app


class HandleTest(unittest.TestCase):
    def test_products_route_lists_the_catalogue(self):
        result = handle(tracked_app(), "products", {})
        self.assertEqual([item["name"] for item in result["items"]], ["lamp"])

    def test_set_price_route_records_the_change(self):
        app = tracked_app()
        handle(app, "set-price", {"id": 1, "price": 18.0})
        self.assertEqual([change["price"] for change in app["price_log"].changes(1, 10)], [18.0])

    def test_unknown_route_is_not_found(self):
        result = handle(tracked_app(), "checkout", {})
        self.assertEqual(result["status"], 404)
