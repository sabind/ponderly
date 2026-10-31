# Requirements Document

## Introduction

When the `review` skill has the `wave-reviewer` read a pull request, the reviewer reports a team-rule departure with no concrete cost in the change as a nit, and the skill folds that nit into the final list as a low finding. On a short list nothing cuts it, so a Reviewer reads, and a benchmark judges, an opinion that names no harm: in ReviewBench chunk 3 both false findings the reviewer added were of this kind, one saying "That is scope creep with no concrete cost here" and the other "no concrete cost in this change can be shown", while the reviewer's other nits, small problems such as a stale list entry or a departure from how the file around the change is written, were judged real. This task stops the reviewer reporting a team-rule departure with no concrete cost as a finding, has it counted instead, widens the repository's own standard to its rule files, keeps what the review leaves out readable from the review's own JSON file, and leaves every other nit, and every other launch of the reviewer, as it is. It replaces Requirement 4.2 and the nit half of Requirement 4.5 of the `review-skill-second-pass-and-bar` spec, which stays as the record of what was built before. It serves the Reviewer, who reads the findings, and the Owner, who reads the benchmark score.

## Glossary

- **Reviewer**: A person who runs the Review_Skill on a pull request and reads its Final_List.
- **Owner**: The person who pays for each review and reads its benchmark score.
- **Review_Skill**: The plugin skill `review`, `plugins/ponderly/skills/review/SKILL.md`.
- **Wave_Reviewer**: The plugin's `wave-reviewer` agent, `plugins/ponderly/agents/wave-reviewer.md`.
- **Wave_Review**: The one launch of the Wave_Reviewer by the Review_Skill, with the merged findings quoted.
- **Launch_Sentence**: The sentence step 5 of the Review_Skill gives the Wave_Review verbatim, beginning "These changes are a pull request reviewed for the review skill".
- **Reviewer_Finding**: One entry of the Wave_Review's Findings block: a file, an exact quote, a problem and a severity of blocker, should-fix or nit.
- **Contradiction**: A Reviewer_Finding that says a finding of the Review_Skill's merged list is wrong, in its claim, its lines or its severity.
- **Team_Rules**: The handbook rules the plugin puts in every agent's context.
- **Repository_Bar**: What the reviewed repository's `CLAUDE.md`, `AGENTS.md`, files under `.claude/rules/`, its contributing guide and the code around the change already do or say about style, structure, comments and tests.
- **Concrete_Cost**: A harm a departure causes in this change that the finding can show, such as a test that cannot fail or a comment that contradicts the code.
- **Unreported_Departure**: A Team_Rules departure with no Concrete_Cost that does not also depart from the Repository_Bar.
- **Unsettled_Lead**: An `unsure` entry of the Wave_Review that is not an Unreported_Departure: a problem the Wave_Reviewer could not tie to a quote or verify at the head.
- **Not_Reported_List**: The list beside `findings` in the final Findings_File that holds, one entry per item, what the review left out of the Final_List and why.
- **ReviewBench_Adapter**: The benchmark's adapter under `benchmarks/reviewbench/agent/`, which reads only the Findings_File's `findings` and copies the file to the run folder's evidence as `review.json`.
- **Bar_Departure**: A change that does otherwise than the Repository_Bar does or says, such as a file written in another idiom than the code around it, or code a rule under `.claude/rules/` forbids.
- **Spec_Wave_Review**: Any launch of the Wave_Reviewer other than the Wave_Review: by `implement-spec`, `readable-code`, `tighten-tests` or an author directly.
- **Final_List**: The findings the Review_Skill returns, or writes to the Findings_File.
- **Findings_File**: The JSON file the Review_Skill writes when run with `--json`.
- **Count_Line**: The line after the Final_List that gives the Review_Skill's counts.
- **System**: The Review_Skill, the Wave_Reviewer and their documentation and evals.

## Requirements

### Requirement 1: Keep a cost-free team-rule departure out of the findings

**User Story:** As a Reviewer, I want the Wave_Review to leave out a team-rule departure that harms nothing in my change, so that every finding I read names a problem I would act on.

#### Acceptance Criteria

