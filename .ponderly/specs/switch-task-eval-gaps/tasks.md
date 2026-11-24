# Implementation Plan

## Overview

The plan repairs the two existing cases, writes the two new ones, adds the README bullet, then checks the whole set free, and ends with the Author's paid runs. The repaired `offers-at-an-unrelated-request` comes before the new offer case, which carries the same earlier work. Every task but the last is proved without a model call: a scaffold is run by hand in an empty scratch directory and its Workspace compared with the prompt, and `make validate` is the full suite at the end of every wave. No task runs an eval case. Task 5.1 is the Author's, and approving this plan does not approve its runs; each waits for the Author's yes when the task is reached.

## Tasks

- [x] 1. Make the two existing workspaces hold what their prompts describe
  - [x] 1.1 Build the finished `subtract` work in `offers-at-an-unrelated-request`
    - In `evals/skills/switch-task/offers-at-an-unrelated-request/`: after `setup.sh calc main`, the scaffold appends `subtract(a, b)` to `calc/ops.py` and its test and import to `tests/test_ops.py`, with the lines `no-offer-for-a-follow-up/scaffold.sh` uses, then copies the case's `files/.` in, all uncommitted. Add `files/.ponderly/specs/subtract/` with a short `requirements.md`, `design.md` and `tasks.md` in the spec template's sections, every task ticked. Update the scaffold's header comment. The prompt and the graders do not change. Ephemeral check: run the scaffold in an empty scratch directory with the environment `evals/README.md` gives; `subtract` is in both files, the spec folder is there, `git status --short` lists all of it as uncommitted, and `python3 -m unittest` passes there
    - _Requirements: 1.1, 1.3, 1.4_
  - [x] 1.2 Build the `visit-counter` spec in `writes-the-compact-line`
    - In `evals/skills/switch-task/writes-the-compact-line/`: after `setup.sh calc main`, the scaffold copies the case's `files/.` in, uncommitted. Add `files/.ponderly/specs/visit-counter/` with a short `requirements.md`, `design.md` and `tasks.md`, tasks unticked, for a `VisitCounter` in `calc/visits.py`; the design states both decisions the prompt carries, counting with `calc.ops.add` so the arithmetic stays in one place, and skipping a repeated `event_id`. Update the scaffold's header comment. The prompt and the graders do not change. Ephemeral check: run the scaffold in an empty scratch directory; the folder holds the three files, `grep` finds `calc.ops.add` and `event_id` in `design.md`, and `git status --short` lists the folder as untracked
    - _Requirements: 1.2, 1.3, 1.4_

- [x] 2. Write the two cases for a skill started by hand
  - [x] 2.1 Write `offers-at-a-skill-started-by-hand`
    - New folder `evals/skills/switch-task/offers-at-a-skill-started-by-hand/` with `case.yaml`, `scaffold.sh` and `files/` as task 1.1 leaves them for its case, and `prompt.md` with the frontmatter the design's Data Models table gives. The prompt opens with `/ponderly:start-task add divide(a, b) to calc/ops.py, raising ZeroDivisionError for a zero divisor, with its test`, then a paragraph, marked as about the session and not part of the task, that describes the finished `subtract` spec run in the words of `offers-at-an-unrelated-request` and says no switch message was shown since. Graders, as the design's table: `offers-the-switch` (`llm`), `speaks-of-switching`, `states-no-route`, `writes-no-file`, `edits-no-file`. Do not run the case. Ephemeral check: the scaffold run as in task 1.1; `make validate` passes
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  - [x] 2.2 Write `no-offer-at-a-skill-started-after-a-small-task`
    - New folder `evals/skills/switch-task/no-offer-at-a-skill-started-after-a-small-task/` with `case.yaml`, a scaffold that builds the plain `calc` fixture on main, and `prompt.md` with the same frontmatter shape. The prompt opens with the same `/ponderly:start-task` command as task 2.1, then a paragraph, marked the same way, that describes the one question answered from `calc/ops.py` in the words of `no-offer-after-a-small-task`. Graders, as the design's table: `makes-no-offer` with the pattern of the two existing no-offer cases, and `states-the-route`. Do not run the case. Ephemeral check: the scaffold run in an empty scratch directory; `make validate` passes
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 3. Put the limit of the hand-off cases in the evals guide
  - [x] 3.1 Add one bullet to `evals/README.md` under "What the sandbox allows"
    - In the guide's own words: `lld/switches-at-the-hand-off` and `bugfix/hands-off-to-pr` grade the call to `ponderly:switch-task` and the decline, because the size hook reads the session's real size and a sandbox session is far under its limit; a session filled to the limit was judged too costly a run; what the hook prints on an allowed call is covered by `checks/test_switch_size.py` and the switch message by `switch-task/writes-the-compact-line`; the size sentence of the message after an allowed call is covered by nothing and shows only in a real session. Manual check: `make validate` passes, which includes `checks/test_docs.py`
    - _Requirements: 4.1, 4.2, 4.3_

