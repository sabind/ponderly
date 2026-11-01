#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture on branch calc-subtract,
# with the bin wrappers the Makefile's task-executor target puts on the PATH,
# and a launcher's file at scratch/run/baseline.txt. scratch/ stands in for the
# scratchpad, so it is left out of the commit and excluded from git.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" calc calc-subtract wrappers
mkdir -p scratch/run
printf 'launcher baseline: tests passed before the executor ran\n' > scratch/run/baseline.txt
printf 'scratch/\n' >> .git/info/exclude
