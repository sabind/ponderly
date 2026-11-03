"""Reads the shop's order export."""

import csv


def load_orders(path):
    """Returns the orders in the CSV export at path as dicts."""
    orders = []
    with open(path, newline="") as export:
        for row in csv.DictReader(export):
            if not row["customer"].strip():
                continue
            amount = row["amount"].replace("$", "").replace(",", "")
            cents = round(float(amount) * 100)
            status = row["status"].strip().lower()
            if status not in ("paid", "refunded"):
                status = "unknown"
            orders.append({"customer": row["customer"].strip(), "cents": cents, "status": status})
    return orders
