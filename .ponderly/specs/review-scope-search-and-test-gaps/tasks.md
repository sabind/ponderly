# Implementation Plan

## Overview

The prompt edits come first and touch separate files: the Shared_Standard and testing lens in `lenses.md`, the arm in `review-arm.md`, and the skill in `SKILL.md`. The review file's consumers, the Adapter's shape string and Review_Health, follow in the same wave since they touch other files. The arm eval prompts are re-quoted after the standard lands and the docs after the behaviour they describe. The four eval cases ran in wave 2; the search switch, its records, the report headers and their checks were added by approved edits and ran in waves 2 to 6. Task 1.11 was removed with requirement 5.10. Nothing is run beyond `make validate` and each task's stated check: every eval case is written and scaffolded and runs only when the Owner asks.

## Tasks

- [x] 1. Change the prompts
  - [x] 1.1 Edit the Shared_Standard and the testing lens in `plugins/ponderly/skills/review/lenses.md`
    - After "A pre-existing problem in a touched file counts when it is verifiable.", add "A file the pull request moved or renamed is touched in every line, so a problem on any of its lines is a finding at that line." In the `## testing` section, add after its first sentence "Before reading the tests, the arm lists each behaviour the change introduces or alters, finds the test that would fail if that behaviour broke, and reports each behaviour with none at the behaviour's own place in the code, though the edit it needs goes in a test.", and change its true-positive sentence to "A true positive names the behaviour, the place it lives and the test that would cover it, or the test that is wrong and how, in the project's own test framework and style." Change no other sentence. Manual check: `git diff` shows only those three sentences changed
    - _Requirements: 1.1, 1.6, 4.1, 4.2, 4.3, 4.5_
  - [x] 1.2 Edit `plugins/ponderly/agents/review-arm.md`
    - Frontmatter `tools:` gains `WebSearch`. Step 1: a file the launch marks moved shows no diff and is still read whole in step 2. Step 2: "Read every changed file whole" gains "a moved file included, since the standard counts its every line". Step 3: "in the unchanged code of the files the pull request touches" gains "a moved file's every line included". Step 4: the search sentences of the design's Review_Arm table, naming "a web search tool" and never `WebSearch`, with the query rule, the never-open rule, the per-copy consequence and the unverified fallback. Arm block: `read:` after `unsure:` with the entry forms of the design's Data Models, and the paragraph after the block defines it. Manual check: `git diff` shows only those places changed; the frontmatter parses with `make validate`
    - _Requirements: 1.2, 1.3, 1.5, 2.1, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  - [x] 1.3 Edit steps 2, 3, 4, 6 and 7 of `plugins/ponderly/skills/review/SKILL.md`
    - As the design's Review_Skill table says: moved files found with `git diff --name-status -M` and marked in the launch's changed-file list; the arm-block test gains the `read:` list; the interim, early-stop and final objects carry `read` and `counts.files_unread`, nine count entries required; the second pass unites Read_Lists per lens; the count line gains `touched files no arm read <n>`, with absent-at-head files excluded and paths normalised as step 4 does. `allowed-tools` already grants `git diff`. Manual check: `git diff` shows only those places; the step 4 JSON block parses with `python3 -c 'import json,sys; json.loads(sys.stdin.read())'`
    - _Requirements: 1.2, 2.2, 2.3, 2.4, 2.7_
  - [x] 1.4 Edit `FINDINGS_SHAPE` in `benchmarks/reviewbench/agent/agent.py`
    - `"files_unread": integer` joins `counts` and `"read": {lens: [string]}` joins the object's fields; change nothing else in the Adapter. Check: `make validate`
    - _Requirements: 2.5_
  - [x] 1.5 Add the unread line to Review_Health in `benchmarks/reviewbench/report.py`
    - One `recorded_total_line("Touched files no arm read", readable, "files_unread")` after the departures line; the section's opening paragraph names the new count among those older files lack; `files_unread` stays out of `COUNT_FIELDS`. Check: `python3 -m unittest checks.test_reviewbench_report`
    - _Requirements: 2.6_
  - [x] 1.6 Add `RB_SEARCH` to the review launch in `benchmarks/reviewbench/agent/agent.py` and the harnesses
    - Unless `RB_SEARCH` is `1`, `WebSearch` joins `ScheduleWakeup` after `--disallowedTools` in the review launch; the repair launch is unchanged. Pass `-e RB_SEARCH` beside `-e RB_INTERRUPT_WAIT_SECONDS` in `benchmarks/reviewbench/run.sh` and `benchmarks/martian/run.sh`, and name it in the `benchmarks/reviewbench/Makefile` header comment and `benchmarks/martian/run.sh`'s header. Ephemeral check: import the adapter and show the review arguments with `RB_SEARCH` unset and with `1`; `bash -n` on both scripts
    - _Requirements: 3.10, 3.11_
  - [x] 1.7 In step 4 of `plugins/ponderly/agents/review-arm.md`, a refused or failed search is unsettled
    - The unverified fallback names a search the host refuses or that fails beside having no search tool. Manual check: `git diff` shows only that sentence changed
    - _Requirements: 3.12_
  - [x] 1.8 Give the search eval case a target of its own
    - Move `evals/agents/review-arm/settles-a-third-party-claim/` to `evals/agents/review-arm-search/settles-a-third-party-claim/`; in the root `Makefile`, `eval-agent-review-arm-search` grants `--allow-tools Bash WebSearch --scaffold` with the `bin` PATH, and `eval-agent-review-arm` goes back to `--allow-tools Bash --scaffold`. Check: `make -n eval-agent-review-arm-search` and `make -n eval-agent-review-arm` print the right grants; `make validate`
    - _Requirements: 5.9_
  - [x] 1.9 Record search in the adapter and the run
    - `adapter.log` gains `search on` or `search off` beside the model line; `benchmarks/reviewbench/run.sh` writes `search` into `run.json` from `RB_SEARCH`, `false` when unset. Ephemeral check: the adapter's log line both ways; `bash -n`
    - _Requirements: 3.13_
  - [x] 1.10 Record search in the Martian run
    - `benchmarks/martian/run.sh` writes `search` into its `run.json` from `RB_SEARCH`, true only when it is `1`, as the ReviewBench harness does. Ephemeral check: the jq expression both ways; `bash -n`
    - _Requirements: 3.13_
  - [x] 1.12 Show search in the ReviewBench report header
    - In `benchmarks/reviewbench/report.py`'s `header_section`, add `- Search: on` or `- Search: off` after the Effort line, from `run_info.get("search")`, off when missing. Check: `python3 -m unittest checks.test_reviewbench_report`
    - _Requirements: 3.14_
  - [x] 1.13 Show search in the Martian report header
    - In `benchmarks/martian/report.py`, the "Image settings" line gains `search on` or `search off` the same way. Check: `python3 -m unittest checks.test_martian_report`
    - _Requirements: 3.14_

