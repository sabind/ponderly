# Requirements Document

## Introduction

The `review` skill reads a pull request through one review arm per lens and writes its findings to a file when asked. ReviewBench chunk 4 (run `2026-11-01T08-54-43-prs15-19`) showed two defects in it. On one pull request an arm judged the change's formatting-only edits out of scope and, under the rule that puts a finding at each place a defect is copied, wrote one finding per file, seven in all, every one judged false: 7 of the run's 9 false findings and the difference between that pull request's precision of 57% and the others' 80% to 100%. And three of the run's five final review files lacked the four counts the final pass adds, because the session reused the interim object it had written earlier, whose shape does not hold them. This task narrows the per-copy rule to verified defects and makes the review file carry its final counts whichever way the session writes it. It serves the Reviewer, who reads the findings, and the Owner, who reads the benchmark's score and the run's health.

## Glossary

- **Reviewer**: A person who runs the Review_Skill on a pull request and reads its findings.
- **Owner**: The person who pays for each review and reads its benchmark score and health report.
- **Review_Skill**: The plugin skill `review`, `plugins/ponderly/skills/review/SKILL.md`.
- **Lenses_File**: The Review_Skill's `plugins/ponderly/skills/review/lenses.md`.
- **Shared_Standard**: The sentences of the Lenses_File's opening paragraph from "Across every lens" to its end, sent to every Review_Arm.
- **Review_Arm**: One launch of the plugin's `review-arm` agent, `plugins/ponderly/agents/review-arm.md`, by the Review_Skill, reading the pull request through one lens.
- **Defect**: A line or lines of code or text at the head that do the wrong thing, which a Review_Arm has verified by reading and which an edit at that place would fix.
- **Change_Remark**: A judgement about the pull request as a whole rather than about a line that does the wrong thing, such as that it reformats files it did not need to touch, mixes two purposes, or is too large; it names no line an edit would fix.
- **Per_Copy_Rule**: The sentences of the Shared_Standard and of step 3 of the Review_Arm that put one finding at each place a Defect is copied or needs its own edit.
- **Unsure_Note**: An entry under the `unsure` field of an arm block, never scored as a finding; the Review_Skill passes an entry beginning `outside lens:` to the wave reviewer as a lead, and lists an entry beginning `change remark:` after the count line.
- **Findings_File**: The JSON object the Review_Skill writes to the path given with `--json`, in two writes: the Interim_Object after the first merge and the Final_Object at the end.
- **Interim_Object**: The Findings_File as written after the first merge, with `pass` `"first"`.
- **Final_Object**: The Findings_File as written at the end of the review, with `pass` `"final"`.
- **Final_Counts**: The four entries of the `counts` object that only the final pass can know: `departures_not_reported`, `folded`, `not_anchored` and `relaunched`.
- **Base_Counts**: The four entries of the `counts` object the first merge knows: `candidates`, `removed_by_merge`, `removed_by_review` and `failed_arms`.
- **Arm_Eval_Case**: An eval case under `evals/agents/review-arm/` whose prompt quotes the Shared_Standard and one lens verbatim from the Lenses_File.
- **Review_Eval_Case**: An eval case under `evals/skills/review/` that runs the Review_Skill on a fixture.
- **System**: The Lenses_File, the Review_Arm, the Review_Skill, the ReviewBench adapter's shape text, their documentation and their evals.

## Requirements

### Requirement 1: Put a finding at each copy of a defect only

**User Story:** As a Reviewer, I want one finding per copy only when each copy is a Defect, so that a remark about the whole change is not repeated once per file it touches.

#### Acceptance Criteria

