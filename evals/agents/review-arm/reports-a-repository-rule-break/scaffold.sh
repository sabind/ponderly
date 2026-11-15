#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture with this case's base/
# copied in first, so main commits .claude/rules/naming.md, whose one sentence
# is "Name every boolean function with an `is_` or `has_` prefix.", on branch
# calc-validate with the bin wrappers the Makefile's review-arm target puts on
# the PATH. It then copies this case's files/ over it and commits nothing, so
# the working tree adds valid_divisor to calc/ops.py on lines 9 and 10, a
# boolean function with neither prefix and no other defect.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/base/." .
bash "$ROOT/evals/fixtures/setup.sh" calc calc-validate wrappers
cp -R "$(dirname "$0")/files/." .
