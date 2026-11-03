#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture on main, with the bin
# wrappers the Makefile's rule-communication target puts on the PATH, and the
# README, gallery/thumbs.py and tests/test_thumbs.py from files/. The README
# describes a gallery page whose HTTP client is not chosen yet, offers requests
# or httpx, and gives what a visitor waits through under each. The files are
# copied in before the setup script runs so that its one commit holds them; the
# README replaces the fixture's README.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/files/." .
bash "$ROOT/evals/fixtures/setup.sh" calc main wrappers
