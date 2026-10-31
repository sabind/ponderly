# finding-in-each-of-three-files

Tests that the review keeps one finding at each copy when the same defect is
planted in three changed files, and twice in one of them, so that each copy
gets its own edit, rather than one finding that describes the other copies in a
sentence or a merge that collapses them. The second copy in `shop/reports.py`
is there because the merge's duplicate collapse only compares candidates in the
same file: two findings there that name each other's file and line must both
reach the reply.

## What the scaffold builds

The `shop` fixture, built by `evals/fixtures/setup.sh shop shop-lookups`,
which commits the fixture on main and checks out branch `shop-lookups`. The
scaffold copies this case's `files/` in after that call, for the reason the
`finds-planted-defects` README gives, and commits nothing, so the planted
change is an uncommitted diff against main: one changed file and two new ones.

Each planted function opens a connection with `connect(path)`, queries it,
returns early when the query finds no rows and closes the connection only on
the path that found rows, so the empty path leaves the connection open
(reliability: resource leak; a query that raises leaks it too):

- `files/shop/handlers.py` adds `product_name`, lines 13 to 19: `connect` on
  line 14, the early `return None` on line 17, `connection.close()` on line 18.
- `files/shop/reports.py` is new and holds two copies:
  - `average_price`, lines 4 to 10: `connect` on line 5, the early
    `return 0.0` on line 8, `connection.close()` on line 9.
  - `price_range`, lines 13 to 19: `connect` on line 14, the early
    `return None` on line 17, `connection.close()` on line 18.
- `files/shop/pricing.py` is new and adds `cheapest_product`, lines 4 to 10:
  `connect` on line 5, the early `return None` on line 8, `connection.close()`
  on line 9.

The graders want, for each file, a final-list line whose range starts and ends
inside a planted function and whose message names the connection or its close
(`connection`, `connect` or `close`, any case), so a finding anchored at the
`connect` line, the early return or the whole function passes, and a finding on
those lines about something else, such as a missing test, does not. One more
grader wants two such lines on `shop/reports.py`, one inside each copy, in
either order; a single finding spanning both functions passes neither range.

These line numbers live here, outside the fixture tree, because `setup.sh`
copies the whole fixture into the reviewed workspace: an answer key there
would let the review read the defects instead of finding them.
