#!/usr/bin/env bash
# Builds the workspace for this case: this case's files/ copied in first, so
# the clamp fixture's main commit holds clamp/cli.py with --high and a README
# example running `python3 -m clamp.cli 150 --high 120`, with the bin wrappers
# the Makefile's review-arm target puts on the PATH; then rewrites clamp/cli.py
# uncommitted, renaming --high to --max and leaving the README as it is.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/files/." .
bash "$ROOT/evals/fixtures/setup.sh" clamp main wrappers
cat > clamp/cli.py <<'CLI'
import argparse

from clamp.core import DEFAULT_HIGH, DEFAULT_LOW, clamp


def main(argv=None):
    parser = argparse.ArgumentParser(prog="clamp", description="Keep a number inside a range.")
    parser.add_argument("value", type=float, help="the number to clamp")
    parser.add_argument("--low", type=float, default=DEFAULT_LOW, help="the smallest value returned")
    parser.add_argument("--max", type=float, default=DEFAULT_HIGH, help="the largest value returned")
    args = parser.parse_args(argv)
    print(clamp(args.value, args.low, args.max))


if __name__ == "__main__":
    main()
CLI
