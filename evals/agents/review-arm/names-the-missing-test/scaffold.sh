#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture with this case's base/
# copied in first, so main commits a divide that raises "cannot divide by zero"
# and a test that checks that message exactly, on branch calc-subtract with
# the bin wrappers the Makefile's review-arm target puts on the PATH. It then
# copies this case's files/ over it and commits nothing, so the working tree
# adds subtract to calc/ops.py on lines 9 and 10 with no test, and rewords
# divide's message on line 15, which the existing
# test_divide_by_zero_raises_its_message in tests/test_ops.py checks exactly.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/base/." .
bash "$ROOT/evals/fixtures/setup.sh" calc calc-subtract wrappers
cp -R "$(dirname "$0")/files/." .
