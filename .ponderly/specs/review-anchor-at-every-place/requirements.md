# Requirements Document

## Introduction

The `review` skill returns findings anchored to lines, and a defect often lives in more than one place: a stub and the interface it lacks, the same mistake copied into several files, a code change and the documentation it made stale. Today a review arm writes one finding for such a defect, at the place the fix would change, preferring a file the pull request touched, and lists the other places as a sentence. A Reviewer posting those findings as comments gets one comment where the author must make several edits, and a benchmark that compares findings only within a file counts every other place as missed: across ReviewBench chunks 1 to 3 that lost 14 golden true positives our own messages named. Problems the arms noticed outside their lens, and problems the wave reviewer could quote but doubted, were also dropped, and one high-severity defect was missed because an arm read a newly called handler from its middle. This task puts a finding at every place that needs its own edit and, where either of two edits alone would fix the defect, at the place the pull request changed; keeps those findings apart through the arm, the merge and the wave review; hands the arms' outside-lens notes to the wave reviewer; has the arm sweep for copies and read newly depended-on code from its first line; removes the cap, so that no verified finding is dropped for its severity or the list's length; and records the wave reviewer's share in the review's JSON file. It serves the Reviewer, who reads and posts the findings, and the Owner, who pays for each review and reads its benchmark score. It builds on the approved `review-skips-no-cost-departures` and `review-documentation-lens` specs and replaces the two-place anchoring sentence that commit 1f0f3ef added.

## Glossary

- **Reviewer**: A person who runs the Review_Skill on a pull request and reads or posts its Final_List.
- **Owner**: The person who pays for each review and reads its benchmark score.
- **Review_Skill**: The plugin skill `review`, `plugins/ponderly/skills/review/SKILL.md`.
- **Review_Arm**: The plugin's `review-arm` agent, `plugins/ponderly/agents/review-arm.md`, launched once per Lens.
- **Lens**: One `##` section of `plugins/ponderly/skills/review/lenses.md`.
- **Shared_Standard**: The sentences of `lenses.md`'s opening paragraph that the Review_Skill quotes to every Review_Arm, from "Across every lens" to the paragraph's end.
- **Wave_Reviewer**: The plugin's `wave-reviewer` agent, `plugins/ponderly/agents/wave-reviewer.md`, shared with `implement-spec`, `readable-code` and `tighten-tests`.
- **Wave_Review**: The one launch of the Wave_Reviewer by the Review_Skill, in step 5.
- **Launch_Sentence**: The sentence step 5 of the Review_Skill gives the Wave_Review verbatim, beginning "These changes are a pull request reviewed for the review skill", as the `review-skips-no-cost-departures` spec leaves it.
- **Finding**: One entry of an arm block or of the Final_List: a file, a line range at the head, a severity, a category and a message.
- **Reviewer_Finding**: One entry of the Wave_Review's Findings block: a file, an exact quote, a problem and a severity.
- **Defect**: One thing wrong in the change, which one fix, made at one or more places, removes.
- **Place**: A line range at the head, in any file the Review_Arm read, where a Defect lives.
- **Own_Edit_Place**: A Place that must itself be edited for the Defect to be fixed, because it is wrong on its own, such as a stub that does nothing or a copy of a wrong return.
- **Either_Side_Defect**: A Defect between two Places where an edit at either Place alone would fix it, such as a new call into a handler whose guard does not serve that call, or code and a document that disagree.
- **Changed_Side**: The Place of an Either_Side_Defect whose lines the pull request added or changed.
- **Multi_Place_Set**: The Findings of one Defect at two or more Places, each naming the others' file and line.
- **Outside_Lens_Lead**: An `unsure` entry of a Review_Arm's block that names a problem outside its Lens.
- **New_Dependency**: A function or endpoint that the change makes code call or rely on and that the code did not call or rely on before.
- **Sweep**: The Review_Arm's search, before it returns its block, for further copies of a Defect that comes from a pattern.
- **Cap**: The largest number of Findings a merge of the Review_Skill kept, 40, dropping from the lowest severity; this change removes it.
- **Findings_Limit**: The ReviewBench_Adapter's own limit on the Findings it scores, `MAX_FINDINGS = 40` in `benchmarks/reviewbench/agent/findings.py`.
- **Final_List**: The Findings the Review_Skill returns, or writes to the Findings_File.
- **Findings_File**: The JSON file the Review_Skill writes when run with `--json`.
- **Count_Line**: The line after the Final_List that gives the Review_Skill's counts.
- **Not_Reported_List**: The `not_reported` list the `review-skips-no-cost-departures` spec adds to the final Findings_File.
- **ReviewBench_Adapter**: The benchmark's adapter under `benchmarks/reviewbench/agent/`, which reads the Findings_File's `findings` and `counts.failed_arms`.
- **Benchmark_Report**: `benchmarks/reviewbench/report.py`, which writes a run's report, its Review health section included.
- **System**: The Review_Skill, the Lenses file, the Review_Arm, and their documentation and evals.

