# Implementation Plan

## Overview

A gate comes first: this change is written on top of the `review-skips-no-cost-departures` and `review-documentation-lens` specs, so it checks both are built before touching a file. Then the instruction files change, the Shared_Standard and the Review_Arm together with the merge and cap edits of the Review_Skill, and step 5 and 6a of the Review_Skill after them, then the cap's removal from it, so that no two tasks edit `SKILL.md` at once; the benchmark's limit and report line go alongside. The reference entries follow the text they describe, and the eval prompts follow the Shared_Standard they quote. Instruction text has no unit tests here: each task is proved by `make validate` and a dry run of the new text on the ReviewBench evidence the design cites, read only; the eval cases are written and their scaffolds built, never run until the Owner asks. A last task checks that the Wave_Reviewer's definition and the Launch_Sentence came through untouched.

## Tasks

- [x] 1. Check that the two specs this change builds on are built
  - Read `.ponderly/specs/review-skips-no-cost-departures/tasks.md` and `.ponderly/specs/review-documentation-lens/tasks.md`. If any task in either is unticked, stop and say which spec and task are unfinished; do not start task 2. The one exception is the documentation-lens spec's task 3.2 and its parent task 3, which wait for this change and whose re-quoting tasks 5.1 and 5.2 here do; leave them unticked, and say in task 6.1's report that the Owner can tick them. Confirm that step 5 of `plugins/ponderly/skills/review/SKILL.md` holds the Launch_Sentence word for word as the design quotes it, that `lenses.md` has a `## documentation` section, and that `evals/agents/review-arm/documentation-lens/` exists. Record the hash of `plugins/ponderly/agents/wave-reviewer.md` (`git hash-object`) for task 6.1. Manual check: the three confirmations and the hash are in the task's report
  - _Requirements: 10.1, 10.3_

- [x] 2. Put the place rule in the Shared_Standard and the arm's procedure
  - [x] 2.1 Extend the Shared_Standard in `plugins/ponderly/skills/review/lenses.md`
    - Append the design's five sentences, word for word, after "A pre-existing problem in a touched file counts when it is verifiable.", in the same paragraph. In the paragraph's first sentence change "the three sentences of this paragraph" to "the sentences of this paragraph". Change no `##` section. Manual check: `make validate` passes, and a dry run of the new standard on the evidence (`b-judge-boundary.md` and `d-cross-file-defects.md` under `.git/benchmark-data/review-investigations/`) places AY2526S2's stub at `DeleteNoteCommand.java:35` and `Model.java:175`, CrabTrap's 503 only at `AuditTrail.tsx:113`, NCATSTranslator G18 at `gtopdb.py:145`, figlet's narrowed filters in six workflows, and splits CrabTrap's `context.Background()` sentence into its own finding at `pg_audit_reader.go:370`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.1, 2.2, 2.3, 2.4_
  - [x] 2.2 Change steps 2 to 5 and the `unsure` rule of `plugins/ponderly/agents/review-arm.md`
    - Make the six edits of the design's Review_Arm table, word for word: the New_Dependency sentence after step 2, the Sweep sentence after step 3, the "no problem twice at the same place" carve-out in step 4, the bar in step 4 naming `AGENTS.md` and `.claude/rules/` files as the Launch_Sentence does, step 5 reduced to the smallest-range rule with the 1f0f3ef two-place sentence removed, and the arm block's `unsure` sentence with the `outside lens:` prefix. Change nothing else, the description and the Second pass section included. Manual check: `make validate` passes, and a dry run of step 2 on CrabTrap's handler (`internal/admin/api.go` at 5ef0884, read in the run's checkout only if present, else from `a-missed-highs.md`) reaches the `evalStore == nil` guard at line 1046 and names the configuration without an LLM judge
    - _Requirements: 1.9, 3.1, 3.2, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 8.1, 8.5, 10.5_

