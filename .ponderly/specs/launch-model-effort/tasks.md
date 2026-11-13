# Implementation Plan

## Overview

The agent files change first, because the skills name what they define:
- the frontmatter levels;
- the Small_Task test in the Executor's description.

The reviewers' Gathering_Steps follow in the next wave, so that no two tasks edit one agent file at once.

The eight Launching_Skills change next, one task per skill, except for `strategy`, `hld` and `lld`, which change alike in one task. Each skill task writes three sentences in that skill's own words:
- the Effort_Proposal at the place the design's table names;
- the `model` and `effort` on its launches, with the retry without `effort`;
- for the four Executor_Skills, the Escalation.

The reference entries follow the text they describe. A last task is the headless trial with `--plugin-dir`.

Instruction text has no unit tests in this repository, so each task is proved by `make validate` and a dry run of the new text on one concrete case, read only. No `make eval-*` target runs.

In `plugins/claude/ponderly/agents/task-executor.md` and `plugins/claude/ponderly/skills/implement-spec/SKILL.md`, two sibling branches change other sentences at the same time. Tasks touching those files change only the sentences named, with no reflow, reorder or tidying.

## Tasks

- [x] 1. Set the agents' levels and the Small_Task test
  - [x] 1.1 Set `effort: medium` in the frontmatter of `review-arm.md`, `document-reviewer.md` and `wave-reviewer.md` under `plugins/claude/ponderly/agents/`
    - Change only the `effort:` line of each file. Leave `model: sonnet` in `review-arm.md` and `document-reviewer.md`, and `model: opus` in `wave-reviewer.md`. Leave `task-executor.md` alone; it already has `model: sonnet` and `effort: medium`. Manual check: `make validate` passes, and `rg -n '^(model|effort):' plugins/claude/ponderly/agents </dev/null` shows `effort: medium` four times and `opus` once, on `wave-reviewer.md`
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  - [x] 1.2 Add the Small_Task test to the `description` of `plugins/claude/ponderly/agents/task-executor.md`
    - Append to the description, in its own words, the design's Small_Task test and the instruction to launch on `haiku` for a Small_Task, on `sonnet` otherwise, and on `sonnet` when the size is unclear. Change no other line of the file. Manual check: `make validate` passes, which holds the description under 1,024 characters. A dry run of the test sorts a one-file wording change as small and a new function with its test as not small
    - _Requirements: 2.1, 2.2, 2.3_
  - [x] 1.3 Make the Wave_Reviewer's step 1 gather in one diff and batched reads
    - In step 1 of `plugins/claude/ponderly/agents/wave-reviewer.md` only, replace "For each listed tracked file run `git diff <base> -- <path>`" with one `git diff <base> -- <path> ...` over every listed tracked file. Add that reads which do not depend on each other go in one message. Restate the missing-input clause "a `git diff` that fails or that comes back empty against the base for a listed file `git status` does not show as new" for a listed file absent from that one diff's output. Change nothing outside step 1. Manual check: `make validate` passes. A dry run of step 1 on a launch listing three tracked files and one new file gives one `git diff` call and one message of reads
    - _Requirements: 6.1, 6.3, 6.4_
  - [x] 1.4 Make the Lens_Arm's step 1 gather in one diff and batched reads
    - In step 1 of `plugins/claude/ponderly/agents/review-arm.md` only, replace "run `git diff <base> <head> -- <path>` for each changed file" with one command over every changed file, and the working-tree form likewise. Add that reads which do not depend on each other go in one message. Change nothing outside step 1. Manual check: `make validate` passes. A dry run of step 1 on a two-commit range with three changed files gives one `git diff` call
    - _Requirements: 6.2, 6.3, 6.4_

