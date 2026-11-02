# Requirements Document

## Introduction

The ReviewBench adapter, `benchmarks/reviewbench/agent/agent.py`, runs the `review` skill in one Claude Code session per pull request and writes the findings file the benchmark scores, with the session's cost and duration. Five sessions today and in chunk 4 wrote their final review file and then kept running until the adapter killed them after its grace, and each lost its cost: the session had scheduled a wakeup with Claude Code's `ScheduleWakeup` tool as a fallback while the review arms ran, never cancelled it, and Claude Code's print mode kept the process alive for the timer and never printed its result. The one session that cancelled its wakeup exited, and the eight that never scheduled one exited. This task stops the session scheduling a wakeup, ends a session that still lingers with an interrupt before the kill, and recovers the cost of a killed session from its own transcript. It serves the Owner, who pays for each review and reads the run's cost column and health report.

## Glossary

- **Owner**: The person who pays for each review and reads the run's report.
- **Adapter**: The ReviewBench entrypoint `benchmarks/reviewbench/agent/agent.py`, run inside the image once per pull request.
- **Review_Session**: The Claude Code process the Adapter launches with `-p` to run the `review` skill on one pull request.
- **Review_File**: The JSON file the `review` skill writes at the path the Adapter gives it, whose `pass` is `"final"` when the review is done.
- **Result_JSON**: The JSON object Claude Code prints on stdout at the end of a `-p` session, carrying `total_cost_usd`, `duration_ms` and the token usage.
- **Grace**: The seconds the Adapter lets the Review_Session keep running after the Review_File turns final, `RB_FINAL_GRACE_SECONDS`, 60 by default.
- **Interrupt_Wait**: The seconds the Adapter waits after sending the interrupt for the Review_Session to exit on its own, before the kill.
- **Kill**: The `SIGKILL` the Adapter sends to the Review_Session's process group.
- **Wakeup_Tool**: Claude Code's `ScheduleWakeup` tool, which schedules a timer that re-invokes the session.
- **Transcript**: The session file Claude Code writes under the session account's `~/.claude/projects/<project>/<session id>.jsonl`, one JSON row per line.
- **Budget_Row**: A Transcript row of type `attachment` whose `attachment.type` is `budget_usd` and whose `attachment.used` is the session's spend so far in dollars.
- **Findings_File**: The JSON file the Adapter writes for the benchmark, whose `usage` object carries `cost_usd`, `time_in_ms` and `total_tokens`.
- **Adapter_Log**: The `adapter.log` file in the evidence folder beside the Findings_File, one timestamped line per event.
- **System**: The Adapter, the harness script `benchmarks/reviewbench/run.sh` and Makefile that pass variables into the image, their README and the checks under `checks/`.

## Requirements

### Requirement 1: Launch the review session without the wakeup tool

**User Story:** As an Owner, I want the Review_Session unable to schedule a wakeup, so that it exits when its review is done instead of waiting for a timer the Adapter then kills.

#### Acceptance Criteria

1. THE Adapter SHALL pass `--disallowedTools ScheduleWakeup` among the Review_Session's launch arguments.
2. THE Adapter SHALL leave the repair session's launch arguments as they are.
3. THE Adapter SHALL pass the other launch arguments as it does today, in their order, with the new pair added.

### Requirement 2: Interrupt a lingering session before the kill

**User Story:** As an Owner, I want a Review_Session that lingers past the Grace to get an interrupt and a short wait before the Kill, so that a session able to finish on an interrupt prints its Result_JSON and its cost is recorded.

#### Acceptance Criteria

