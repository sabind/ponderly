from shop.db import connect, query

PAGE_SIZE = 10


def list_products(connection, page=1, size=PAGE_SIZE):
    rows = query(connection, "SELECT id, name, price FROM products ORDER BY id")
    offset = (page - 1) * size
    items = rows[offset:offset + size]
    return {"items": items, "page": page, "has_more": len(rows) > offset + size}


def product_name(path, product_id):
    connection = connect(path)
    rows = query(connection, "SELECT name FROM products WHERE id = ?", (product_id,))
    if not rows:
        return None
    connection.close()
    return rows[0]["name"]
