# Implementation Plan

## Overview

The plan edits the four prompt files first, each in its own task since each is one file and none reads another's new text, then the two files that describe them, the ReviewBench adapter's schema prompt and `docs/reference.md`, then the eval cases that prove the new behaviour, written but not run, and last the free checks and one headless trial with the worktree's copy of the plugin. Each prompt edit is the wording the design's Components and Interfaces section gives, copied word for word, placed where it says and nowhere else, so the sibling branches can be brought together with this one. The proof is `make validate`, the eval cases run by hand only when the Owner asks, and the trial, which costs about one review and also waits for the Owner's yes.

## Tasks

- [x] 1. Edit the prompt text
  - [x] 1.1 Edit `plugins/claude/ponderly/agents/review-arm.md`
    - The front matter `description` clause, the sentence appended to step 2, the sentence inserted in step 4 after "not how this repository does.", the new first Messages bullet at 150 words, and the `low` and `unsure` clauses of the arm-block notes, each as the design gives them. Touch nothing else: not the `effort:` line, not step 1 or step 3, and no reflow. and the arm-block template's `message:` line. Manual check: `git diff` shows only those six places changed
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 2.1, 2.2, 3.1, 3.3, 6.1_
  - [x] 1.2 Edit the documentation lens in `plugins/claude/ponderly/skills/review/lenses.md`
    - Insert the design's Description sentence before "It carries the category `documentation`". Touch no other lens and not the opening paragraph, which is the shared standard. Manual check: `git diff` shows the one insertion
    - _Requirements: 4.1, 4.2, 4.3_
  - [x] 1.3 Edit the Standard of `plugins/claude/ponderly/agents/wave-reviewer.md`
    - Add ", unless the sentence of those files it breaks implies a graver severity" to the nit sentence of the review-skill paragraph, insert the design's `problem` sentence before "Every launch without that sentence keeps the paragraph above as it stands.", and replace the Findings template's `problem: <one sentence>` line with the design's. Touch nothing else: not the `effort:` line, step 1, step 3, step 4, a `records:` section or any other line of the Findings section. Manual check: `git diff` shows only those three places changed
    - _Requirements: 2.2, 3.2, 3.4, 6.1_
  - [x] 1.4 Edit step 7 of `plugins/claude/ponderly/skills/review/SKILL.md`
    - The description remark lines after the change remark lines in the session reply; a `not_reported` bullet for each `description remark:` entry with `file` `null`, its passage as `quote`, the role and wording as `problem` and `reason` `description remark`, with the split at the first `": ` after the opening quote mark; the fallback for an entry with no straight-quoted passage; the JSON reply and the no-wave-review `not_reported` sentence naming the description remarks beside the change remarks; "in the last of each arm's blocks that the merges took" in place of "in the arm blocks the merges took, once per arm" for both change and description remarks; line breaks in a message or remark written as a space in the session reply; and every `description remark:` entry skipped when the title and body were both "none given". Touch no other step. Manual check: `git diff` shows changes in step 7 alone
    - _Requirements: 4.3, 4.4, 4.5, 6.1_

- [x] 2. Describe the change
  - [x] 2.1 Add `"description remark"` to the `reason` list of the findings schema string in `benchmarks/reviewbench/agent/agent.py`
    - Only the string; no scoring code changes. Manual check: `make validate` passes
    - _Requirements: 4.5_
  - [x] 2.2 Update `docs/reference.md`
    - `review`: the arms read the repository's rule files and report each break their lens covers; each finding's message is what is wrong, the fix and why it matters to the user, operator or owner; the description remark lines after the change remark lines and the `description remark` reason in `not_reported`. `review-arm`: the rule reading in step 2, a rule break as a finding quoting the rule, `low` unless the rule implies more, and the message order: what is wrong, the fix, then the case for the user, operator or owner. `wave-reviewer`: the rule-implied severity and the Case in a review-skill launch. Manual check: each entry agrees with the file it describes
    - _Requirements: 6.2_

