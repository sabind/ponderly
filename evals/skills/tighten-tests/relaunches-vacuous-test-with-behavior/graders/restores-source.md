---
type: llm
focus: trace
---

PASS only if Claude restores the mutation/backup so the source matches the initial state and reports the source check result.
FAIL if the hand-back leaves the fixture source changed or omits the source check.