1. WHEN the Review_File has been final for the Grace and the Review_Session is still running, THE Adapter SHALL send `SIGINT` to the Review_Session's process group.
2. WHILE the Interrupt_Wait has not elapsed after the interrupt, THE Adapter SHALL keep reading the Review_Session's stdout and wait for it to exit.
3. WHEN the Review_Session exits within the Interrupt_Wait, THE Adapter SHALL read its Result_JSON from the stdout it collected and treat the session as ended after the Grace, logging that it exited on the interrupt and how many seconds after the Review_File turned final.
4. IF the Review_Session is still running when the Interrupt_Wait elapses, THEN THE Adapter SHALL send the Kill as it does today and log that the interrupt was ignored.
5. THE Adapter SHALL read the Interrupt_Wait from `RB_INTERRUPT_WAIT_SECONDS`, 20 by default, and the harness SHALL pass that variable into the image and the README SHALL list it beside the Grace.
6. THE Adapter SHALL leave the time-limit kill as it is: a Review_Session that reaches `RB_TIMEOUT_SECONDS` gets the Kill with no interrupt first.

### Requirement 3: Recover the cost of a session that printed no result

**User Story:** As an Owner, I want the cost of a killed Review_Session read from its Transcript, so that the run's cost column and total are complete rather than missing the sessions that lingered.

#### Acceptance Criteria

1. WHEN the Review_Session's stdout holds no Result_JSON with a cost, THE Adapter SHALL read the Transcript of the Review_Session and take the `used` value of its last Budget_Row as the Findings_File's `cost_usd`.
2. THE Adapter SHALL find the Transcript as the newest `.jsonl` file directly under the session account's `~/.claude/projects/<project>/` directories, where the session account's home is the one the Review_Session ran with.
3. WHEN the cost is read from the Transcript, THE Adapter SHALL write a line to the Adapter_Log saying that the cost came from the transcript's last budget line and its value.
4. IF no Transcript is found, or the Transcript holds no Budget_Row, or a Budget_Row's `used` is not a number, THEN THE Adapter SHALL leave `cost_usd` absent from the Findings_File as today and log that no cost could be recovered.
5. IF a Transcript row is not valid JSON, THEN THE Adapter SHALL skip that row and go on reading.
6. WHEN the Result_JSON is present, THE Adapter SHALL take its cost as today and read no Transcript for the cost.
7. WHILE `RB_KEEP_TRANSCRIPTS` is not `0`, THE Adapter SHALL recover the cost whether or not the copy of the Transcript into the evidence succeeds, since the Transcript is read from the session account's home.
8. IF `RB_KEEP_TRANSCRIPTS` is `0`, THEN THE Adapter SHALL leave `cost_usd` absent for a Review_Session that printed no Result_JSON and log that no cost could be recovered, since Claude Code then writes no Transcript, and the README SHALL say so under that variable.
9. WHEN the Review_Session's usage has no `cost_usd` and the repair session's result reports one, THE Adapter SHALL leave `cost_usd` absent from the Findings_File rather than record the repair's cost as the whole.
10. WHEN the repair session's result reports a duration, THE Adapter SHALL add it to the Review_Session's measured time before that time is raised to the adapter's own clock, so the repair's seconds are not added on top of the raised floor.

### Requirement 4: Prove and document the change

**User Story:** As an Owner, I want each new path proved by a free check and the README to say what the Adapter does, so that a regression shows in `make validate` and a reader knows why a cost is present after a kill.

#### Acceptance Criteria

1. THE System SHALL hold one check per path in `checks/test_reviewbench_agent.py`: the flag in the review launch arguments and its absence from the repair launch; the cost read from the Transcript's last Budget_Row when stdout has no Result_JSON; no Budget_Row leaving the cost absent; a session that exits on the interrupt within the Interrupt_Wait with its Result_JSON recorded; a session that ignores the interrupt getting the Kill after the Interrupt_Wait.
2. THE System SHALL say in `benchmarks/reviewbench/README.md` that the review session runs without the wakeup tool and why, that a lingering session gets an interrupt and the Interrupt_Wait before the kill, and that a cost absent from the result is read from the transcript's budget line.
3. THE System SHALL build no image and run no benchmark or eval in this task.
