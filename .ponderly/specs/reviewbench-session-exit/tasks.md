# Implementation Plan

## Overview

The adapter changes come in two steps on `benchmarks/reviewbench/agent/agent.py`, one after the other since both edit the same file: first the interrupt path inside `run_claude`, then the launch flag, the wait setting, the log clause and the cost recovery in `review_pull_request` with the new `transcript_cost`. The harness and README edits touch other files and run beside the first step. The five checks come last, once the behaviour they prove exists. Nothing is run beyond `make validate` and each task's ephemeral check: no image is built and no benchmark or eval runs in this spec.

## Tasks

- [x] 1. Change the adapter
  - [x] 1.1 Add the interrupt before the kill in `run_claude` of `benchmarks/reviewbench/agent/agent.py`
    - Add the keyword argument `interrupt_wait_seconds=None`. When the grace elapses with the process still running and the wait is a number above 0: send `SIGINT` to the process group with the same `ProcessLookupError` and `PermissionError` handling as the kill; poll `process.poll()` every `POLL_SECONDS` until it exits or the wait elapses, the reader thread collecting stdout throughout; when it exited, set `ended = "interrupted"` and return the exit code and the joined stdout; when it is still running, fall into today's `SIGKILL`, reader join and stdout close with `ended = "final"`. A wait of `None` or `0` keeps today's path. Update the docstring's list of `ended` values. The time-limit path stays a plain kill. Ephemeral check: a scratch stub that writes a final review file, prints a result and sleeps, called through `run_claude` with a grace of 0 and a wait of 2, returns `"interrupted"` with the result on stdout; the same stub ignoring `SIGINT` returns `"final"` after about 2 seconds
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_
  - [x] 1.2 Wire the launch flag, the wait, the log clause and the cost recovery in `benchmarks/reviewbench/agent/agent.py`
    - In `review_arguments`, insert `"--disallowedTools", "ScheduleWakeup"` after `"--permission-mode", "bypassPermissions"`; leave `repair_arguments` as it is. Read `RB_INTERRUPT_WAIT_SECONDS` as a float, 20 when unset or empty, and pass it to the review session's `run_claude` only. In the grace log line, append `; it exited on the interrupt` when `ended` is `"interrupted"` and `; it ignored the interrupt and was killed` when it is `"final"`, keeping the line's existing start. Add `transcript_cost(home)`: the newest `.jsonl` directly under any `<home>/.claude/projects/<project>/` directory, read line by line, rows that do not parse skipped, returning the `used` of the last row whose `type` is `attachment` and whose `attachment.type` is `budget_usd` as a float, or `None` when the home is `None`, the directory or file is absent, no such row exists or `used` is not a number. After `usage_of(stdout)`, when `cost_usd` is absent, call it with `claude_home(env)` and set `usage["cost_usd"]` when it returns a number, logging `cost <value> read from the transcript's last budget line`; otherwise log `no cost in the result and none in a transcript`. Ephemeral check: a scratch home with a project directory holding a transcript of three rows (a budget row with used 1.5, a line that is not JSON, a budget row with used 3.99) and a sub-directory with a newer file gives 3.99; a transcript with no budget row gives `None`
    - _Requirements: 1.1, 1.2, 1.3, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  - [x] 1.3 Fix the repair session's usage merge in `benchmarks/reviewbench/agent/agent.py`
    - In `review_pull_request`, merge the repair's usage so that a missing review `cost_usd` stays missing when the repair reports one, and so that the repair's `duration_ms` is added to the review's `time_in_ms` before `max()` with the adapter's clock, not after. Change `add_usage` or its call, whichever is smaller. Ephemeral check: a review usage without `cost_usd` merged with a repair usage of cost 0.3 has no `cost_usd`; one with cost 2.0 gives 2.3; a review time of 50 ms with a repair time of 100 ms and an adapter clock of 5000 ms gives 5000, and with an adapter clock of 10 ms gives 150
    - _Requirements: 3.9, 3.10_

