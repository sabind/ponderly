from shop.db import connect, query


def cheapest_product(path):
    connection = connect(path)
    rows = query(connection, "SELECT id, name, price FROM products ORDER BY price LIMIT 1")
    if not rows:
        return None
    connection.close()
    return rows[0]
