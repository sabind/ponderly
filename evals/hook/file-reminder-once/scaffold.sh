#!/usr/bin/env bash
# Builds the workspace for this case: two test files, tests/test_parser.py and
# tests/test_lexer.py, both of which remind-rules.sh sorts as test files, so
# the Tests rule attaches after the first Read and not after the second.
set -euo pipefail
mkdir -p tests
cat > tests/test_parser.py <<'TEST'
import unittest


class ParserTest(unittest.TestCase):
    def test_empty_input_parses_to_nothing(self):
        self.assertEqual([], [])
TEST
cat > tests/test_lexer.py <<'TEST'
import unittest


class LexerTest(unittest.TestCase):
    def test_empty_input_has_no_tokens(self):
        self.assertEqual([], [])
TEST
