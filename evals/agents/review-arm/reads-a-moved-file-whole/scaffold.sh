#!/usr/bin/env bash
# Builds the workspace for this case: copies this case's files/ in first, so
# the calc fixture's commit on main also holds calc/average.py, whose mean
# skips the first value in its loop on line 6, and tests/test_average.py, then
# checks out branch move-average with the bin wrappers the Makefile's
# review-arm target puts on the PATH. It moves calc/average.py unchanged to
# calc/stats/average.py with git mv and points the test's import at the new
# path, and commits nothing, so the working tree against main holds the move,
# which git diff -M shows as R100, and that one edit.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
cp -R "$(dirname "$0")/files/." .
bash "$ROOT/evals/fixtures/setup.sh" calc move-average wrappers
GIT=/Library/Developer/CommandLineTools/usr/bin/git; [ -x "$GIT" ] || GIT=$(command -v git)
mkdir -p calc/stats
$GIT mv calc/average.py calc/stats/average.py
cat > tests/test_average.py <<'TEST'
import unittest

from calc.stats.average import mean


class MeanTest(unittest.TestCase):
    def test_mean_of_empty_is_zero(self):
        self.assertEqual(mean([]), 0.0)
TEST
