# Implementation Plan

## Overview

The two instruction files change first and independently, since they meet only through the Launch_Sentence, which the design fixes word for word: the review skill's steps 4, 5 and 7, and the `wave-reviewer`'s review-skill paragraph and nit clause. The reference entries and the two eval cases follow, once the text they describe and quote is in. Instruction text has no unit tests here: each task is proved by `make validate` and a dry run of the new text on the chunk 3 evidence, read only, and the eval cases are written and their scaffolds built but not run until the Owner asks.

## Tasks

- [x] 1. Leave cost-free team-rule departures out of the review and keep what was left out
  - [x] 1.1 Change the Launch_Sentence and add the count and the list in `plugins/ponderly/skills/review/SKILL.md`
    - Step 5: replace the Launch_Sentence with the design's whole new sentence, which changes only the bar list and the last clause; change nothing else in the step's bullets. After the verdict paragraph, add a paragraph: when the Findings have a `verdict` line, the departures not reported are its `unsure` entries that begin `departure not reported:`. Step 7: add `departures not reported <n>` to the Count_Line after the fold facts when the Wave_Review returned Findings; add `counts.departures_not_reported` to the final object, 0 when the Wave_Review did not return or did not run; add `not_reported` beside `findings` with the entries, reasons and `null`s the design's step 7 row gives, covering all three reasons: `team-rule departure without cost` for each `departure not reported:` entry, `unsettled lead` for each other `unsure` entry but `nothing`, and `not anchored` for each reviewer finding step 6d counts as not anchored, with the reviewer's file, quote and problem as returned; empty when the Wave_Review did not return or did not run, and never an entry in `findings`. The Count_Line's `not anchored` count stays as it is. Step 4: the interim JSON example gains `"not_reported": []`. Steps 6 and 6d do not change. Manual check: `make validate` passes, and a dry run of steps 5 and 7 on the reviewer's Findings in `benchmarks/reviewbench/runs/2026-10-30T16-14-21-prs10-14/logs/AY2526S2-CS2103T-W14-3_tp_152-e0a9ce03/` (read only), rewritten by hand as the new Standard would return them, gives the count and the `not_reported` entries, with a reviewer finding whose quote is changed by hand to one not in its file landing in `not_reported` as `not anchored`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.3_
  - [x] 1.2 Change the review-skill paragraph and the nit clause of `plugins/ponderly/agents/wave-reviewer.md`
    - Replace the old sentences of the Standard's review-skill paragraph with the design's new ones, word for word: the sentence on what to read, the sentence that made a cost-free departure a nit, and the no-bar sentence. Replace the Findings section's nit clause with the design's new clause. Change nothing else in the file; every launch without the Launch_Sentence reads as before. Manual check: `make validate` passes, and a dry run of the new paragraph on the chunk 3 reviewer nits (`LogicManagerTest.java` `getMethods_success`, `ConflictResolvers.kt` `InvocationTargetException`, `Plugin.kt` fully qualified names, `encryption.rs` `type_complexity`) puts the first two under `unsure` as `departure not reported:` and keeps the last two as nits
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 3.2_

  - [x] 1.3 Apply the four changes after the wave 0 review to `plugins/ponderly/skills/review/SKILL.md`
    - Make the design's "Changes after the wave 0 review" edits word for word: move the departures paragraph of step 5 above the verdict paragraph; replace step 6c's first bullet; add step 7's `dropped by relaunched arm` bullet after the `not anchored` bullet; add step 7's sentence on splitting a departure entry. Change nothing else, step 5's launch-sentence bullet included. Manual check: `make validate` passes, each new text is found once with `grep -c`, and a hand dry run of step 7 on one reviewer finding given to a relaunched arm whose second-pass list leaves it out puts it in `not_reported` as `dropped by relaunched arm`
    - _Requirements: 2.4, 2.5, 3.3_

- [x] 2. Document the change
  - [x] 2.1 Update the `review` and `wave-reviewer` entries of `docs/reference.md`
    - `review`: the wave review paragraph says the reviewer leaves out a team-rule departure with no concrete cost and the skill counts it; What it writes names `departures not reported` in the count line and the `not_reported` list in the JSON file. `wave-reviewer`: What the prompt carries names the bar's files, `AGENTS.md` and `.claude/rules/` among them, and replaces "reports a team-rule departure with no concrete cost in the change as a `nit`" with leaving it out under `unsure`, a departure from the repository's own bar with no cost staying a `nit`. Manual check: `make validate` passes and each entry agrees with the file it describes
    - _Requirements: 4.1_

- [x] 3. Prove it with eval cases, not run until the Owner asks
  - [x] 3.1 Update the `judges-by-the-repository-bar` case under `evals/agents/wave-reviewer/`
    - `prompt.md`: the new Launch_Sentence, word for word; its description and expected outcome say no divider-comment finding at any severity and a `departure not reported:` entry under `unsure`. Rename the grader `no-divider-finding-above-nit.md` to `no-divider-finding.md`, matching any severity; add `lists-the-departure.md`, a regex for `departure not reported:`; keep the floor-division, launch and verdict graders. Manual check: `make validate` passes and the scaffold builds the fixture in a scratch directory; the case is not run
    - _Requirements: 4.2, 4.4, 4.5_
  - [x] 3.2 Write the `reports-a-bar-departure-as-nit` case under `evals/agents/wave-reviewer/`
    - In the layout of `judges-by-the-repository-bar`: a calc fixture whose committed modules annotate every parameter and return, and an uncommitted `calc/stats.py` with a correct, unannotated `mean`; the prompt launches the reviewer with the new Launch_Sentence and the mean requirement; graders: the sub-agent was launched, a finding on the missing annotations at severity nit, and no finding at blocker or should-fix. Manual check: `make validate` passes and the scaffold builds the fixture in a scratch directory; the case is not run
    - _Requirements: 1.3, 4.3, 4.5_

## Notes

- No optional test tasks: the eval cases are the proof the requirements name, so they are not marked `*`.
- The chunk 3 run folder is read, never written. Under `benchmarks/`, only the adapter's `FINDINGS_SHAPE` and repair prompt change, at the Owner's request after the tasks, as the design's REPAIR row records. The repair-prompt gap the design's Error Handling names is not fixed here.
- The Launch_Sentence is the one text two files and two eval prompts share; copy it from the design word for word. Another change in flight adds sentences after it in step 5; touch nothing else in step 5's bullets.
- The `review-skill-second-pass-and-bar` spec is a record and is not edited.
- No eval target runs in this spec; each case is run by hand, one at a time, only when the Owner asks.
- Commit nothing; the author commits.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["1.3", "2.1", "3.1", "3.2"] }
  ]
}
```
