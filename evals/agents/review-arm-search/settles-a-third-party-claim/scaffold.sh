#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture on branch
# calc-workflows with the bin wrappers the Makefile's review-arm-search target
# puts on the PATH, then copies this case's files/ over it and commits nothing,
# so the working tree holds two new GitHub Actions workflows,
# .github/workflows/unit-tests.yml and .github/workflows/lint-checks.yml, whose
# push event sets both branches and branches-ignore on lines 5 to 8, which
# GitHub rejects.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" calc calc-workflows wrappers
cp -R "$(dirname "$0")/files/." .