- [x] 2. Choose the Executor's model, escalate and propose the effort in the four Executor_Skills
  - [x] 2.1 Change `plugins/claude/ponderly/skills/implement-spec/SKILL.md`
    - In step 4, add an `Effort` question to the set-up AskUserQuestion call. Its layout text gives the proposal for the run's executor and Wave_Reviewer launches by the design's High_Effort_Criteria, and the cost line for high. When step 4 asks no question, the proposal is stated in its "where things stand".
    - In step 5, replace "Each agent runs on the model its own definition pins" with the design's sentence.
    - At "Launching a task", name the Launch_Model beside the task's number, and pass `model` by the Executor's Small_Task test and `effort` only when it is not medium, with the retry without `effort`.
    - Before the `stopped` rule's "do not relaunch or retry the task unprompted" and the two fix-attempt paths, add the Escalation for a Haiku launch: a new executor on `sonnet`, as the first fix attempt where there are two.
    - Pass the step 4 effort on Wave_Reviewer launches only when it is not medium.
    - Change no other sentence.
    - Manual check: `make validate` passes. A dry run of steps 4 and 5 on this spec's own `tasks.md` at wave cadence asks the `Effort` question with medium proposed, launches task 1.1 on `haiku`, and on a `stopped` Summary from it launches a new executor on `sonnet` without asking
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8_
  - [x] 2.2 Change `plugins/claude/ponderly/skills/start-task/SKILL.md`
    - On Executor_Route, the route statement names the Launch_Model and the Effort_Proposal, and the free-text answer to `Route` can change the level. The launch passes `model`, and `effort` only when it is not medium, with the retry. Before the `Relaunch` question, a `stopped` Summary from a Haiku launch gets one Escalation, with its `stopped because` quoted and the files holding partial edits under Author's additions; the `Relaunch` question follows only if the Sonnet launch stops too. Update the Stops line to match. The launch still never says the task comes from a spec. Manual check: `make validate` passes. A dry run on a one-line wording change gives a route statement naming `haiku` and medium
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 5.4, 5.6, 5.8_
  - [x] 2.3 Change `plugins/claude/ponderly/skills/readable-code/SKILL.md`
    - In step 3's message, before the `Groups` question, state the Effort_Proposal for the executors and the Wave_Reviewer. The free-text answer can change it. In step 4, each group's launch passes `model` by the Small_Task test, and `effort` only when it is not medium, with the retry. The `stopped` rule "Do not relaunch it or work around it" is preceded by one Escalation for a Haiku launch. A step 6 fix of Haiku work goes to a new executor on `sonnet`, never as a follow-up to the Haiku one. Manual check: `make validate` passes. A dry run on a branch with one group of two files launches it on `sonnet`
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 5.4, 5.6, 5.8_
  - [x] 2.4 Change `plugins/claude/ponderly/skills/tighten-tests/SKILL.md`
    - In step 5's message, before the `Approve` question, state the Effort_Proposal for the executors and the Wave_Reviewer. The free-text answer can change it. In step 6, each File_Group launch passes `model` by the Small_Task test, and `effort` only when it is not medium, with the retry. A `stopped` Summary or a Shortfall from a Haiku launch gets one Escalation, and every relaunch "as in step 6" of Haiku work runs on `sonnet`. Manual check: `make validate` passes. A dry run on one group whose Verdicts drop one test from one file launches it on `haiku`
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 5.4, 5.6, 5.8_

- [x] 3. Propose the effort in the reviewer-only skills
  - [x] 3.1 Change `plugins/claude/ponderly/skills/review/SKILL.md`
    - At step 3, before the arms launch, state the Effort_Proposal for the Lens_Arms and the Wave_Reviewer by the High_Effort_Criteria, taking a level named in the request. Pass `effort` on those launches only when it is not medium, with the retry without it. Add no stop. Manual check: `make validate` passes. A dry run on a range reviewed outside the session that built it, with an empty pull request body, no issue and no spec, proposes high for the reviewers, with the criterion and the cost line; the same range reviewed in the session that built it proposes medium
    - _Requirements: 1.5, 5.1, 5.2, 5.3, 5.5, 5.6, 5.8_
  - [x] 3.2 Change `plugins/claude/ponderly/skills/strategy/SKILL.md`, `skills/hld/SKILL.md` and `skills/lld/SKILL.md` alike
    - In each step 3, add the Effort_Proposal for the Document_Reviewer launches to the prose round, or state it when nothing is left to ask. In each step 5, pass `effort` on the launch only when it is not medium, with the retry. Manual check: `make validate` passes. A dry run of `hld` with `Parent: none` proposes high by criterion 4
    - _Requirements: 1.5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.8_

- [x] 4. Document the change
  - [x] 4.1 Update `docs/reference.md` and the plugin's `README.md` where they describe what changed
    - Fix each entry that describes the agents' models or effort, `implement-spec`'s set-up questions, a skill's handling of a stopped executor, or the reviewers' gathering. Fix any stale cross-reference found in those entries. Change no entry for anything else. Manual check: `make validate` passes, and each changed entry agrees with the file it describes
    - _Requirements: 1.1, 3.1, 5.1, 6.1_

- [x] 5. Try the changed plugin headless
  - [x] 5.1 Run the design's headless trial with `claude --plugin-dir plugins/claude/ponderly`, and record what was seen
    - From the worktree root, with each prompt piped on stdin, first confirm the session loaded this worktree's agents: the Executor's description shows the Small_Task test. Then, in a scratch repository under the scratchpad, run `start-task` on a one-line wording change and on a contained change that adds a function. Read each sub-agent transcript's `model` field, expecting Haiku and then Sonnet. Then run `review` on a two-file range with "run the reviewers at high" in the request, and read the arms' effort in their transcripts. Say what was seen, including which Haiku model the alias gave. Delete the scratch repository. This task makes real model calls; say so to the author before running it
    - _Requirements: 1.1, 2.1, 2.2, 5.5, 5.6_

## Notes

- Write each skill's sentences in that skill's own voice. Name the Executor's Small_Task test and the design's High_Effort_Criteria; do not paste another skill's steps.
- The High_Effort_Criteria and the cost line go into each skill as the design gives them. The cost line says its dollars are list prices, not what a subscription bills.
- No check greps a prompt for these values. Behaviour is proved by the dry runs here and the trial in 5.1; no `make eval-*` target runs without the author's go.
- The before-and-after comparison of tokens and turns runs about a week after the change is installed, outside this plan. Issue #501 in sabind/dansabin waits on it.
- No commit, push, pull request or version bump.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["1.3", "1.4", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2"] },
    { "id": 2, "tasks": ["4.1"] },
    { "id": 3, "tasks": ["5.1"] }
  ]
}
```
