#!/usr/bin/env bash
# Builds the workspace for this case: one test file, tests/test_parser.py, which
# the PostToolUse hook sorts as a test file, so reading it brings the Tests rule.
set -euo pipefail
mkdir -p tests
cat > tests/test_parser.py <<'PY'
import unittest


class ParserTest(unittest.TestCase):
    def test_empty_input_parses_to_nothing(self):
        self.assertEqual([], [])


if __name__ == "__main__":
    unittest.main()
PY
