# Implementation Plan

## Overview

The two agent definitions come first, since every other change quotes their shapes: the executor's Summary lines and the wave reviewer's new step and `records:` section. The three launching skills, the documentation and the two new eval cases follow in one wave, each in its own files. Last, a headless session confirms the worktree's copy of the plugin loads and runs the executor once to show the new Summary. Every change is instruction text, so each task is proved by `make validate` and a reading of the changed text against the design; the behaviour is proved by the two eval cases, whose runs cost money and wait for the author's yes.

## Tasks

- [x] 1. The agents
  - [x] 1.1 `plugins/claude/ponderly/agents/task-executor.md`, the Summary
    - In the Summary block, replace the `files changed:` line `- <path>` with the two line shapes of the design's Data Models: `` - `<path>`: <why> `` and `` - `<path>`, `<path>`: <why> ``.
    - In the Summary block, add above the `unsure:` line's existing item the line `` - `<path>`: <a point about that line's change, inferred or unverified> ``.
    - Append to the paragraph after the block one sentence on `files changed`: each path on exactly one line; several paths on one line only for the same change for the same reason; the reason says what changed, and why only when the code does not make it plain or a choice was made; a stopped Summary's partial edit begins its reason with `partial:`; no change reads `files changed: none`.
    - Append to the same paragraph one sentence on `unsure`: an item about the change of one `files changed` line begins with that line's backticked paths and a colon; every other item stays as it is.
    - Change no other sentence of the file: a sibling branch edits it too.
    - Run `make validate`.
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10_
  - [x] 1.2 `plugins/claude/ponderly/agents/wave-reviewer.md`, the record step and the `records:` section
    - Append to step 3 one sentence: the executors' records are not read in steps 1 to 3, and a record never withdraws or softens a finding.
    - Add a new step 4, "Check the records", as the design's key decision describes: read the records the launch quotes; give each `files changed` line one entry, `matches` or `does not match` with the line and the change quoted; give each changed file no line names a `not in any record` entry; settle from the code each `unsure` item of a line that the code can settle, quoted; report a change found wrong as a finding as well; make the reads that settle `unsure` items, where they do not depend on each other, in one message, not one read per turn. With no records in the launch, `records: none given`.
    - Renumber the old step 4 as step 5.
    - In the Findings block, add the `records:` section of the design's Data Models between `findings:` and `unsure:`.
    - Append to the paragraph after the block one sentence: what a `records:` entry holds, and that `verdict` depends only on `findings:`.
    - Run `make validate`.
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9_

- [x] 2. The launching skills
  - [x] 2.1 `plugins/claude/ponderly/skills/implement-spec/SKILL.md`
    - Step 5's reviewer launch: add one bullet, after the files that cite the changed ones, holding the read-after sentence from the design, verbatim, then each task's `files changed` and `unsure` from its Summary, quoted, headed by the task's number.
    - The paragraph that says where the file list and the `unsure` items come from: add that the records of tasks ticked at an earlier hand-back come from that hand-back's report.
    - The collection paragraph after the review: add that a `records:` entry that does not match, a quoted line with no entry and a `not in any record` entry go under the report's problems, quoted; a settled `unsure` item is reported as settled with what the code showed; every other `unsure` item is handled as now; a `not in any record` entry for a file of a task that appeared already done or that the author did by hand is not listed as a problem, since that task has no record: the report shows it under that task's done work as awaiting the author's review, to confirm the change is the one the task intended.
    - Step 6: add that the report shows each task's record under its done work with its checks beside it, and a fix's record beside the record it amends, marked as not reviewed.
    - Step 8's final review launch: add the read-after sentence, verbatim, before the wave reports, which carry the records.
    - Change no other sentence of the file: a sibling branch edits it too.
    - Run `make validate`.
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_
  - [x] 2.2 `plugins/claude/ponderly/skills/readable-code/SKILL.md`
    - Step 6's reviewer launch: add the bullet as in 2.1, each record headed by its File_Group.
    - Step 6's handling of the Findings: the `records:` problems and the settled `unsure` items as in 2.1.
    - Step 7's hand-back: each group's record with its checks, and a fix's record marked as not reviewed.
    - Run `make validate`.
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  - [x] 2.3 `plugins/claude/ponderly/skills/tighten-tests/SKILL.md`
    - Step 9's reviewer launch: add the bullet as in 2.1, each record headed by its File_Group.
    - Step 9's handling of the Findings: the `records:` problems and the settled `unsure` items as in 2.1.
    - Step 10's hand-back list: each group's record with its checks, and a fix's record marked as not reviewed.
    - Run `make validate`.
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [x] 3. The documentation
  - [x] 3.1 `docs/reference.md`: in the task-executor section, what `files changed` and `unsure` now hold; in the wave-reviewer section, the record step and the `records:` section. Run `make validate`.
    - _Requirements: 4.1_
  - [x] 3.2 `docs/guides/make-a-small-change.md` and `docs/guides/build-a-feature.md`: the `files changed` field description and the sequence diagrams' Summary messages say each file comes with its reason; `build-a-feature.md`'s diagram shows the reviewer receiving the records. No semicolon in a Mermaid message. Leave the captures and their SVGs, which are recorded runs. Run `make validate`.
    - _Requirements: 4.2_

- [x] 4. Proof
  - [x] 4.1 Eval case `evals/agents/task-executor/records-each-change/`, in the shape of the existing `done-with-assumptions` case: a scaffold where one task puts the same edit into two files and a different edit into a third; a regex grader for `status: done`; an LLM grader that passes when `files changed` groups the two like files on one line with a reason, gives the third its own line with a reason, and names no file twice. Run `make validate`; do not run the case.
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.3; Property 1_
  - [x] 4.2 Eval case `evals/agents/wave-reviewer/checks-a-wrong-record/`, from the `finds-the-contradiction` scaffold: a correct `subtract` and a second correct file, with a quoted record whose reason for `calc/ops.py` describes something else and that leaves the second file out. An LLM grader passes when the Findings mark the `calc/ops.py` line `does not match` with both quotes, give the second file a `not in any record` entry, and keep the verdict `holds`. Run `make validate`; do not run the case.
    - _Requirements: 2.3, 2.4, 2.5, 2.7, 4.3; Property 3_
  - [x] 4.3 Manual check: from the worktree root, run `claude --plugin-dir plugins/claude/ponderly -p` with the prompt on stdin, first confirming the session loaded this worktree's agent definitions and not the installed 1.8.0 copy, then launching `ponderly:task-executor` on a small two-file change in a scratch repository, and record the Summary it returned.
    - _Requirements: 1.1, 1.9_

## Notes

- In `task-executor.md` and `implement-spec/SKILL.md`, add sentences and bullets; do not reflow, reorder or tidy the rest, so the sibling branches can be merged.
- Quote the design's read-after sentence verbatim wherever a task names it.
- No version bump, no commit, no push, no pull request until the author asks.
- Running `make eval-*` costs money; the eval cases are written here and run only on the author's yes.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1", "2.2", "2.3", "3.1", "3.2", "4.1", "4.2"] },
    { "id": 2, "tasks": ["4.3"] }
  ]
}
```
