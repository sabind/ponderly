import unittest

from shop.db import connect
from shop.history import price_history
from shop.price_log import PriceLog


def priced_db():
    connection = connect()
    connection.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    connection.execute("INSERT INTO products (name, price) VALUES ('lamp', 20.0)")
    return connection


class PriceHistoryTest(unittest.TestCase):
    def test_reports_the_lowest_and_highest_recorded_price(self):
        connection = priced_db()
        price_log = PriceLog(connection)
        price_log.record(1, 25.0, "2026-01-01")
        price_log.record(1, 15.0, "2026-02-01")
        result = price_history(connection, price_log, 1)
        self.assertEqual((result["lowest"], result["highest"]), (15.0, 25.0))

    def test_a_product_with_no_changes_reports_its_current_price(self):
        connection = priced_db()
        result = price_history(connection, PriceLog(connection), 1)
        self.assertEqual(result["product"]["price"], 20.0)
        self.assertIsNone(result["last_changed_at"])

    def test_an_unknown_product_is_not_found(self):
        connection = priced_db()
        result = price_history(connection, PriceLog(connection), 2)
        self.assertEqual(result["status"], 404)
