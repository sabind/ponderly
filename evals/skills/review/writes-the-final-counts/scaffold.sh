#!/usr/bin/env bash
# Builds the workspace for this case: the shop fixture on branch shop-orders
# with the bin wrappers the Makefile's review target puts on the PATH, then
# copies this case's files/ over it and commits nothing, so the working tree
# adds shop/orders.py, whose order_total swallows the TypeError a NULL price
# or quantity raises and returns a partial, taxed total.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" shop shop-orders wrappers
# git ignores the findings file, so the skill accepts a path inside the
# repository and the tree stays clean.
echo review.json >> .git/info/exclude
cp -R "$(dirname "$0")/files/." .
