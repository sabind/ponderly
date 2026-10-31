#!/usr/bin/env bash
# Builds the workspace for this case: this case's files/ copied in first, so
# the shop fixture's main commit holds shop/commands.py, whose delete_product
# returns a success message and touches nothing, with the bin wrappers the
# Makefile's review-arm target puts on the PATH; then rewrites shop/db.py
# uncommitted, adding save_product persistence and no way to delete, so the
# stub in shop/commands.py and the missing delete in shop/db.py each need an
# edit of their own.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/files/." .
bash "$ROOT/evals/fixtures/setup.sh" shop main wrappers
cat > shop/db.py <<'DB'
import sqlite3


def connect(path=":memory:"):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def query(connection, sql, params=()):
    return [dict(row) for row in connection.execute(sql, params)]


def save_product(connection, name, price):
    cursor = connection.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    connection.commit()
    return cursor.lastrowid
DB