- [x] 2. Prove the report line
  - [x] 2.1 Add one test to `checks/test_reviewbench_report.py`
    - A run of two review files, one with `files_unread` 3 and one without it, prints "Touched files no arm read: 3 on 1 pull request(s) (recorded by 1 of 2 review files)". Follow the module's existing tests. Check: `make validate`
    - _Requirements: 2.6_
  - [x] 2.2 Add two checks for `RB_SEARCH` to `checks/test_reviewbench_agent.py`
    - By default the review launch's `--disallowedTools` holds `WebSearch`; with `RB_SEARCH=1` it does not, and holds `ScheduleWakeup` still. Follow the existing launch-argument test's form. Check: `make validate`
    - _Requirements: 3.10_
  - [x] 2.3 One check in `checks/test_reviewbench_agent.py` that `adapter.log` says `search off` by default and `search on` with `RB_SEARCH=1`
    - Follow the existing adapter-log tests' form. Check: `make validate`
    - _Requirements: 3.13_
  - [x] 2.4 One check in `checks/test_reviewbench_report.py` that a run recording `search` true prints `Search: on` and one recording none prints `Search: off`
    - One test per path, following the module's header tests. Check: `make validate`
    - _Requirements: 3.14_
  - [x] 2.5 The same checks in `checks/test_martian_report.py`
    - One test per path, following the module's header tests. Check: `make validate`
    - _Requirements: 3.14_