## Requirements

### Requirement 1: A Finding at every Place that needs its own edit

**User Story:** As a Reviewer, I want a Finding at each Place I must edit to fix a Defect, so that each comment I post sits where a change is needed.

#### Acceptance Criteria

1. WHEN a Review_Arm verifies a Defect at two or more Own_Edit_Places, THE Review_Arm SHALL write one Finding at each Own_Edit_Place, in its own file, whether or not the pull request touched that file.
2. WHEN a Review_Arm verifies an Either_Side_Defect whose Changed_Side is one Place, THE Review_Arm SHALL write one Finding at the Changed_Side and none at the other Place.
3. WHEN a Review_Arm verifies an Either_Side_Defect whose two Places the pull request both changed, THE Review_Arm SHALL write one Finding at each Place.
4. WHEN code and a document, configuration or manifest disagree, THE Review_Arm SHALL treat the disagreement as an Either_Side_Defect, so that its Finding sits on the code lines when only the code changed, on the document lines when only the document changed, and on both when both changed.
5. WHEN a Defect has two or more Own_Edit_Places in one file, THE Review_Arm SHALL write one Finding at each of them.
6. THE Review_Arm SHALL name, in each Finding of a Multi_Place_Set, the file and line of every other Finding of that set, and the other Place of an Either_Side_Defect in its one Finding.
7. THE Review_Arm SHALL never describe another Own_Edit_Place's Defect as a sentence in a Finding in place of a Finding of its own.
8. IF a Review_Arm suspects a Place of a Defect it has not verified at the head, THEN THE Review_Arm SHALL write no Finding at that Place and SHALL list it under `unsure`.
9. THE System SHALL state this rule once, in the Shared_Standard, and SHALL replace the anchoring sentence of step 5 of the Review_Arm with a rule that gives each Finding the smallest line range at the head that holds its Place.

### Requirement 2: One Defect per Finding

**User Story:** As a Reviewer, I want each Finding to describe one Defect and nothing it did not verify, so that each comment can be acted on and judged alone.

#### Acceptance Criteria

1. THE Review_Arm SHALL describe one Defect in each Finding's message.
2. WHEN a Review_Arm verifies a second Defect while writing a Finding, THE Review_Arm SHALL write it as a Finding of its own at its own Place, even when it is on the same lines.
3. THE Review_Arm SHALL include in a Finding's message no aside that restates a claim it did not verify.
4. THE System SHALL state this rule in the Shared_Standard, beside the rule of Requirement 1.

### Requirement 3: The arm keeps a Multi_Place_Set

**User Story:** As a Reviewer, I want the arm to keep every Finding of a Multi_Place_Set, so that its own duplicate rule does not undo Requirement 1.

#### Acceptance Criteria

1. THE Review_Arm SHALL treat the Findings of a Multi_Place_Set as different Findings, not as one problem reported twice.
2. THE Review_Arm SHALL still report no Defect twice at the same Place.

### Requirement 4: The arm sweeps for copies

**User Story:** As a Reviewer, I want the arm to look for further copies of a patterned Defect, so that a copy is reported even when no arm happened to read it.

#### Acceptance Criteria

1. WHEN a Review_Arm verifies a Defect that comes from a pattern, such as a copied helper, a repeated line or a step missing at a call site, THE Review_Arm SHALL search the other changed files, and the call sites of a changed function or action that it read at the head, for the same pattern before returning its block.
2. WHEN the Sweep finds a copy that the Review_Arm verifies at the head, THE Review_Arm SHALL write it as a Finding under Requirement 1.
3. IF the Sweep finds a copy the Review_Arm cannot verify at the head, THEN THE Review_Arm SHALL write no Finding for it.
4. THE Review_Arm SHALL search no file outside the changed files and the call sites it already read.
5. THE System SHALL state the Sweep in step 3 of the Review_Arm and not in the Shared_Standard.

