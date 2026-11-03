# Requirements Document

## Introduction

The `review` skill reads a pull request through one review arm per lens and returns line-anchored findings. The ReviewBench chunk 3 rerun (run `2026-11-01T21-29-46-prs10-14`) missed 46 of the set's 74 golden problems, and reading the misses beside the arms' transcripts showed three causes. On a pull request that moved 29 files unchanged, the arms opened none of them, and 13 golden problems sit in those files; the golden set treats a moved file as touched, and the Owner holds the same view: a moved file's every line is touched. A claim about a third-party tool, that Codex resolves an `@file` include, was reported once and hedged "could not confirm", so the rule that puts a finding at every copy of a verified defect never fired for the two other templates, both golden highs. And the testing lens made 24 findings on one pull request while missing all six golden entries that ask for a test of a behaviour the change introduced, because the arm critiques the tests a change adds rather than listing the change's behaviours and looking for each one's test. This task makes the arms read every touched file whole, moved files included, and say what they read; lets an arm settle a third-party claim with a web search when one is available, without leaking the repository; and gives the testing lens a behaviour-first method. It serves the Reviewer, who reads the findings, and the Owner, who reads the benchmark score and the run's health.

## Glossary

- **Reviewer**: A person who runs the Review_Skill on a pull request and reads its findings.
- **Owner**: The person who pays for each review and reads its benchmark score and health report.
- **Review_Skill**: The plugin skill `review`, `plugins/ponderly/skills/review/SKILL.md`.
- **Lenses_File**: The Review_Skill's `plugins/ponderly/skills/review/lenses.md`.
- **Shared_Standard**: The sentences of the Lenses_File's opening paragraph from the sentence that begins "Across every lens, a finding worth reporting" to its end, sent to every Review_Arm.
- **Review_Arm**: One launch of the plugin's `review-arm` agent, `plugins/ponderly/agents/review-arm.md`, by the Review_Skill, reading the pull request through one lens.
- **Touched_File**: A file the pull request added, modified, moved or renamed, as the Review_Skill's changed-file list names it at the head.
- **Moved_File**: A Touched_File whose content at the head is the same as at the base under another path, which `git diff` shows as a rename with no content change.
- **Read_List**: The list, in an arm block, of the Touched_Files the Review_Arm read whole at the head and the other files it read, each with the line ranges read when not whole.
- **Unread_Count**: The number of Touched_Files that no Review_Arm's Read_List names as read whole.
- **Search_Tool**: A web search tool the host offers the Review_Arm, such as Claude Code's `WebSearch`, which returns page excerpts for a query.
- **Public_Fact**: The name of a third-party tool and the behaviour of it in question, as a search query may carry; never a line of the repository's code, a file name from it, the repository's name or the pull request.
- **Third_Party_Claim**: A statement a finding rests on about what a tool, library or service outside the repository does, such as whether a CLI resolves an include directive.
- **Behaviour**: Something the change makes the code do that it did not do before, or do differently: a new branch, a new input accepted, a new output, a changed result.
- **Findings_File**: The JSON object the Review_Skill writes to the path given with `--json`, as an interim object after the first merge and a final object at the end.
- **Review_Health**: The section of the ReviewBench report, `benchmarks/reviewbench/report.py`, that reads each pull request's Findings_File counts.
- **Adapter**: The ReviewBench entrypoint `benchmarks/reviewbench/agent/agent.py`, whose `FINDINGS_SHAPE` string describes the Findings_File to the repair session.
- **Arm_Eval_Case**: An eval case under `evals/agents/review-arm/` whose prompt quotes the Shared_Standard and one lens verbatim from the Lenses_File.
- **Review_Eval_Case**: An eval case under `evals/skills/review/` that runs the Review_Skill on a fixture.
- **System**: The Lenses_File, the Review_Arm, the Review_Skill, the Adapter's shape string, Review_Health, their documentation and their evals.

## Requirements

