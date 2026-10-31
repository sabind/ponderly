#!/usr/bin/env bash
# Builds the workspace for this case: the shop fixture on branch shop-orders
# with the bin wrappers the Makefile's review target puts on the PATH, then
# copies this case's files/ over it and commits nothing, so the working tree
# adds shop/orders.py with the planted defect the README names.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" shop shop-orders wrappers
cp -R "$(dirname "$0")/files/." .