### Requirement 5: The arm reads a New_Dependency from its first line

**User Story:** As a Reviewer, I want the arm to read newly depended-on code from its signature, so that an early return the change now runs into is not missed.

#### Acceptance Criteria

1. WHEN the change introduces a New_Dependency, THE Review_Arm SHALL read it from its signature through every guard and early return before the branch the change uses.
2. WHEN the Review_Arm reads such a guard or early return, THE Review_Arm SHALL establish under which configuration it fires.
3. THE Review_Arm SHALL not take a test that always sets up what a guard checks as evidence that the guard is met in production.
4. THE System SHALL state this in step 2 of the Review_Arm.

### Requirement 6: The merge keeps a Multi_Place_Set and every verified Finding

**User Story:** As a Reviewer, I want the merge to keep each Finding of a Multi_Place_Set and to cut no verified Finding, so that every Place reaches my list.

#### Acceptance Criteria

1. WHILE `--duplicates` is `same-defect`, THE Review_Skill SHALL not collapse two Findings at different Places that name each other's file and line.
2. WHILE `--duplicates` is `same-defect`, THE Review_Skill SHALL collapse two Findings at the same Place that name the same Defect and the same fix, as it does today.
3. THE Review_Skill SHALL leave the `keep` and `overlap` modes as they are.
4. THE Review_Skill SHALL apply no Cap: neither merge, in step 4 or step 6e, SHALL drop a Finding for its severity or for the length of the list.
5. THE Review_Skill SHALL write no `removed_by_cap` count in the Findings_File and no `cut by the cap` in the Count_Line, and its counts SHALL add up without one.
6. THE ReviewBench_Adapter SHALL score every Finding that passes its file and line checks, with no Findings_Limit and no `over_limit` count.
7. THE Benchmark_Report SHALL print no line for findings removed by a cap, and SHALL still read as readable a review file that records `removed_by_cap`, as files from earlier runs do.

### Requirement 7: The wave review keeps a Multi_Place_Set and reports what it can quote

**User Story:** As a Reviewer, I want the wave reviewer to treat a Multi_Place_Set as one Defect at several Places and to report a problem it can quote, so that its findings fill the Places the arms missed instead of being lost.

#### Acceptance Criteria

1. THE Review_Skill SHALL tell the Wave_Review that a Multi_Place_Set is not a duplicate.
2. THE Review_Skill SHALL tell the Wave_Review to report a Defect it finds at several Places as one Reviewer_Finding per Place, each with its own quote, and never to list other Places inside one Reviewer_Finding.
3. THE Review_Skill SHALL tell the Wave_Review that a problem it can tie to a file and an exact quote at the head is a Reviewer_Finding at the severity it deserves, with its doubt stated in the problem together with what would settle it, a file to read or a case to run.
4. THE Review_Skill SHALL tell the Wave_Review that a doubtful problem with no way to settle it, or one it cannot tie to a quote, goes under `unsure`.
5. WHEN step 6a sorts a Reviewer_Finding at a Place where the merged list has no Finding, THE Review_Skill SHALL sort it as new, even when its problem names a Finding of the merged list at another Place.
6. THE System SHALL put these instructions in step 5 of the Review_Skill, after the Launch_Sentence, and SHALL change nothing in the Wave_Reviewer's definition.

### Requirement 8: Hand the arms' outside-lens notes to the wave review

**User Story:** As a Reviewer, I want problems an arm noticed outside its lens to be checked by the wave reviewer, so that they reach my list when the code bears them out.

#### Acceptance Criteria

1. WHEN the Review_Skill launches the Wave_Review, THE Review_Skill SHALL quote each Outside_Lens_Lead of the merge's Review_Arms, with its Lens, as leads the arms did not settle.
2. THE Review_Skill SHALL tell the Wave_Review to verify each lead at the head and to report those the code bears out as Reviewer_Findings.
3. WHEN a Reviewer_Finding comes from a lead, THE Review_Skill SHALL fold, relaunch or settle it like any other Reviewer_Finding.
4. IF no Review_Arm returned an Outside_Lens_Lead, THEN THE Review_Skill SHALL say in the launch that there are no leads.
5. THE Review_Skill SHALL not quote an `unsure` entry that is not an Outside_Lens_Lead, such as `nothing` or `review not done:`.

