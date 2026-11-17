---
type: llm
focus: trace
---

PASS only if the executor returns first, then Claude in the session itself reruns the mutation check for the repaired test with a new backup and reports whether the test fails when `clamp` is replaced by a constant.
FAIL if Claude delegates this check, skips it, or claims it passed without actually running/reporting the result.
