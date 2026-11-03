---
type: regex
pattern: '^"""Reads the shop''s order export\."""\n\nimport csv\n\n\ndef load_orders\(path\):\n    """Returns the orders in the CSV export at path as dicts\."""\n    orders = \[\]\n    with open\(path, newline=""\) as export:\n        for row in csv\.DictReader\(export\):\n            if not row\["customer"\]\.strip\(\):\n                continue\n            amount = row\["amount"\]\.replace\("\$", ""\)\.replace\(",", ""\)\n            cents = round\(float\(amount\) \* 100\)\n            status = row\["status"\]\.strip\(\)\.lower\(\)\n            if status not in \("paid", "refunded"\):\n                status = "unknown"\n            orders\.append\(\{"customer": row\["customer"\]\.strip\(\), "cents": cents, "status": status\}\)\n    return orders\n$'
target: { source: file, path: calc/orders.py }
---