### Requirement 9: Record the wave reviewer's share in the Findings_File

**User Story:** As an Owner, I want each review's JSON file to say how many findings the wave reviewer added and which arms ran twice, so that I can judge the reviewer's worth from the run folder without its transcript.

#### Acceptance Criteria

1. WHEN the Review_Skill writes the final Findings_File, THE System SHALL write `counts.folded`, `counts.not_anchored` and `counts.relaunched`, with the numbers and lenses the Count_Line gives for folded, not anchored and relaunched.
2. THE System SHALL make `counts.not_anchored` equal the number of Not_Reported_List entries whose reason is `not anchored`.
3. IF the Wave_Review held, did not return or did not run, THEN THE System SHALL write `counts.folded` and `counts.not_anchored` as 0 and `counts.relaunched` as an empty list.
4. THE System SHALL name the new keys in the snake-case form of the `counts` keys the `review-skips-no-cost-departures` spec leaves.
5. THE System SHALL change under `benchmarks/` only the ReviewBench_Adapter's Findings_Limit, its repair prompt's `counts` shape, the Benchmark_Report's cap line and the benchmark README's sentence on it, as Requirement 6 and this requirement name, and SHALL add `folded`, `not_anchored` and `relaunched` to that repair prompt's shape and drop `removed_by_cap` from it.

### Requirement 10: Build on the two specs in flight

**User Story:** As an Owner, I want this change written against the Launch_Sentence and Lenses file as the two approved specs leave them, so that it applies on top of them without a conflict.

#### Acceptance Criteria

1. THE System SHALL quote the Launch_Sentence and the Shared_Standard as the `review-skips-no-cost-departures` and `review-documentation-lens` designs leave them.
2. THE System SHALL add its words to step 5 of the Review_Skill after the Launch_Sentence and SHALL leave the Launch_Sentence word for word.
3. IF either of those specs' tasks is not ticked when this spec's implementation starts, THEN THE System SHALL stop before its first task and say which spec is unfinished, except the `review-documentation-lens` task that waits for this change to re-quote the eval prompts, which this spec's eval tasks do.
4. THE System SHALL leave the Wave_Reviewer's effort and model as they are.
5. THE Review_Arm SHALL name, in step 4's bar for style, structure, comments and tests, the same files the Launch_Sentence names: the repository's `CLAUDE.md`, `AGENTS.md`, files under `.claude/rules/` and contributing guide.

### Requirement 11: Document and prove the change

**User Story:** As an Owner, I want the reference docs and the evals to match the new rules, so that a reader knows where findings sit and a regression shows up before a benchmark run.

#### Acceptance Criteria

1. THE System SHALL describe in `docs/reference.md` and the README, where they describe anchoring, the merge, the Cap or the Wave_Review's launch, the rules of Requirements 1, 6, 7, 8 and 9, the Cap's removal included, and SHALL fix any stale cross-reference it finds there.
2. THE System SHALL update every eval prompt that quotes the Shared_Standard verbatim to quote it as this change leaves it.
3. THE System SHALL update the `evals/agents/review-arm/documentation-lens` case so that it expects the Finding on the changed code lines of `clamp/cli.py`, naming `README.md`.
4. THE System SHALL include Review_Arm eval cases for: one Defect at two Own_Edit_Places in two files, expecting one Finding in each naming the other; a code change that leaves an untouched document naming the old value, expecting one Finding on the code lines naming the document; the same wrong return in two files, expecting one Finding per file; and a New_Dependency that returns early under a configuration the tests never use, expecting a Finding that names the guard.
5. THE System SHALL include Review_Skill eval cases for: an Outside_Lens_Lead naming a planted defect that the Final_List must hold; and one planted Defect in three changed files, expecting one Finding in each.
6. THE System SHALL run `make validate` and no eval case until the Owner asks, each case then run by hand, one at a time.
7. THE System SHALL run no ReviewBench chunk to prove this change; the measure is the Owner's choice afterwards, and its scores need not compare with earlier chunks.
8. THE System SHALL keep the `checks/` unit tests of the ReviewBench_Adapter and the Benchmark_Report passing, changing only those that assert the Findings_Limit or the cap line.