- [x] 3. Prove it with eval cases, not run until the Owner asks
  - [x] 3.1 Write the `reports-a-repository-rule-break` case under `evals/agents/review-arm/`
    - In the layout of `names-the-missing-test`: a fixture with a `.claude/rules/` file holding one sentence, such as a naming rule, that the uncommitted change breaks at no other cost; the prompt launches the arm on the maintainability lens; graders: the arm was launched, the lens is named, a finding on the breaking lines at `low` whose message quotes the rule's sentence. Manual check: `make validate` passes and the scaffold builds the fixture in a scratch directory; the case is not run
    - _Requirements: 1.2, 2.2, 6.3, 6.4_
  - [x] 3.2 Write the `remarks-on-the-description` case under `evals/agents/review-arm/`
    - In the layout of `documentation-lens`: a small correct change whose pull request body describes only its mechanism, such as the function it renames and the flag it adds, with no word on what the user sees; the prompt launches the arm on the documentation lens; graders: the arm was launched, the lens is named, an `unsure` entry beginning `description remark:` that names the user, operator or owner, and no finding anchored to a file that is not in the change. Manual check: `make validate` passes and the scaffold builds the fixture in a scratch directory; the case is not run
    - _Requirements: 4.1, 4.2, 6.3, 6.4_
  - [x] 3.3 Add a grader to the `names-the-missing-test` case under `evals/agents/review-arm/`
    - `names-a-role.md`, a regex that the subtract finding's message names `user`, `operator` or `owner`, in the shape of `finds-the-untested-subtract.md`. Leave the prompt and the other graders as they are. Manual check: `make validate` passes; the case is not run
    - _Requirements: 3.1, 6.3, 6.4_
  - [x] 3.4 Update the `documentation-lens` case under `evals/agents/review-arm/` so its prompt quotes the documentation lens as `lenses.md` now reads
    - Leave its graders as they are. Manual check: the quoted lens matches `lenses.md` word for word, and `make validate` passes; the case is not run
    - _Requirements: 6.3, 6.4_
  - [x] 3.5 Write the `no-remark-without-a-description` case under `evals/agents/review-arm/`
    - In the layout of `documentation-lens`, with its fixture, and with title and body both "none given"; graders: the arm was launched, the lens is named, and no `description remark:` line (`not_contains`). Manual check: `make validate` passes and the scaffold builds the fixture in a scratch directory; the case is not run
    - _Requirements: 4.3, 6.3, 6.4_

- [x] 4. Check and try
  - [x] 4.1 Run `make validate`
    - Report the result as it is
    - _Requirements: 6.5_
  - [x] 4.2 Run one headless review with the worktree's plugin, only after the Owner says yes
    - From the worktree root, `claude --plugin-dir plugins/claude/ponderly -p` with the prompt on stdin, on a small scratch repository with a `.claude/rules/` file, a change that breaks it, and no title or body; first confirm from the session that it loaded this worktree's copy and not the installed 1.8.0, and say what showed it. Report whether each arm read the rule file or already had it in context, the finding quoting the rule, one message with its Case, no `description remark:` line, six arm launches and one wave review. Cost about $3.70
    - _Requirements: 1.1, 1.2, 3.1, 4.3, 5.1, 5.2_

## Notes

- No optional test tasks: the eval cases are the proof the requirements name, so none is marked `*`.
- Copy each new sentence from the design's Components and Interfaces section word for word; reflow, reorder or tidy nothing around it, since `launch-model-effort`, `executor-record` and `tests-before-code` change nearby text.
- The `review-skips-no-cost-departures` and `review-skill-second-pass-and-bar` specs are records and are not edited.
- No eval target or benchmark runs in this spec; each case is run by hand, one at a time, only when the Owner asks.
- No change to the plugin version, no commit, no push and no pull request; the author commits.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4", "2.1"] },
    { "id": 1, "tasks": ["2.2", "3.1", "3.2", "3.3", "3.4", "3.5"] },
    { "id": 2, "tasks": ["4.1"] },
    { "id": 3, "tasks": ["4.2"] }
  ]
}
```
