# Implementation Plan

## Overview

The two prompt edits come first and do not touch each other's files: the Shared_Standard and the arm's step 3 for the per-copy rule, and the three places in the review skill for the counts. The arm eval prompts are re-quoted after the Shared_Standard lands, since they copy it verbatim. The two eval cases and the reference entry follow the edits they prove or describe, and the Makefile grant goes with the review case that needs it. Nothing is run: every eval case is written and scaffolded, proved by `make validate`'s parse of its files and a dry read of its graders against the fixture, and run only when the Owner asks. There is no unit-test framework for prompt text, so the free checks are `make validate` and each task's stated manual check.

## Tasks

- [x] 1. Tie the per-copy rule to a defect
  - [x] 1.1 Edit the Shared_Standard in `plugins/ponderly/skills/review/lenses.md`
    - In the opening paragraph, make the Per_Copy_Rule sentence's subject explicit, "When a defect, a place where the code or text at the head does the wrong thing and an edit there would fix it, needs its own edit at several places ...", and add after it the Change_Remark sentence from the design: a judgement about the change as a whole, such as that it reformats or reorders files beyond its purpose, mixes two purposes or is too large, names no line an edit would fix, is not a finding, and goes under `unsure` in one entry however many files it concerns. Change no other sentence. Manual check: `git diff` shows only those two sentences changed, and the paragraph still reads from "Across every lens" to its end
    - _Requirements: 1.1, 1.2, 1.4, 1.6_
  - [x] 1.2 Edit step 3 of `plugins/ponderly/agents/review-arm.md`
    - The copy-search sentence starts from a verified defect, "When a defect that you have verified at one place comes from a pattern ...", and ends with the clause that a remark about the change as a whole starts no search and is one `unsure` entry, as the standard says. Manual check: `git diff` shows only step 3 changed
    - _Requirements: 1.3, 1.4, 1.5_
  - [x] 1.3 Move the Change_Remark sentence and add the `change remark:` prefix in `plugins/ponderly/skills/review/lenses.md` and `plugins/ponderly/agents/review-arm.md`
    - In `lenses.md` line 3, move the Change_Remark sentence from after the Per_Copy_Rule sentence to after "a place you suspect but have not verified at head is no finding and goes under unsure.", and change its ending to "goes under unsure in one entry beginning `change remark:` that says what it is about, however many files it concerns." In `review-arm.md` step 3, the closing clause reads "a remark about the change as a whole starts no search and is one `unsure` entry beginning `change remark:`, as the standard says." Manual check: `git diff` against HEAD shows only those sentences changed in each file
    - _Requirements: 1.2, 1.3_
  - [x] 1.4 Name the Shared_Standard's opening sentence in `plugins/ponderly/skills/review/SKILL.md` and `plugins/ponderly/skills/review/lenses.md`
    - Both files define the shared standard as the paragraph from "Across every lens" to its end, and that phrase occurs twice on lenses.md line 3, the first time inside the file's sentence about itself, so a session can quote the wrong start. In SKILL.md step 1 and in the lenses.md sentence that names the standard, write `from "Across every lens, a finding worth reporting"` in place of `from "Across every lens"`. Manual check: `git diff` shows only those two phrases changed, and the six arm prompts' quoted spans still match lenses.md from that opening
    - _Requirements: 3.2_

- [x] 2. Carry the final counts in every review file
  - [x] 2.1 Edit steps 2, 4 and 7 of `plugins/ponderly/skills/review/SKILL.md`
    - Step 4's JSON block: `counts` holds the eight entries, the four Final_Counts at `0`, `0`, `0` and `[]`, and the sentence after the block says the four are the final pass's counts, kept at those values until step 7. Step 7's `--json` paragraph: name the eight entries of `counts` as required in the final object "whether the object is written afresh or the interim file is edited", keeping each entry's existing value rule. Step 2's early stop: list the eight entries by name in place of "every count 0" and the three names. Manual check: `git diff` shows only those three places changed, and the JSON block parses with `python3 -c 'import json,sys; json.loads(sys.stdin.read())'` on the block's text
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  - [x] 2.2 List each arm's change remarks in step 7 of `plugins/ponderly/skills/review/SKILL.md`
    - After the count line, without `--json`, one line per `unsure` entry beginning `change remark:` in the arm blocks the merges took, once per arm, each line as `change remark: <its text after the prefix>`; with `--json`, a new `not_reported` bullet: each such entry with `file` and `quote` `null`, its text after the prefix as `problem`, and `reason` `change remark`, and the reply with the path and the count line gains the same lines. Never in `findings`. Manual check: `git diff -U0` shows the step 7 hunks and no other
    - _Requirements: 1.7_
  - [x] 2.4 Accept a git-ignored `--json` path inside the repository, in `plugins/ponderly/skills/review/SKILL.md` and `docs/reference.md`
    - In SKILL.md: the preamble sentence "The one file it writes is the JSON a `--json` path names, and only when that path is outside the repository" gains "or ignored by it"; the Stops entry "a `--json` without a path or with a path inside the repository" becomes "with a path inside the repository that git does not ignore"; step 1's path check reads "When it is the root, or lies under it and `git check-ignore -q <path>` fails, say that the `--json` path must be outside the repository or ignored by it, naming both, and stop." In the `review` entry of docs/reference.md, the sentence on the `--json` path says the same. Manual check: `git diff -U0 HEAD` shows the three SKILL.md sentences and one reference sentence changed beyond the branch's earlier hunks; `git check-ignore -q` run by hand in a scratch repository with and without an exclude entry gives exit 0 and 1
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [x] 2.3 Edit `FINDINGS_SHAPE` in `benchmarks/reviewbench/agent/agent.py`
    - Drop the clause "these four only when `pass` is `final`," and add `"change remark"` to the `reason` alternatives of `not_reported`; change nothing else in the adapter. Check: `make validate`
    - _Requirements: 2.5_

