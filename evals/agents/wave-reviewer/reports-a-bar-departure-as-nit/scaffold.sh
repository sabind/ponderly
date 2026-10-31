#!/usr/bin/env bash
# Builds the workspace for this case: the calc fixture on branch calc-mean,
# with calc/ops.py and calc/compare.py from files/ committed in its one commit,
# both annotating every parameter and return, and the bin wrappers the
# Makefile's wave-reviewer target puts on the PATH; then an uncommitted
# calc/stats.py that adds a correct mean with no annotations, a departure from
# the code around it that costs nothing in this change, and an uncommitted
# tests/test_stats.py that tests mean in the fixture's own style, so the change
# carries its test.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/files/." .
bash "$ROOT/evals/fixtures/setup.sh" calc calc-mean wrappers
printf 'def mean(values):\n    return sum(values) / len(values)\n' > calc/stats.py
printf 'import unittest\n\nfrom calc.stats import mean\n\n\nclass StatsTest(unittest.TestCase):\n    def test_mean(self):\n        self.assertEqual(mean([1, 2]), 1.5)\n' > tests/test_stats.py
