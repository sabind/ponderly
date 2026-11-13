---
type: llm
---

The reply is a Summary from an agent asked to put the same header-comment line at the top of `calc/ops.py` and `tests/test_ops.py`, and a different change, a licence line, at the end of `README.md`.

PASS if the status is done AND each of `calc/ops.py`, `tests/test_ops.py` and `README.md` appears on exactly one line of the `files changed` list, each line with a reason. The two Python files may share one line or have a line each. No line may name a file other than these three.
FAIL if any of the three files is missing from the list, if any file is named on more than one line, if any line has no reason, or if the status is stopped.
