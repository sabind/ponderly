#!/usr/bin/env bash
# Builds the workspace for this case: the shop fixture on branch shop-page-size
# with the bin wrappers the Makefile's review target puts on the PATH, then,
# committing nothing, moves README.md to docs/README.md with git mv, so the
# working tree shows it as R100 against main, and edits shop/handlers.py to
# raise PAGE_SIZE from 10 to 20.
set -euo pipefail
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
bash "$ROOT/evals/fixtures/setup.sh" shop shop-page-size wrappers
# git ignores the findings file, so the skill accepts a path inside the
# repository and the tree stays clean.
echo review.json >> .git/info/exclude
mkdir -p docs
git mv README.md docs/README.md
sed 's/^PAGE_SIZE = 10$/PAGE_SIZE = 20/' shop/handlers.py > shop/handlers.py.new
mv shop/handlers.py.new shop/handlers.py
