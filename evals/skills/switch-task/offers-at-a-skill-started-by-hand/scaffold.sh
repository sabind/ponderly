#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture, committed on main, with subtract, its test and its finished spec added uncommitted.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" calc main
# The earlier work the prompt describes, left uncommitted as work in hand.
cat >> calc/ops.py <<'PY'


def subtract(a, b):
    return a - b
PY
sed -i.bak 's/import add, multiply/import add, multiply, subtract/' tests/test_ops.py
rm tests/test_ops.py.bak
cat >> tests/test_ops.py <<'PY'

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
PY
cp -R "$(dirname "$0")/files/." .
