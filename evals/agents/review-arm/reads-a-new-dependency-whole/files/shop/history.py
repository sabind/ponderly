from shop.db import query

HISTORY_LIMIT = 30


def price_history(connection, price_log, product_id, limit=HISTORY_LIMIT):
    if price_log is None:
        return {"status": 503, "error": "price history is not enabled"}
    if limit < 1:
        return {"status": 400, "error": "limit must be at least 1"}
    products = query(connection, "SELECT id, name, price FROM products WHERE id = ?", (product_id,))
    if not products:
        return {"status": 404, "error": "no such product"}
    product = products[0]
    changes = price_log.changes(product_id, limit)
    lowest = product["price"]
    highest = product["price"]
    for change in changes:
        lowest = min(lowest, change["price"])
        highest = max(highest, change["price"])
    if changes:
        last_changed_at = changes[0]["changed_at"]
    else:
        last_changed_at = None
    return {
        "status": 200,
        "product": product,
        "changes": changes,
        "lowest": lowest,
        "highest": highest,
        "last_changed_at": last_changed_at,
    }
