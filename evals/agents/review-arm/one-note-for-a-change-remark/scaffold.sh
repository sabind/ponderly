#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture on branch
# calc-strategies with the bin wrappers the Makefile's review-arm target puts
# on the PATH, then copies this case's files/ over it and commits nothing, so
# the working tree holds two new strategy modules, calc/add_strategy.py and
# calc/multiply_strategy.py, whose apply calls _both_numbers on line 10,
# ignores its result and returns {"success": True} on line 11, and
# formatting-only edits of calc/ops.py, calc/__init__.py and tests/test_ops.py
# that change no behaviour.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" calc calc-strategies wrappers
cp -R "$(dirname "$0")/files/." .