- [x] 3. Document the rule
  - [x] 3.1 Update the `review-arm` entry of `docs/reference.md`
    - Its sentence on copies gains "for a defect it verified; a remark about the change as a whole goes under unsure". Manual check: the entry reads in order and names no benchmark
    - _Requirements: 3.1_

- [x] 4. Re-quote the Shared_Standard in the arm eval prompts
  - [x] 4.1 Rebuild the five prompts under `evals/agents/review-arm/`
    - In `security-lens`, `documentation-lens`, `finding-at-each-own-edit-place`, `finding-in-each-copy` and `reads-a-new-dependency-whole`, replace the quoted Shared_Standard with the paragraph as `lenses.md` now holds it, from "Across every lens" to its end, and nothing else in the prompt. Manual check: for each prompt, the quoted paragraph is byte-equal to the file's, shown by extracting both and running `diff`
    - _Requirements: 3.2_

- [x] 5. Prove it with eval cases, written and scaffolded but not run
  - [x] 5.1 Write the `one-note-for-a-change-remark` case under `evals/agents/review-arm/`
    - `case.yaml`, `scaffold.sh` (calc fixture on branch `calc-strategies` with wrappers, then this case's `files/` copied over), `files/` holding the two strategy modules of `finding-in-each-copy` and formatting-only edits of `calc/ops.py`, `calc/__init__.py` and `tests/test_ops.py` (import order, blank lines, quote style, no behaviour change), `prompt.md` in the sibling cases' form quoting the Shared_Standard and the correctness lens verbatim, and graders: `launches-the-arm` (tool_used Agent), `names-lens` (regex `^lens: correctness`), `finds-the-add-strategy` and `finds-the-multiply-strategy` (regex on each file), `no-finding-on-reformatted-files` (regex, `file: (?:calc/ops\.py|calc/__init__\.py|tests/test_ops\.py)` with a negative expectation in the form the sibling graders use for absence), and `notes-the-reformat-once` (regex, `^\s*- change remark:` with flag m, on the arm's block). Manual check: `bash scaffold.sh` in a scratch directory leaves the three reformatted files as uncommitted modifications with `git diff --stat` showing no added logic, and the two strategy modules untracked; `make validate` parses the case
    - _Requirements: 3.3_
  - [x] 5.2 Write the `writes-the-final-counts` case under `evals/skills/review/` and grant Write in the Makefile
    - `case.yaml`, `scaffold.sh` (shop fixture on branch `shop-orders` with wrappers, then this case's `files/` copied over), `files/shop/orders.py` as in `keeps-an-outside-lens-lead`, `prompt.md` with `allowed_tools: [Read, Glob, Grep, Agent, Write]` and the prompt `/ponderly:review --json review.json`; the scaffold appends `review.json` to `.git/info/exclude` after setup, so git ignores the file without a tracked change and the skill accepts the path (the eval sandbox denies every write outside the workspace, so the file must sit inside it); graders: `writes-the-file` (file_exists `review.json`), `pass-is-final` (regex `"pass": *"final"` on that file), one regex grader per count key on that file matching the key alone, `"candidates":`, `"removed_by_merge":`, `"removed_by_review":`, `"failed_arms":`, `"departures_not_reported":`, `"folded":`, `"not_anchored":` and `"relaunched":` (the last two of `failed_arms` and `relaunched` are lists, never numbers), and `launches-the-wave-reviewer-once` as the three-files case has it; no grader on `not_reported`, which the arm case proves. In the Makefile, `eval-skill-review: CASE_ARGS += --allow-tools Bash Write --scaffold`. Manual check: `bash scaffold.sh` in a scratch directory leaves `shop/orders.py` uncommitted; `make validate` parses the case; `make -n eval-skill-review` prints the grant; the partial files the first attempt left (graders with number patterns for the list keys, `remarks-have-their-reason`, and a scaffold comment naming another case) are replaced or removed
    - _Requirements: 3.4, 3.5_

## Notes

- Every edit to a prompt is the smallest wording change that says the rule; no sentence is restyled.
- No eval case is run in this spec. The Owner runs them one at a time afterwards, and the ReviewBench measure is the chunk 1 rerun, outside the tasks.
- Under `benchmarks/` only the adapter's `FINDINGS_SHAPE` string changes, in task 2.3.
- `rg` needs an explicit path and `</dev/null`; never bare `git stash`; commit nothing.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "2.1"] },
    { "id": 1, "tasks": ["1.3", "2.2", "2.3"] },
    { "id": 2, "tasks": ["3.1", "4.1", "5.1"] },
    { "id": 3, "tasks": ["1.4"] },
    { "id": 4, "tasks": ["2.4", "5.2"] }
  ]
}
```
