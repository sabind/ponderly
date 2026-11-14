#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
CASE=$(dirname "$0")
cp -R "$CASE/../audits-over-tested-branch/files/." .
bash "$ROOT/evals/fixtures/setup.sh" clamp clamp-tests wrappers
cp "$ROOT/evals/fixtures/clamp/tests/test_clamp.py" tests/test_clamp.py
git -c user.name=fixture -c user.email=fixture@example.com commit -q -am "Test clamp"
