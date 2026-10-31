# Implementation Plan

## Overview

The Lenses_File changes first, the new section and the narrowed maintainability section in one task since they share one file and one boundary, beside a read of the skill and the arm agent that confirms nothing names five lenses. The reference entry and the new arm eval case follow, once the lens text they describe and quote is in. Instruction text has no unit tests here: each task is proved by `make validate` and a dry run of the lens text on a chunk 3 pull request, read only, and the eval case is written and its scaffold built but not run until the Owner asks. No ReviewBench run is part of these tasks.

## Tasks

- [x] 1. Add the documentation lens and narrow maintainability
  - [x] 1.1 Edit `plugins/ponderly/skills/review/lenses.md`
    - Add the design's `## documentation` section word for word, after `## maintainability` and before `## testing`. In `## maintainability`, make the design's four replacements: the documentation clause, the categories sentence, "the stale sentence" dropped from the true-positive sentence, and the last sentence naming the documentation lens. Change nothing else, the opening paragraph and the Shared_Standard included; another change in flight edits the Shared_Standard. Manual check: `make validate` passes, no benchmark is named in the file, and a dry run of the new section on the `scotthamilton77_agents-config_1-1fc78970` change (its diff read from the chunk 3 run folder's evidence, read only) lists the templates it would read in full and the names it would search for
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11, 1.12, 2.1, 2.2, 2.3, 2.4, 3.4, 3.5_
  - [x] 1.2 Confirm the skill and the arm agent take a sixth lens unchanged
    - Read `plugins/ponderly/skills/review/SKILL.md` and `plugins/ponderly/agents/review-arm.md` for any count or list of lenses, any lens named as a fixed set, and any benchmark named in the arm; step 6a's sort by `lenses.md`'s words and the arm's category list holding `documentation` are expected. Change a file only if the read finds one, and report what was read and found. Manual check: `make validate` passes
    - _Requirements: 3.1, 3.2, 3.4, 3.5_
  - [x] 1.3 Make the arm read only
    - Make the design's "Changes after the wave 1 review" edits word for word: the read-only and run paragraphs of `plugins/ponderly/agents/review-arm.md`, the four run clauses of `plugins/ponderly/skills/review/lenses.md`, and the lens quotes of the `security-lens` and `documentation-lens` prompts. Manual check: `make validate` passes, `rg` finds no run clause in `lenses.md` or the arm, each prompt's quoted lens matches `lenses.md` byte for byte, and the frontmatter, `SKILL.md`'s opening, `plugins/ponderly/README.md`, `llms.txt` and the `review-arm` entry and disclosure of `docs/reference.md` show no change from HEAD in those texts
    - _Requirements: 3.6_

- [x] 2. Document the change
  - [x] 2.1 Update the `review` entry of `docs/reference.md`
    - Replace "correctness, reliability, security, maintainability and testing" with the six lenses, documentation among them, and add the design's sentence on what the documentation arm reads and searches for. Fix any other stale cross-reference to the five lenses in `docs/reference.md`, the README or `llms.txt` the change makes untrue. Manual check: `make validate` passes and the entry agrees with `lenses.md`
    - _Requirements: 4.1_

- [x] 3. Prove it with an eval case, not run until the Owner asks
  - [x] 3.1 Write the `documentation-lens` case under `evals/agents/review-arm/`
    - In the `security-lens` layout: `case.yaml`, `prompt.md`, `scaffold.sh`, `files/` and `graders/`. `files/` holds `clamp/cli.py`, an argparse command line taking a value and `--high`, and a `README.md` whose example runs `python3 -m clamp.cli 150 --high 120`; the scaffold copies them in before `evals/fixtures/setup.sh clamp main wrappers` so they are committed, then writes an uncommitted `clamp/cli.py` that renames `--high` to `--max`, leaving the README unchanged. The prompt quotes the Shared_Standard and the Documentation_Lens verbatim from `lenses.md` as it stands after task 1.1, and gives the range, the changed file and a title. Graders: the arm launched as `ponderly:review-arm`, `^lens: documentation`, a finding with `file: clamp/cli.py` whose message names `README.md`, and `--max` in the block. Manual check: `make validate` passes and the scaffold builds the fixture in a scratch directory with `git status` showing only `clamp/cli.py` modified; the case is not run
    - _Requirements: 4.2, 4.4, 4.6_
  - [x] 3.2 Rebuild the arm eval prompts after the anchoring change lands, by hand
    - Only once the anchoring change in flight has landed in the Shared_Standard of `lenses.md`: rebuild the `security-lens` prompt's quoted Shared_Standard and security lens from `lenses.md` word for word, and confirm the `documentation-lens` prompt's quoted Shared_Standard and Documentation_Lens still match `lenses.md`, rebuilding it if not. Manual check: `make validate` passes and each quoted text is found verbatim in `lenses.md`; neither case is run
    - _Requirements: 4.3, 4.4_

## Notes

- No optional test tasks: the eval case is the proof the requirements name, so it is not marked `*`.
- Task 3.2 waits for the anchoring change in flight to land in the Shared_Standard; until then the `security-lens` prompt stays as it is.
- Nothing under `benchmarks/` changes; the chunk 3 run folder is read, never written. The adapter's findings shape belongs to the `review-skips-no-cost-departures` spec, which records its change. No ReviewBench run is part of these tasks; the Owner chooses the measure afterwards, as the design names.
- The lens text names no benchmark.
- No eval target runs in this spec; the case is run by hand only when the Owner asks.
- Commit nothing; the author commits.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3"] },
    { "id": 1, "tasks": ["2.1", "3.1"] },
    { "id": 2, "tasks": ["3.2"] }
  ]
}
```
