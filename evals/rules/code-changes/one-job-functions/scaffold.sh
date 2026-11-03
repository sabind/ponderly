#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture on main with
# files/calc/orders.py, whose load_orders parses, cleans and classifies each row
# in one body. The file is copied in before the setup script runs so that its
# one commit holds it.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/files/." .
bash "$ROOT/evals/fixtures/setup.sh" calc main
