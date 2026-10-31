# Requirements Document

## Introduction

The `review` skill reads a pull request through one review arm per lens, and today documentation is one clause among eight in the maintainability lens, so no arm proofreads the prose and configuration a change touches or looks for the documentation it leaves stale. In ReviewBench chunk 3, 14 of the 49 golden problems the review missed sat in such files, and on one pull request that changed about a dozen templates, which held 25 of the chunk's 74 golden problems, the review found 16% of them. This task adds a documentation lens, a sixth arm that reads every changed prose and configuration file, and every place the change makes documentation stale, for text a reader would act on wrongly, and narrows the maintainability lens so the two do not report the same sentence. It serves the Reviewer, who wants the README, help text and templates of a change checked like its code, and the Owner, who reads the review's score on the benchmarks.

## Glossary

- **Reviewer**: A person who runs the Review_Skill on a pull request and reads its findings.
- **Owner**: The person who pays for each review and reads its benchmark score.
- **Review_Skill**: The plugin skill `review`, `plugins/ponderly/skills/review/SKILL.md`.
- **Lenses_File**: The Review_Skill's `plugins/ponderly/skills/review/lenses.md`, whose shared standard and `##` sections define the arms.
- **Lens**: One `##` section of the Lenses_File, naming the problems its arm looks for and the categories its findings carry.
- **Review_Arm**: One launch of the plugin's `review-arm` agent by the Review_Skill, reading the pull request through one Lens.
- **Documentation_Lens**: The Lens this task adds, named `documentation`.
- **Maintainability_Lens**: The Lens named `maintainability` in the Lenses_File.
- **Prose_File**: A file meant to be read as text rather than run: Markdown, templates, help text, changelogs, and documentation pages, with the example commands they hold.
- **Config_File**: A file of settings or pipeline definition, such as workflow YAML, a manifest or front matter, read as text that names commands, paths or code.
- **Stale_Documentation**: A Prose_File, Config_File, comment or docstring, changed or not, that the pull request makes untrue, such as a README naming an option the change renamed.
- **Reader_Cost**: What a reader does wrong because of a text: runs a command that fails, follows a link that is broken, relies on a statement the code contradicts, or misreads a wrong term.
- **Arm_Eval_Case**: An eval case under `evals/agents/review-arm/` whose prompt quotes the Lenses_File's shared standard and one Lens verbatim.
- **Shared_Standard**: The sentences of the Lenses_File's opening paragraph from "Across every lens" to its end, sent to every Review_Arm.
- **System**: The Lenses_File, the Review_Skill, their documentation and their evals.

## Requirements

### Requirement 1: Proofread the change's prose and configuration

**User Story:** As a Reviewer, I want one arm to read every changed Prose_File and Config_File and the documentation the change makes stale, so that a wrong README, template or help text is found like a wrong line of code.

#### Acceptance Criteria

1. THE System SHALL hold the Documentation_Lens as a `##` section named `documentation` in the Lenses_File, so that the Review_Skill launches its Review_Arm with the others on every review.
2. THE Documentation_Lens SHALL direct its Review_Arm to read every changed Prose_File and Config_File in full at the head.
3. THE Documentation_Lens SHALL name these problems: text that contradicts the code or the commands it describes; broken markup, such as unmatched tags, bad links and malformed front matter; examples that would not run as written; typos, wrong terms and unprofessional wording in user-facing text, interface labels and help strings included; and Stale_Documentation elsewhere in the repository.
4. THE Documentation_Lens SHALL include in Stale_Documentation a comment or docstring that no longer matches code that is right, and SHALL leave code that does not do what its docstring says to the correctness Lens.
5. THE Documentation_Lens SHALL direct its Review_Arm to find Stale_Documentation by searching the repository for each symbol, option, command, path or file the change renamed, removed or altered, and to judge only the documentation that names one of them, never reading every Prose_File in the repository; WHILE a pull request changes no Prose_File and no Config_File, the arm SHALL still run that search.
6. THE Documentation_Lens SHALL carry the category `documentation`, and no other.
7. THE Documentation_Lens SHALL define a true positive as a finding that names the sentence and what it contradicts or the Reader_Cost it causes.
8. THE Documentation_Lens SHALL define a false positive as a style preference or a rewording with no Reader_Cost.
9. THE Documentation_Lens SHALL leave a change to a Config_File that breaks or weakens a build or CI pipeline to the reliability Lens, and take only a Config_File's comments, names and descriptions that contradict the commands or code they name.
10. THE Documentation_Lens SHALL give severity guidance: medium for an example that would not run as written, text that tells a reader to do the wrong thing, markup that hides content, and a broken link in a quickstart or install path; low for any other broken link and for a typo or a wrong term; high only when following the text loses data or breaks a user's setup.
11. IF the Review_Arm finds no problem the Documentation_Lens names, THEN THE System SHALL return the arm's block with no findings, as every Lens does.
12. THE correctness and reliability Lenses SHALL each name the Documentation_Lens as the owner of the stale text at their boundary: a stale comment or docstring on code that is right, and a Config_File's comment or description that no longer matches what it runs.

