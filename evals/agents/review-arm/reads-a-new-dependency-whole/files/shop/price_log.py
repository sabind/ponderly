from shop.db import query


class PriceLog:
    def __init__(self, connection):
        self.connection = connection
        connection.execute(
            "CREATE TABLE IF NOT EXISTS price_changes (product_id INTEGER, price REAL, changed_at TEXT)"
        )

    def record(self, product_id, price, changed_at):
        self.connection.execute(
            "INSERT INTO price_changes (product_id, price, changed_at) VALUES (?, ?, ?)",
            (product_id, price, changed_at),
        )

    def changes(self, product_id, limit):
        return query(
            self.connection,
            "SELECT price, changed_at FROM price_changes WHERE product_id = ? ORDER BY changed_at DESC LIMIT ?",
            (product_id, limit),
        )
