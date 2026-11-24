#!/usr/bin/env bash
# Builds the workspace for this case: this case's files/ copied in first, so
# the clamp fixture's main commit holds clamp/cli.py printing `clamped: 120.0`
# and a README example running `python3 -m clamp.cli 150 --high 120`, with the
# bin wrappers the Makefile's review-arm target puts on the PATH; then rewrites
# clamp/cli.py and README.md uncommitted, adding a --quiet flag that prints the
# bare number, with its help text and a README line, so the change is correct
# and leaves no documentation defect.
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
    parser.add_argument("--high", type=float, default=DEFAULT_HIGH, help="the largest value returned")
    parser.add_argument("--quiet", action="store_true", help="print only the number, without the clamped: label")
    args = parser.parse_args(argv)
    result = clamp(args.value, args.low, args.high)
    print(result if args.quiet else f"clamped: {result}")


if __name__ == "__main__":
    main()
CLI
cat >> README.md <<'README'

Add `--quiet` to print only the number, so `python3 -m clamp.cli 150 --high 120 --quiet`
prints `120.0`.
README
