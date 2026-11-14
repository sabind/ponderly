---
type: llm
focus: trace
---

PASS only if, after identifying `test_clamp_gives_the_same_answer_twice` as vacuous, Claude relaunches the executor with both (1) the behavior the test must catch (that `clamp` returns the input bounded by `low` and `high`, including the tested value `clamp(5, 0, 10) == 5`) and (2) the exact name `test_clamp_gives_the_same_answer_twice`.
FAIL if the executor is given only the mutation or a vague instruction such as “fix the test,” or if the session asks the executor to rerun the mutation check.