### Requirement 1: Read every touched file whole, moved files included

**User Story:** As a Reviewer, I want every file the change touches read whole by each arm, a moved file included, so that a defect on any line of a touched file is found whether the change wrote that line or only carried it.

#### Acceptance Criteria

1. THE Shared_Standard SHALL state that a Moved_File is a Touched_File whose every line counts as the pull request's, so that a verifiable problem on any of its lines is a finding at that line.
2. THE Review_Arm's read step SHALL read every Touched_File whole at the head, a Moved_File included, before looking through the lens.
3. THE Review_Arm's lens step SHALL look for each kind of problem the lens names in every line of every Touched_File, changed or not.
4. THE System SHALL add no argument to the Review_Skill for this: the behaviour holds for every review.
5. WHEN a Touched_File is absent at the head, THE Review_Arm SHALL treat it as deleted, as today, and anchor no finding to it.
6. THE System SHALL keep the Shared_Standard's other sentences as they stand, so that the eval prompts that quote it change only where this task changes it.

### Requirement 2: Record what each arm read

**User Story:** As an Owner, I want each arm to list the files it read, and the review to count the touched files no arm read, so that a miss like the 29 unopened files shows in the review's own output and the run's health.

#### Acceptance Criteria

1. THE Review_Arm's arm block SHALL carry a Read_List under a `read:` field after `unsure:`, one entry per file as `<path>: whole` or `<path>: <start>-<end>[, <start>-<end>...]`, or `read: []` when it read nothing.
2. THE Review_Skill SHALL treat an arm block without a `read:` list as malformed, as it treats one without `unsure:`.
3. THE Review_Skill SHALL compute the Unread_Count from the Read_Lists of the arms whose blocks it took and the changed-file list, and SHALL print it on the count line as `touched files no arm read <n>`.
4. WHEN `--json` is given, THE Findings_File SHALL hold a `read` object mapping each lens name to that arm's Read_List, from the first write, and `counts` SHALL hold `files_unread` as its ninth entry, 0 in the interim object and the Unread_Count in the final object.
5. THE Adapter's `FINDINGS_SHAPE` string SHALL name `files_unread` among the counts and `read` among the object's fields, and nothing else in the Adapter SHALL change.
6. THE Review_Health section SHALL print the sum of `files_unread` over the review files that record it and how many pull requests have a value above 0, saying how many review files record it, as it does for the counts added before.
7. IF an arm's Read_List names a file that is not a Touched_File, THEN THE Review_Skill SHALL keep it in the Findings_File's `read` object and leave it out of the Unread_Count.

### Requirement 3: Settle a third-party claim with search when a search tool is available

**User Story:** As a Reviewer, I want a finding that rests on what an outside tool does to be settled rather than hedged, so that a real defect copied into several files gets a finding at each copy instead of one guess.

#### Acceptance Criteria

1. WHERE a Search_Tool is available, THE Review_Arm SHALL use it to settle a Third_Party_Claim a candidate finding rests on, and SHALL report the finding as verified when the search settles it.
2. WHILE no Search_Tool is available, THE Review_Arm SHALL report a Third_Party_Claim it cannot settle from the repository once, under `unsure`, as unverified, and SHALL go on.
3. WHEN a Third_Party_Claim is settled, THE Review_Arm SHALL apply the Shared_Standard's per-copy rule to the defect it establishes, so that each copy verified at the head gets its own finding.
4. THE Review_Arm SHALL send only Public_Facts in a search query.
5. THE Review_Arm SHALL never open the pull request, its repository or its discussion on any host, and SHALL use no GitHub tool or API.
6. THE Review_Arm's `tools:` SHALL gain `WebSearch` and SHALL not gain `WebFetch`.
7. THE Review_Arm's text SHALL name the capability, a web search tool, not the tool, so that a host without one takes criterion 2.
8. THE System SHALL change no egress of the ReviewBench manifest for this, since the Search_Tool runs through the model API host the manifest already declares.
9. THE System SHALL add no search argument to the Review_Skill; WHILE the Review_Skill runs in an interactive session, whether a search runs SHALL be the host's permission decision for the Search_Tool.
10. THE Adapter SHALL pass `WebSearch` among the review launch's `--disallowedTools` unless `RB_SEARCH` is `1`, so that a headless review searches only when asked.
11. THE ReviewBench and Martian harnesses SHALL pass `RB_SEARCH` into the image, and their READMEs SHALL list it, `0` by default.
12. IF a search is refused or fails, THEN THE Review_Arm SHALL treat the claim as unverified, as criterion 2 says.
13. THE Adapter SHALL write whether web search is on to `adapter.log` when the review starts, and the ReviewBench and Martian harnesses SHALL record it in `run.json` as `search`.
14. THE ReviewBench and Martian reports SHALL show in their header whether web search was on, from `run.json`'s `search`, and `off` when `run.json` records none.

