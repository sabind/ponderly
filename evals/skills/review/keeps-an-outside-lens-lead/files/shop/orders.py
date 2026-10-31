from shop.db import query

TAX_RATE = 0.2


def order_total(connection, order_id):
    lines = query(connection, "SELECT price, quantity FROM order_lines WHERE order_id = ?", (order_id,))
    total = 0.0
    try:
        for line in lines:
            total += line["price"] * line["quantity"]
    except TypeError:
        pass
    return round(total * (1 + TAX_RATE), 2)
