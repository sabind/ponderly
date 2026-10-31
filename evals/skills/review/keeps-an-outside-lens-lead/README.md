# keeps-an-outside-lens-lead

Tests that a defect at the edge of two lenses reaches the review's final
list. The planted error is swallowed, which a reliability lens may see, and
the swallowing makes a function return a wrong total, which is correctness:
an arm may name it only as a lead outside its own lens, which the review must
hand to the wave reviewer to verify rather than drop.

The case proves the outcome, not the route through the leads. It passes when
the final list holds the planted defect, but it also passes when an arm
reported the defect directly as one of its own findings, so it does not show
that a lead was quoted to the wave reviewer, verified and folded.

## What the scaffold builds

The `shop` fixture, built by `evals/fixtures/setup.sh shop shop-orders
wrappers`, which commits the fixture on main and checks out branch
`shop-orders`. The scaffold copies this case's `files/` in after that call and
commits nothing, so the planted change is an uncommitted diff against main,
as in `finds-planted-defects`.

`files/shop/orders.py` is a new file adding `order_total`, which sums each
order line's `price * quantity` and adds tax. The planted defect:

- lines 12-13: the summing loop sits in a `try` whose `except TypeError:
  pass` swallows the error a NULL `price` or `quantity` raises, so the loop
  stops at that line and the partial sum, taxed, is returned as the order's
  total (reliability: swallowed error; correctness: wrong total).

The grader accepts a final-list line on `shop/orders.py` that starts and
ends between lines 9 and 14, so a finding anchored on the `except`, the
whole `try` block, the line that raises or the taxed return all count.

These line numbers live here, outside the fixture tree, because `setup.sh`
copies the whole fixture into the reviewed workspace: an answer key there
would let the review read the defect instead of finding it.