1. WHEN judging for the Review_Skill, THE Wave_Reviewer SHALL return no Reviewer_Finding for an Unreported_Departure.
2. WHEN judging for the Review_Skill, THE Wave_Reviewer SHALL list each Unreported_Departure under `unsure` as one entry that begins `departure not reported:` and gives its file, an exact quote and its problem, naming the Team_Rules rule it departs from.
3. WHEN judging for the Review_Skill, THE Wave_Reviewer SHALL read the Repository_Bar's files that exist before judging style, structure, comments and tests, and SHALL report a Bar_Departure with no Concrete_Cost as a nit.
4. WHEN judging for the Review_Skill, THE Wave_Reviewer SHALL report a Team_Rules departure with a Concrete_Cost at the severity its Findings section gives that cost, whether or not the Repository_Bar also shows it.
5. IF the Repository_Bar cannot be read, because the repository has none of its files and no code around the change, THEN THE Wave_Reviewer SHALL treat every Team_Rules departure with no Concrete_Cost as an Unreported_Departure.
6. WHILE judging a Spec_Wave_Review, THE Wave_Reviewer SHALL hold the changes to the Team_Rules as it does today, reporting a departure as a finding.

### Requirement 2: Count and keep what was left out

**User Story:** As an Owner, I want each review to say how many cost-free departures the reviewer left out and to keep each thing it left out in its JSON file, so that I can assess from the run folder whether the rule hides real problems.

#### Acceptance Criteria

1. WHEN the Wave_Review returns a Findings block, THE Review_Skill SHALL count its `unsure` entries that begin `departure not reported:` and add `departures not reported <n>` to the Count_Line, with 0 when there are none.
2. WHEN the Review_Skill writes the final Findings_File, THE System SHALL give the same number as `counts.departures_not_reported`.
3. IF the Wave_Review did not return or did not run, THEN THE Review_Skill SHALL leave `departures not reported` out of the Count_Line and write `counts.departures_not_reported` as 0.
4. WHEN the Review_Skill writes the final Findings_File, THE System SHALL write the Not_Reported_List as `not_reported`, with one entry for each Unreported_Departure, each Unsettled_Lead, each Reviewer_Finding counted as not anchored and each new Reviewer_Finding, one that is not a Contradiction, given to a relaunched arm that returned a second-pass list which leaves it out, each holding the file, the exact quote, the problem and the reason it was left out (`team-rule departure without cost`, `unsettled lead`, `not anchored` or `dropped by relaunched arm`), and `null` for a file or quote the entry does not give; the Count_Line's `not anchored` count stays as it is.
5. IF the Wave_Review did not return or did not run, or listed nothing under `unsure` but `nothing` and no Reviewer_Finding went unanchored or was dropped by a relaunched arm, THEN THE System SHALL write `not_reported` as an empty list.
6. THE System SHALL keep every Not_Reported_List entry out of `findings`, so that the ReviewBench_Adapter, which reads `findings` only, scores exactly what it scores today.
7. THE Review_Skill SHALL fold, relaunch and settle every Reviewer_Finding as it does today, a nit folding as low.

### Requirement 3: Change only the bar list and the cost-free clause of the Launch_Sentence

**User Story:** As an Owner, I want this change confined to the Launch_Sentence's bar list and cost-free clause and the Wave_Reviewer's matching rule, so that the other change in flight on the same sentence can build on it without a conflict.

#### Acceptance Criteria

1. THE System SHALL change in the Launch_Sentence only the list of what the Repository_Bar holds and the clause that tells the Wave_Reviewer how to report a Team_Rules departure, and SHALL leave the rest of the sentence word for word.
2. THE System SHALL change in the Wave_Reviewer only the review-skill paragraph of its Standard and the clause of its Findings section that names the departures that paragraph calls nits.
3. THE System SHALL record the old and new words of each changed clause in this spec's design, so that another change to the same sentence can be rebased on them.

### Requirement 4: Document and prove the change

**User Story:** As an Owner, I want the reference docs and the evals to match the new rule, so that a reader knows what a review reports and a regression shows up before a benchmark run.

#### Acceptance Criteria

1. THE System SHALL describe in `docs/reference.md`, in the `review` and `wave-reviewer` entries, the files of the Repository_Bar and that a cost-free team-rule departure is counted and not reported, and SHALL name the new count in the `review` entry's description of the Count_Line and the Not_Reported_List in its description of the Findings_File.
2. THE System SHALL update the `evals/agents/wave-reviewer/judges-by-the-repository-bar` case to give the new Launch_Sentence and to expect no divider-comment Reviewer_Finding at any severity and a `departure not reported:` entry under `unsure`, keeping its expectation that the floor division is should-fix or blocker.
3. THE System SHALL include an eval case for the Wave_Reviewer in which a change departs from how the code around it is written, at no Concrete_Cost, and the departure is reported as a nit.
4. THE System SHALL leave every eval case that quotes no changed text as it is.
5. THE System SHALL run no eval case until the Owner asks for it.
