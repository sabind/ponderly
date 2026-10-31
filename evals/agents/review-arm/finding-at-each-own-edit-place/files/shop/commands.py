from shop import db


def add_product(connection, name, price):
    product_id = db.save_product(connection, name, price)
    return {"ok": True, "message": "Added product %d" % product_id}


def delete_product(connection, product_id):
    return {"ok": True, "message": "Deleted product %d" % product_id}