### Requirement 4: Find the tests a change should have

**User Story:** As a Reviewer, I want the testing lens to tell me which behaviour the change introduced has no test that would fail if it broke, so that the gaps reviewers ask about most are in the list.

#### Acceptance Criteria

1. THE Review_Arm's method for the testing lens SHALL list each Behaviour the change introduces or alters, find for each the test that would fail if it broke, and report each Behaviour with no such test as one finding at the Behaviour's place naming the test that would cover it, in the project's own test framework and style.
2. THE testing lens of the Lenses_File SHALL say that a true positive names the Behaviour, the place it lives and the test that would cover it, and that the arm lists the change's Behaviours before reading its tests.
3. THE testing lens SHALL keep its false-positive clause: no finding for coverage an existing test gives, for trivial code the project does not test, or for a test that would not catch a real regression.
4. THE System SHALL add no argument to the Review_Skill for this.
5. THE testing lens SHALL keep looking at the tests the change adds, as today, beside the Behaviours.

### Requirement 5: Prove and document the change

**User Story:** As an Owner, I want each change proved by an eval case and the reference docs to say what the arms now do, so that a regression shows before a benchmark run.

#### Acceptance Criteria

1. THE System SHALL include an Arm_Eval_Case, `reads-a-moved-file-whole`, whose fixture's change moves a file unchanged that holds a verifiable defect, and which expects a finding at that defect's line in the moved file and a Read_List naming the moved file as read whole.
2. THE System SHALL include an Arm_Eval_Case, `settles-a-third-party-claim`, whose fixture's change copies into two files a directive that a named third-party tool does not support, which grants the arm the host's web search tool, and which expects a finding at each copy and a query that holds only Public_Facts.
3. THE System SHALL include an Arm_Eval_Case, `names-the-missing-test`, with the testing lens, whose fixture's change adds a Behaviour with no test, and which expects one finding at the Behaviour naming the test that would cover it, and no finding on a Behaviour an existing test covers.
4. THE System SHALL include a Review_Eval_Case, `counts-the-files-no-arm-read`, which runs the Review_Skill with `--json` on a fixture and expects the Findings_File's `read` object with one key per lens, `files_unread` among the counts, and the count line's `touched files no arm read` entry.
5. THE System SHALL rebuild the prompt of every Arm_Eval_Case that quotes the Shared_Standard from the Lenses_File as it stands after the change.
6. THE System SHALL update the graders of the existing eval cases that parse an arm block for the new `read:` field.
7. THE System SHALL say in the `review` and `review-arm` entries of `docs/reference.md`, in `plugins/ponderly/README.md`, in `llms.txt` and in `benchmarks/reviewbench/README.md` what Requirements 1 to 4 add.
8. THE System SHALL run no eval case and no benchmark until the Owner asks.
9. THE search eval case SHALL run under an eval target of its own that grants `WebSearch`, and no other eval target SHALL grant it, so that the other arm cases keep the tools their earlier runs had.
