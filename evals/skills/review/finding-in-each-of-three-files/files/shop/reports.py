from shop.db import connect, query


def average_price(path):
    connection = connect(path)
    rows = query(connection, "SELECT price FROM products")
    if not rows:
        return 0.0
    connection.close()
    return sum(row["price"] for row in rows) / len(rows)


def price_range(path):
    connection = connect(path)
    rows = query(connection, "SELECT price FROM products")
    if not rows:
        return None
    connection.close()
    return min(row["price"] for row in rows), max(row["price"] for row in rows)