1. THE Shared_Standard SHALL state that the Per_Copy_Rule applies only to a Defect, a place where the code or text at the head does the wrong thing and an edit there would fix it.
2. THE Shared_Standard SHALL state that a Change_Remark is not a finding and goes under `unsure` as one entry beginning `change remark:` that names what the remark is about, however many files it concerns.
3. THE Review_Arm's step 3 SHALL state that its search for copies starts from a Defect, never from a Change_Remark.
4. WHEN a Review_Arm has verified the same Defect at two places, THE System SHALL still produce one finding at each, each naming the other, as the Per_Copy_Rule says today.
5. IF a Review_Arm judges a change to reformat, reorder or otherwise edit files beyond its purpose, THEN THE System SHALL produce no finding for that judgement and at most one Unsure_Note for it.
6. THE System SHALL keep the Shared_Standard's other sentences as they stand, so that the eval prompts that quote it change only where the Per_Copy_Rule changes.
7. THE Review_Skill SHALL end its reply with each arm's `change remark:` entries, one line each after the count line, and with `--json` SHALL list each under `not_reported` with its text as `problem`, `file` and `quote` `null`, and `reason` `change remark`, never under `findings`.

### Requirement 2: Carry the final counts in every final review file

**User Story:** As an Owner, I want every Final_Object to hold the Final_Counts, so that the run's health report reads them from every pull request rather than from the ones whose session happened to write the object afresh.

#### Acceptance Criteria

1. THE Interim_Object's shape in the Review_Skill SHALL hold the Final_Counts beside the Base_Counts, with `departures_not_reported`, `folded` and `not_anchored` at 0 and `relaunched` at `[]`.
2. THE Review_Skill's final write SHALL name the eight entries of `counts`, the Base_Counts and the Final_Counts, as required in the Final_Object, whether the session writes the object afresh or edits the Interim_Object.
3. WHEN the wave review held, did not return or did not run, THE Final_Object SHALL still hold `folded` 0, `not_anchored` 0 and `relaunched` `[]`, and `departures_not_reported` the count line's number when the wave review returned and 0 when it did not.
4. WHEN the Review_Skill stops early and writes the Final_Object with every count 0, THE Final_Object SHALL hold the eight entries of `counts`.
5. THE System SHALL leave the Findings_File's other fields unchanged, and SHALL change the ReviewBench adapter only in its `FINDINGS_SHAPE` text, so that it names the four Final_Counts on both passes and `change remark` among the `not_reported` reasons.

### Requirement 3: Document and prove the change

**User Story:** As an Owner, I want the reference docs to say what the per-copy rule covers and an eval case for each defect, so that a regression shows before a benchmark run.

#### Acceptance Criteria

1. THE System SHALL say in the `review-arm` entry of `docs/reference.md` that a finding per copy is written for a Defect only and that a Change_Remark goes under `unsure`.
2. THE System SHALL rebuild the prompt of every Arm_Eval_Case that quotes the Shared_Standard from the Lenses_File as it stands after the change.
3. THE System SHALL include an Arm_Eval_Case, `one-note-for-a-change-remark`, whose fixture's change holds one Defect copied into two files and formatting-only edits across three other files, and which expects one finding at each copy of the Defect, no finding on the three reformatted files, and at most one Unsure_Note about the reformatting.
4. THE System SHALL include a Review_Eval_Case, `writes-the-final-counts`, whose scaffold excludes `review.json` through `.git/info/exclude`, which runs the Review_Skill with `--json review.json` on a fixture with a planted defect, and which expects `review.json` at the workspace root to have `pass` `"final"` and the eight entries of `counts`.
5. THE System SHALL run no eval case and no benchmark until the Owner asks.

### Requirement 4: Write the findings file to an ignored path inside the repository

**User Story:** As a Reviewer, I want `--json` to accept a path inside the repository when git ignores it, so that I can write the findings beside my checkout without dirtying it.

#### Acceptance Criteria

1. WHEN the `--json` path lies under the repository root and `git check-ignore -q <path>` succeeds, THE Review_Skill SHALL accept it and write the file there.
2. IF the path lies under the repository root and is not ignored, THEN THE Review_Skill SHALL say the path must be outside the repository or ignored by it, naming both, and stop, as today.
3. THE Review_Skill's statement that it changes no file SHALL say the one exception is the `--json` file, outside the repository or ignored by it.
4. THE `review` entry of `docs/reference.md` SHALL say the same.