- [x] 3. Re-quote and document
  - [x] 3.1 Re-quote the Shared_Standard in the six arm prompts under `evals/agents/review-arm/`
    - `security-lens`, `documentation-lens`, `finding-at-each-own-edit-place`, `finding-in-each-copy`, `reads-a-new-dependency-whole` and `one-note-for-a-change-remark`: replace the quoted standard with the paragraph as `lenses.md` now holds it, from the sentence that begins "Across every lens, a finding worth reporting" to its end, and nothing else. Read each case's graders and confirm none parses the arm block's full shape, so none needs the `read:` field. Manual check: each quoted span is byte-equal to the file's, shown by extracting both and running `diff`
    - _Requirements: 5.5, 5.6_
  - [x] 3.2 Update `docs/reference.md`, `plugins/ponderly/README.md`, `llms.txt` and `benchmarks/reviewbench/README.md`
    - As the design's Documentation table says. Manual check: each entry reads in order, names no benchmark in the plugin's own docs, and keeps the file's line width
    - _Requirements: 3.8, 5.7_
  - [x] 3.3 Document `RB_SEARCH` and the permission prompt
    - `RB_SEARCH` in the ReviewBench README's list of variables recorded in `run.json`, as `search`, and in the Martian README's variable list, `0` by default, and what `1` does; the `review-arm` entry of `docs/reference.md` and the plugin README's review-arm line say that by hand a search is the host's permission prompt, asked on first use. Correct the ReviewBench README's paragraph on the session's tools, which says the arms can use `WebSearch`, to say they cannot unless `RB_SEARCH` is `1`; and say in the reference's review-arm entry that a refused or failed search also ends in an unverified `unsure` entry. Manual check: line width kept; `make validate`
    - _Requirements: 3.9, 3.11_

- [x] 4. Prove it with eval cases, written and scaffolded but not run
  - [x] 4.1 Write `evals/agents/review-arm/reads-a-moved-file-whole/`
    - As the design's Testing Strategy says, on the calc fixture in the siblings' form (`case.yaml`, `scaffold.sh`, `files/`, `prompt.md` quoting the standard and the correctness lens verbatim, `graders/`). The moved module already holds a verifiable defect at a known line; the prompt lists it with `(moved from <old path>, unchanged)`. Graders: `launches-the-arm`, `names-lens`, a finding at the moved path's defect line, `read:` naming the moved path with `whole`. Manual check: `bash scaffold.sh` in a scratch directory leaves the move and the one edit as the only changes, and `git diff --name-status -M` shows the move as `R100`; `make validate` parses the case
    - _Requirements: 5.1_
  - [x] 4.2 Write `evals/agents/review-arm-search/settles-a-third-party-claim/`
    - As the design's Testing Strategy says: two GitHub Actions workflow files, each with both `branches` and `branches-ignore` on the same `push` event, correctness lens, `allowed_tools` granting `WebSearch` beside the siblings' grants,. Graders: a finding on each workflow file; no `WebSearch` input in the trace holding either workflow's file name or the fixture's repository name (see `evals/README.md` for trace graders). Manual check: `bash scaffold.sh` in a scratch directory leaves the two workflows uncommitted; `make validate` parses the case The case runs under its own target, `eval-agent-review-arm-search`, as task 1.8 set it up.
    - _Requirements: 5.2_
  - [x] 4.3 Write `evals/agents/review-arm/names-the-missing-test/`
    - As the design's Testing Strategy says, on the calc fixture with the testing lens quoted verbatim from the edited `lenses.md`: a new operation with no test, and a change to an existing operation that its existing test already covers. Graders: a finding at the new operation that names a test for it; no finding at the covered operation. Manual check: `bash scaffold.sh` leaves only those changes; `make validate` parses the case
    - _Requirements: 5.3_
  - [x] 4.4 Write `evals/skills/review/counts-the-files-no-arm-read/`
    - As the design's Testing Strategy says, on the shop fixture with one moved file and one edited one, `review.json` appended to `.git/info/exclude` in the scaffold as `writes-the-final-counts` does, prompt `/ponderly:review --json review.json`. Graders on the file: `"read": *\{\s*"[a-z]+": *\[` and `"files_unread":`; on the reply: `touched files no arm read`. Manual check: `bash scaffold.sh` leaves the move and the edit; `make validate` parses the case
    - _Requirements: 5.4_

## Notes

- Every prompt edit is the smallest wording that says the rule; no sentence is restyled.
- No eval case and no benchmark is run in this spec; the measure is a chunk 3 rerun on the subscription token, the Owner's call afterwards.
- Under `benchmarks/` the adapter, both `run.sh` files, the ReviewBench Makefile, both `report.py` files and both READMEs change, as the tasks say.
- `rg` needs an explicit path and `</dev/null`; never bare `git stash`; commit nothing.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4", "1.5"] },
    { "id": 1, "tasks": ["2.1", "3.1", "3.2"] },
    { "id": 2, "tasks": ["1.6", "1.7", "4.1", "4.2", "4.3", "4.4"] },
    { "id": 3, "tasks": ["1.8", "1.9"] },
    { "id": 4, "tasks": ["1.10", "2.2", "3.3"] },
    { "id": 5, "tasks": ["1.12", "1.13", "2.3"] },
    { "id": 6, "tasks": ["2.4", "2.5"] }
  ]
}
```
