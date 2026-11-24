#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture, committed on main; then
# copies this case's files/ in uncommitted, so the workspace holds the unticked
# visit-counter spec under .ponderly/specs/visit-counter/ that the prompt names:
# a VisitCounter in calc/visits.py that counts with calc.ops.add and skips a
# repeated event_id.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" calc main
cp -R "$(dirname "$0")/files/." .