### Requirement 2: Keep the maintainability lens off the same sentence

**User Story:** As a Reviewer, I want the maintainability arm and the documentation arm to report different problems, so that one stale sentence is not reported twice under two lenses.

#### Acceptance Criteria

1. THE Maintainability_Lens SHALL keep, of its documentation clause, only a public contract that is missing its docstring and a comment that describes the algorithm instead of the intent.
2. THE Maintainability_Lens SHALL stop carrying the category `documentation`.
3. THE Maintainability_Lens SHALL name the Documentation_Lens as the owner of stale, misleading or contradicting text, as the other Lenses name the owners of their boundaries.
4. THE Maintainability_Lens SHALL leave unprofessional wording and reader-facing confusion in user-facing text to the Documentation_Lens.

### Requirement 3: Launch the sixth arm with no change to the skill's steps

**User Story:** As an Owner, I want the sixth arm to run through the same launch, merge, cap and count line as the other five, so that adding a lens costs one section and no change to the skill.

#### Acceptance Criteria

1. THE System SHALL confirm that no step of the Review_Skill and no part of the `review-arm` agent hard-codes five Lenses or names the five, and SHALL fix any that does.
2. WHEN the Review_Skill sorts a wave-review finding to a Lens, THE System SHALL let a documentation problem fall to the Documentation_Lens by the Lenses_File's own words.
3. THE System SHALL record in the design that a sixth arm adds about one arm's cost to every review, so that the budget rule, which compares remaining with spent, stops a second pass slightly more often.
4. THE Lenses_File SHALL name no benchmark, and neither SHALL the `review-arm` agent.
5. WHEN a Lens directs its Review_Arm to search beyond the files the pull request touches, THE `review-arm` agent SHALL search as far as the Lens says and report what it verifies there like any other finding.
6. THE `review-arm` agent SHALL run no code of the repository or the change, and SHALL settle each candidate by reading or leave it under `unsure`.

### Requirement 4: Document and prove the change

**User Story:** As an Owner, I want the reference docs to list the six lenses and an eval case to show the documentation arm at work, so that a reader knows what a review covers and a regression shows before a benchmark run.

#### Acceptance Criteria

1. THE System SHALL list the six Lenses in the `review` entry of `docs/reference.md` and say there what the Documentation_Lens reads.
2. THE System SHALL include an Arm_Eval_Case, `documentation-lens`, whose fixture's change renames a command-line option and leaves a README example using the old name, and which expects a `documentation` finding on the changed lines of `clamp/cli.py` that names the `README.md` example and the new option.
3. WHEN the Shared_Standard changes, THE System SHALL rebuild the `security-lens` Arm_Eval_Case's prompt from the Lenses_File, and SHALL rebuild it only after the change to the Shared_Standard in flight on the same file has landed.
4. THE System SHALL quote the Shared_Standard and the Documentation_Lens in the `documentation-lens` prompt verbatim from the Lenses_File as it stands when the case is written, and SHALL rebuild that prompt when either changes.
5. THE System SHALL name in the design the two ReviewBench measures the Owner chooses between afterwards, a single rerun of the `scotthamilton77/agents-config` pull request (Test_Set index 10, `make prs PRS="10"`) as the targeted check and the rerun of a whole chunk as the real measure, and SHALL include no run in its tasks.
6. THE System SHALL run no eval case until the Owner asks for it.