- [x] 3. Keep the set through the Review_Skill and record the reviewer's share
  - [x] 3.1 Change the merge, the Cap, the Terms and the JSON counts in `plugins/ponderly/skills/review/SKILL.md`
    - Make the design's Review_Skill edits outside step 5 and step 6a, word for word: the description's "at most 80"; the Terms' "the sentences of that file's opening paragraph"; step 2's no-diff counts with `folded`, `not_anchored` and `relaunched`; step 4.3's `same-defect` exemption for candidates that name each other; the Cap of 80 in step 4.5, in step 4's counts paragraph and in both places of step 6e; and step 7's `--json` counts sentence. Leave the `keep` and `overlap` modes, the Count_Line and everything the skips spec added as they are. Manual check: `make validate` passes; no "40" remains in the file as a cap (`rg -n '\b40\b' plugins/ponderly/skills/review/SKILL.md </dev/null`); and a dry run of steps 4 and 7 on chunk 3's AY2526S2 `review.json` (read only), with two findings added by hand at `DeleteNoteCommand.java:35` and `Model.java:175` naming each other, keeps both and gives `counts.not_anchored` equal to the `not anchored` entries of `not_reported`
    - _Requirements: 1.9, 6.1, 6.2, 6.3, 6.4, 6.5, 9.1, 9.2, 9.3, 9.4, 9.5_
  - [x] 3.2 Add the place and quote rule and the arms' leads to step 5, and the sort rule to step 6a, of `plugins/ponderly/skills/review/SKILL.md`
    - After the Launch_Sentence bullet, which stays word for word, add the design's two bullets, word for word: the place-and-quote sentence and the arms' leads with their "No leads." case. In step 6a, after "Any other reviewer finding is **new**.", add the design's sentence on a finding at another place. Change nothing in `plugins/ponderly/agents/wave-reviewer.md`. Manual check: `make validate` passes; the Launch_Sentence is unchanged (`git diff` shows no line removed from it); and a dry run of step 5 on chunk 3's nebula and jadx arm blocks (read only, from the investigation's quotes in `a-missed-highs.md`), with their outside-lens `unsure` entries rewritten with the `outside lens:` prefix, quotes the `with_keys` alias and the off-EDT read as leads
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.1, 8.2, 8.3, 8.4, 8.5, 10.2_

- [x] 4. Document the change
  - [x] 4.1 Update the `review` and `review-arm` entries of `docs/reference.md`
    - Make the design's Documentation table edits: the Cap's removal in both `review` paragraphs, the `same-defect` exemption, the place rule, the wave review's place and quote rule and leads, the three new `--json` counts, and in `review-arm` the place rule, the Sweep, the New_Dependency read and the `outside lens:` prefix. Read the README's mentions of the review skill and fix one only if it describes anchoring, the merge, the Cap or the launch; fix any stale cross-reference found in these entries. Manual check: `make validate` passes and each entry agrees with the file it describes
    - _Requirements: 11.1_

- [x] 5. Prove it with eval cases, written and scaffolded but not run until the Owner asks
  - [x] 5.1 Re-quote the Shared_Standard in `evals/agents/review-arm/security-lens/prompt.md`
    - Replace the quoted standard with the paragraph's sentences from "Across every lens" to its end, copied from `lenses.md` as task 2.1 leaves it; graders unchanged. Manual check: `make validate` passes and the quote matches `lenses.md` byte for byte
    - _Requirements: 11.2_
  - [x] 5.2 Re-quote the Shared_Standard in the `documentation-lens` case
    - In `evals/agents/review-arm/documentation-lens/prompt.md`: replace the quoted standard as in 5.1; the documentation lens quote, graders, description and expected outcome stay as they are, since the case already expects the finding on `clamp/cli.py` naming the README example. Manual check: `make validate` passes, the quote matches `lenses.md` byte for byte, and the scaffold builds the fixture in a scratch directory; the case is not run
    - _Requirements: 11.2, 11.3, 11.4_
  - [x] 5.3 Write the `finding-at-each-own-edit-place` case under `evals/agents/review-arm/`
    - In the `security-lens` layout, with the correctness lens and the standard quoted from `lenses.md`: the `shop` fixture with a `files/` overlay committing `shop/commands.py`, whose `delete_product` returns a success message and touches nothing; the scaffold leaves uncommitted a `shop/db.py` that adds `save_product` persistence and no way to delete. Graders: the arm was launched, `^lens: correctness`, `file: shop/commands\.py`, `file: shop/db\.py`. Manual check: `make validate` passes and the scaffold builds the fixture in a scratch directory with `shop/commands.py` committed and `shop/db.py` uncommitted; the case is not run
    - _Requirements: 1.1, 1.6, 11.4_
  - [x] 5.4 Write the `finding-in-each-copy` case under `evals/agents/review-arm/`
    - Correctness lens, `calc` fixture: the scaffold leaves uncommitted two new strategy modules, each returning `{"success": True}` after a check whose result it ignores. Graders: the arm was launched, one regex per module for `file: <module path>`. Manual check: `make validate` passes and the scaffold builds; the case is not run
    - _Requirements: 1.1, 1.7, 11.4_
  - [x] 5.5 Write the `reads-a-new-dependency-whole` case under `evals/agents/review-arm/`
    - Reliability lens, `shop` fixture: a `files/` overlay commits a handler whose first lines return an error when a configured store is `None`, at least fifteen lines above the branch the new caller uses, and tests that always set the store; the scaffold leaves uncommitted a new caller of that handler. Graders: the arm was launched, `file:` the new caller's path, and the guard's variable name in the block. Manual check: `make validate` passes and the scaffold builds; the case is not run
    - _Requirements: 1.2, 5.1, 5.2, 5.3, 11.4_
  - [x] 5.6 Write the `keeps-an-outside-lens-lead` case under `evals/skills/review/`
    - In the `finds-planted-defects` layout, with its answer key in the case's `README.md`: the `shop` fixture with an uncommitted change planting a swallowed error that makes a function return a wrong total. Graders: the final list has a line on the planted file and line. The `README.md` says the case proves the outcome, not the route through the leads. Manual check: `make validate` passes and the scaffold builds; the case is not run
    - _Requirements: 8.1, 8.2, 8.3, 11.5_
  - [x] 5.7 Write the `finding-in-each-of-three-files` case under `evals/skills/review/`
    - Same layout: the `shop` fixture with an uncommitted change planting the same unclosed-connection pattern in three changed files. Graders: one regex per file for a final-list line on it. Manual check: `make validate` passes and the scaffold builds; the case is not run
    - _Requirements: 1.1, 4.2, 6.1, 11.5_

- [x] 7. Remove the cap from the skill and the benchmark
  - [x] 7.1 Remove the cap from `plugins/ponderly/skills/review/SKILL.md`
    - Make the design's Review_Skill rows for the cap, word for word where they quote: the description's "keeps at most 80", step 2's `removed_by_cap`, step 4.5 and its counts paragraph, the step 4 JSON example's `removed_by_cap`, step 6e's cap clauses, step 7's `cut by the cap <n>` and any `removed_by_cap` in step 7's `--json` sentence. Renumber nothing; leave step 5, step 6a and the Launch_Sentence as task 3.2 leaves them. Manual check: `make validate` passes; `rg -n -i '\bcap\b|removed_by_cap' plugins/ponderly/skills/review/SKILL.md </dev/null` finds only the budget note's `$<cap>`; and the counts still add up as step 7 states them
    - _Requirements: 6.4, 6.5, 9.3_
  - [x] 7.2 Remove the Findings_Limit from `benchmarks/reviewbench/agent/findings.py`
    - Make the design's Benchmark rows for `agent/findings.py` and `checks/test_reviewbench_findings.py`. Manual check: `python3 -m unittest checks.test_reviewbench_findings` and `make validate` pass, and the changed test fails against the old `MAX_FINDINGS = 40`
    - _Requirements: 6.6, 11.8_
  - [x] 7.3 Drop the cap line from `benchmarks/reviewbench/report.py` and fix the repair prompt's shape in `benchmarks/reviewbench/agent/agent.py`
    - Make the design's Benchmark rows for `report.py`, `agent/agent.py` and `checks/test_reviewbench_report.py`. Manual check: `python3 -m unittest checks.test_reviewbench_report` and `make validate` pass, and `rg -n 'cap of 40|removed_by_cap' benchmarks/reviewbench/report.py benchmarks/reviewbench/agent/agent.py </dev/null` finds nothing
    - _Requirements: 6.7, 9.5, 11.8_

- [x] 6. Check what others share came through untouched
  - [x] 6.1 Confirm the Wave_Reviewer and the Launch_Sentence are unchanged, and run the free checks
    - Compare `git hash-object plugins/ponderly/agents/wave-reviewer.md` with the hash task 1 recorded; confirm step 5's Launch_Sentence still reads word for word as the design quotes it; confirm the Wave_Reviewer's `model` and `effort` frontmatter are as they were. Run `make validate`. Say that the documentation-lens spec's task 3.2 is now done by tasks 5.1 and 5.2 and is the Owner's to tick. Manual check: the hash matches, the sentence matches, and `make validate` passes; report any failure as it is
    - _Requirements: 7.6, 10.2, 10.4, 11.6, 11.7_

## Notes

- No optional test tasks: the eval cases are the proof the requirements name, so they are not marked `*`.
- Copy every quoted sentence from the design word for word; the Launch_Sentence and the Shared_Standard are each quoted in several files.
- `plugins/ponderly/agents/wave-reviewer.md` is never edited by this spec.
- Under `benchmarks/` only `reviewbench/agent/findings.py`, `reviewbench/agent/agent.py` and `reviewbench/report.py` change, by tasks 7.2 and 7.3; run folders and golden sets are read, never written, and no benchmark target runs. Known follow-up under `benchmarks/`, not done here: have the benchmark report's Review health section read `folded`, `not_anchored` and `relaunched`.
- `rg` needs an explicit path and `</dev/null`.
- No eval target and no ReviewBench chunk runs in this spec; each case is run by hand, one at a time, only when the Owner asks, and the benchmark measure is the Owner's choice afterwards.
- Merged specs are records and are not edited; the two sibling specs are read, not changed.
- Commit nothing; the author commits.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1"] },
    { "id": 1, "tasks": ["2.1", "2.2", "3.1"] },
    { "id": 2, "tasks": ["3.2", "5.1", "5.3", "5.4", "5.5", "7.2", "7.3"] },
    { "id": 3, "tasks": ["7.1", "5.2", "5.6", "5.7"] },
    { "id": 4, "tasks": ["4.1"] },
    { "id": 5, "tasks": ["6.1"] }
  ]
}
```
