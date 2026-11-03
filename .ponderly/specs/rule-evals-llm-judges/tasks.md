# Implementation Plan

## Overview

The grader edits, the new case and the version bump come first, since they are independent files. `make validate` follows, then a one-run trial of each judged case to read its verdicts, then the five Ablation_Runs one at a time, then the evidence page. The evals are the tests: the properties are proved by the trial runs and the Ablation_Runs, and `make validate` proves the cases are well formed.

## Tasks

- [x] 1. Judge the communication cases
  - [x] 1.1 Add `evals/rules/communication/lays-out-before-asking/graders/lays-out-in-uploader-terms.md` and delete `uploader-before-the-options.md` and `recommends-in-prose.md`; update the case's `description` and `expected_outcome` if they name a deleted grader's check
    - The bar names the dropped file to send again and the wait behind a failing job, requires a recommendation with its reason before the options, and fails a pasted README table
    - _Requirements: 1.1, 1.3, 1.4, 1.5_
  - [x] 1.2 Add `evals/rules/communication/user-effect-before-mechanism/graders/subscribers-see-it-first.md` and delete `user-before-mechanism.md` and `does-not-open-with-mechanism.md`
    - The bar names a subject line cut off mid-word in subscribers' inbox, said before `test_render_subject_width`, `render_subject` or any path
    - _Requirements: 1.2, 1.3, 1.4, 1.5_

- [x] 2. Judge the collaboration case
  - [x] 2.1 Add `evals/rules/collaboration/one-open-decision-at-a-time/graders/lays-out-backoff-as-customers-live-it.md`; delete no grader
    - The bar names a customer's import burst and throttled uploads under fixed and exponential, with a recommendation and its reason, and fails a description of the backoff formula alone
    - _Requirements: 2.1, 2.2, 2.3, 1.5_

- [x] 3. Add the library-choice case
  - [x] 3.1 Add `evals/rules/communication/names-library-choice-by-what-visitors-see/` with `prompt.md`, `case.yaml`, `scaffold.sh`, `files/README.md`, `files/gallery/thumbs.py` and `files/tests/test_thumbs.py`, in the shape of `lays-out-before-asking`
    - README holds the table in design.md's Data Models; `thumbs.py` loads thumbnails one after another with `requests`
    - _Requirements: 3.1, 3.5_
  - [x] 3.2 Add its graders: `lays-out-as-visitors-see-it.md` (llm), `offers-requests.md`, `offers-httpx.md` and `thumbs-left-alone.md` (regex on the file)
    - _Requirements: 3.2, 3.3, 3.4, 3.5_

- [x] 4. Bump the plugin version to 1.6.1 in `plugins/ponderly/.claude-plugin/plugin.json`
  - _Requirements: 7.1_

- [x] 5. Prove the cases
  - [x] 5.1 Run `make validate` and fix any failure
    - _Requirements: 4.1, 4.2_
  - [x] 5.2 Run each of the four judged cases once with the plugin (`--runs 1 --case <name>`), one at a time, and read each last message against its judge's verdict; report a verdict that reads wrong to Dan before going on
    - Counts towards Eval_Spend
    - _Requirements: 1.1, 1.2, 2.1, 3.2, 3.3_

- [x] 6. Rerun the rule evals with and without the plugin
  - [x] 6.1 `make eval-rule-collaboration EVAL_ARGS="--ablation with-without --runs 3" EVAL_MAX_COST_USD=12`
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6, 5.7_
  - [x] 6.2 `make eval-rule-communication`, same flags
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6, 5.7_
  - [x] 6.3 `make eval-rule-code-changes`, same flags
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6, 5.7_
  - [x] 6.4 `make eval-rule-tests`, same flags
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6, 5.7_
  - [x] 6.5 `make eval-rule-workflow`, same flags
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 7. Update `docs/evidence.md` with the rule tables introduced as an adherence check, one sentence on why they are not a benchmark, a pointer to ReviewBench and Martian as the evidence with an outside answer key, the five tables under 2026-11-03 / plugin 1.6.1 headings, the per-case note on what each grader can and cannot compare, the Routing_Grader notes, the judged-case paragraph, `tests` moved out of Not measured, and the rule-change list removed
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.2_

## Notes

- Grader bodies follow `evals/rules/code-changes/one-job-functions/graders/one-job-per-function.md`: one sentence on what the text is, a PASS paragraph, a FAIL paragraph. Single-quote any frontmatter value with `: ` or ` #`.
- Evals run one at a time in the background, never two at once. Before each, add up the COST lines printed so far; if the next estimate would pass $35, stop and ask Dan.
- A 300-second timeout with one api_retry and little cost is an API stall: rerun that target alone.
- Do not touch `~/.claude/plugins/` or the other worktrees. Commit nothing.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "2.1", "3.1", "4"] },
    { "id": 1, "tasks": ["3.2"] },
    { "id": 2, "tasks": ["5.1"] },
    { "id": 3, "tasks": ["5.2"] },
    { "id": 4, "tasks": ["6.1"] },
    { "id": 5, "tasks": ["6.2"] },
    { "id": 6, "tasks": ["6.3"] },
    { "id": 7, "tasks": ["6.4"] },
    { "id": 8, "tasks": ["6.5"] },
    { "id": 9, "tasks": ["7"] }
  ]
}
```