- [x] 2. Pass the wait through the harness and document it
  - [x] 2.1 Pass `RB_INTERRUPT_WAIT_SECONDS` into the image in `benchmarks/reviewbench/run.sh` and name it in the `benchmarks/reviewbench/Makefile` header comment
    - In `run.sh`, add `-e RB_INTERRUPT_WAIT_SECONDS` after `-e RB_FINAL_GRACE_SECONDS` on the `try-agent.sh` call; in the Makefile's header comment, add it to the sentence listing the variables that reach the adapter in the image. Manual check: `git diff` shows the one line in each file; `bash -n benchmarks/reviewbench/run.sh` passes
    - _Requirements: 2.5_
  - [x] 2.2 Document the wakeup flag, the interrupt and the recovered cost in `benchmarks/reviewbench/README.md`
    - Under the variables that reach the image and are not recorded in `run.json`, add `RB_INTERRUPT_WAIT_SECONDS`: the seconds the adapter waits after interrupting a session that outlived the grace before killing it, `20` by default. In the evidence section's paragraph on the session, say that the review session runs with Claude Code's `ScheduleWakeup` tool disallowed, because a session that scheduled a wakeup as a fallback while the arms ran stayed alive for the timer after its review was done and was killed with its cost lost; that a session still running once the review file has been final for the grace gets an interrupt and the wait before the kill; and that when the result carries no cost the adapter reads the session's spend from the transcript's last budget line and says so in `adapter.log`. Manual check: the README's lines stay under its existing width and the three statements read in order
    - _Requirements: 4.2_

- [x] 3. Prove the paths
  - [x] 3.1 Add the five checks to `checks/test_reviewbench_agent.py`
    - Add stub actions: `final_then_result_on_interrupt` installs a `SIGINT` handler that prints `RESULT` and exits 0, writes the final review file and sleeps 60; `final_then_sleep_ignoring_interrupt` sets `SIGINT` to `SIG_IGN`, writes the final review file, writes `<HOME>/.claude/projects/-work-repo/session.jsonl` with a budget row (`used` 1.5), a line that is not JSON and a budget row (`used` 3.99), then sleeps 60; `final_then_sleep_without_budget` does the same with a transcript holding one `user` row and no budget row. Add the tests, one per path, each with `RB_FINAL_GRACE_SECONDS="1"`, `RB_TIMEOUT_SECONDS="8"` and `RB_INTERRUPT_WAIT_SECONDS="2"` where the stub sleeps: the review launch argv of the `unparseable` plan's first call holds `--disallowedTools` followed by `ScheduleWakeup` and its second call's argv holds no `--disallowedTools`; the result-on-interrupt plan exits 0 with `cost_usd` 0.5 and an adapter log line matching `turned final; it exited on the interrupt`; the ignoring plan exits 0 after at least 3 seconds with `cost_usd` 3.99, a log line matching `turned final; it ignored the interrupt and was killed` and a line `cost 3.99 read from the transcript's last budget line`; the no-budget plan exits 0 with no `cost_usd` in `usage` and a log line `no cost in the result and none in a transcript`. Keep the test names behaviour sentences. Check: `make validate`, and the existing grace tests still pass
    - _Requirements: 4.1_
  - [x] 3.2 Add the two checks for the usage merge to `checks/test_reviewbench_agent.py`
    - One test per path against the existing stub: a review that prints no result and whose transcript has no budget row, followed by a repair that reports a cost, leaves `cost_usd` absent from the findings file; a review whose result reports a short duration followed by a repair with a longer one records the adapter's clock, not their sum. Add stub actions as needed. Check: `make validate`
    - _Requirements: 3.9, 3.10_

## Notes

- Every edit to the adapter is the smallest change that gives the behaviour; no function is restyled.
- No image is built and no benchmark or eval runs in this spec; the first run on the rebuilt image is the Owner's call afterwards.
- `rg` needs an explicit path and `</dev/null`; never bare `git stash`; commit nothing; never print a credential.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "2.1", "2.2"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["1.3", "3.1"] },
    { "id": 3, "tasks": ["3.2"] }
  ]
}
```