- [x] 4. Check the whole set, free
  - [x] 4.1 Compare every `switch-task` prompt with its Workspace, and show nothing shipped changed
    - For each of the seven cases under `evals/skills/switch-task/`, run its scaffold in an empty scratch directory and confirm every path, function and decision the prompt names as earlier work is there; report any that is not, and fix it only in a case this plan changes or adds. Then `git diff --stat $(git merge-base origin/main HEAD) -- plugins/claude/ponderly/skills/switch-task plugins/claude/ponderly/hooks .ponderly/specs/compact-at-task-switch evals/skills/lld/switches-at-the-hand-off evals/skills/bugfix/hands-off-to-pr` prints nothing, and `make validate` passes. Delete the scratch directories
    - **Property 1: A prompt's description is true of its Workspace**
    - **Property 3: The shipped behaviour is untouched**
    - **Validates: Requirements 1.4, 2.1, 3.1, 4.4, 5.1, 5.2**

- [x] 5. The Author's paid runs
  - [x] 5.1 Run the samples, then the confirming run, each on the Author's yes
    - Not run by an executor. First `make eval-skill-switch-task EVAL_ARGS="--runs 1 --case offers-at-a-skill-started-by-hand"`, the case most likely to fail. If it fails because of the case, correct the case and sample again; if the model read the prompt correctly and made no offer, stop and report the trace, changing nothing in the skill. Then the same with `--case no-offer-at-a-skill-started-after-a-small-task`. Then the confirming run, `make eval-skill-switch-task EVAL_ARGS="--runs 3" EVAL_MAX_COST_USD=4`, three runs because four of the seven cases have an `llm` grader. Estimated at about thirteen cents a run from the recorded runs: under $0.30 for the two samples and about $2.70 for the confirming run. Record the scores and the cost here
    - Recorded 2026-11-24: three runs each, all 1.00, for `offers-at-an-unrelated-request`, `writes-the-compact-line`, `no-offer-at-a-skill-started-after-a-small-task`, `clears-for-unrelated-work`, `no-offer-after-a-small-task`, `no-offer-for-a-follow-up` and `lld/switches-at-the-hand-off`. `offers-at-a-skill-started-by-hand` first ran eight times: every reply made the offer and started nothing; four scored under 1.00, one because the cost ceiling skipped its judge and three on wording, which led to two approved edits of Requirement 2.2 and its graders. In its final form it then scored 1.00 on three runs of its own, so Property 2 rests on that run beside the opposite case's three in the confirming run, not on one run holding both. Cost $6.55: $0.71 for four samples, $4.14 for the confirming run, which stopped at its ceiling because the target selects eight cases, $1.20 for the three cases it left, and $0.49 for the final three runs of the offer case
    - **Property 2: The two new cases cannot both pass on one fixed habit**
    - **Validates: Requirements 2.2, 2.4, 3.2, 3.4, 5.3, 5.4**

## Notes

- No task is an optional test: the cases are the tests, and they are the work.
- No task but 5.1 runs `make eval-…`, and 5.1 only on the Author's yes at the time.
- Nothing under `plugins/claude/ponderly/` changes, so the plugin's version does not change.
- A case's scaffold is its own regular, executable file, and its `description` and `expected_outcome` are single-quoted, as `evals/README.md` says.
- Scratch directories for running a scaffold by hand go in the session's scratchpad and are deleted before the task is done. Read their files; run nothing from inside them but the checks a task names.
- The spec files under a case's `files/` are fixture text: true to the prompt, short, and never built.

## Task Dependency Graph

Wave 0 holds the work that shares no file. Task 2.1 follows 1.1 because it copies that case's scaffold and spec folder. The free check reads everything, and the paid runs come last.

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "2.2", "3.1"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["4.1"] },
    { "id": 3, "tasks": ["5.1"] }
  ]
}
```
