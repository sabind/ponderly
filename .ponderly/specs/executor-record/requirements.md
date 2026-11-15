# Requirements Document

## Introduction

When a `task-executor` agent finishes, its Summary lists the files it changed, the checks it ran and what it is unsure of, but not why it touched each file or what it did not know about it. The `wave-reviewer` agent that reads the work never sees the Summary at all: the launching skill collects the executors' `unsure` items beside the reviewer's Findings after the review. This change tunes the Summary's format, not its process: its file list becomes one entry per file or per group of files given the same change, each saying why it was touched, and each `unsure` item about one change names the files it concerns, so what the executor did not know sits beside the change it is about. The `unsure` field and the way every launcher handles it stay as they are. The reviewer is then given each executor's record and has it read every change first, form its own view, and only then hold each entry against what it read and say whether it matches. The hand-back then shows each executor's account of its work with the reviewer's check beside it. It serves the Operator, who sees which accounts the reviewer confirmed, and the Owner, who can trace each change to the reason given for it.

## Glossary

- **Executor**: The plugin's `task-executor` agent, defined in `plugins/claude/ponderly/agents/task-executor.md` and launched as `ponderly:task-executor`.
- **Reviewer**: The plugin's `wave-reviewer` agent, defined in `plugins/claude/ponderly/agents/wave-reviewer.md` and launched as `ponderly:wave-reviewer`.
- **Summary**: The fixed-shape report the Executor returns as its final text.
- **Change_Entry**: One entry of the Summary's record of work: the path of one changed file, or the paths of several files given the same change, with its Reason.
- **Reason**: What a Change_Entry's change does, in one sentence, followed by why it was made that way only when the code does not make that plain or the Executor chose one way of doing it over another.
- **Unsure_Item**: One entry of the Summary's existing `unsure` field: a point the Executor inferred rather than observed, could not verify, or noticed outside the task.
- **Record**: The Change_Entries and the Unsure_Items of one Executor's Summary, taken together.
- **Own_View**: The Reviewer's judgment of each change, formed from the diff, the cited excerpts and the citing files alone.
- **Record_Check**: The Reviewer's verdict on one Change_Entry, given after its Own_View is formed: whether the entry's paths and Reason match the change it read, with a quote where they do not, and what the code shows for each Unsure_Item about that entry the Reviewer could settle.
- **Records_Launcher**: A skill that launches both the Executor and the Reviewer and passes Records to the Reviewer: `implement-spec`, `readable-code` and `tighten-tests`.
- **Hand_Back**: The message a Records_Launcher writes to the Operator with the `report` skill at the end of a cadence unit or run.
- **Operator**: The person running a launching skill in their session, who reads its hand-back.
- **Owner**: The maintainer of the plugin, accountable for what its skills and agents do.

## Requirements

### Requirement 1: The Summary records each change

**User Story:** As an Operator, I want each Executor to say, for each file it touched, why it touched it and what it did not know, so that I can see the reasoning behind the work and not only its list of files.

#### Acceptance Criteria

1. THE Executor SHALL return in its Summary one Change_Entry for each file it created, edited or removed, or one Change_Entry for a group of files given the same change.
2. THE Executor SHALL name a file in exactly one Change_Entry.
3. THE Executor SHALL group files in one Change_Entry only when the same change, for the same Reason, was made in each of them.
4. THE Executor SHALL give each Change_Entry a Reason that says what the change does.
5. THE Executor SHALL keep the Summary's `unsure` field, with every item its procedure sends there today.
6. WHEN an Unsure_Item is about the change of one Change_Entry, THE Executor SHALL name in it the file or files of that entry.
7. WHEN the Executor stops with partial edits, THE Executor SHALL give each partially edited file a Change_Entry whose Reason says the edit is partial.
8. IF the Executor changed no file, THEN THE Executor SHALL say so in the record in one line.
9. THE Summary SHALL still let a launcher list every changed path from one field, as the launchers' `git status` and `deleted:` checks need.
10. WHEN a change is not plain from its code, or the Executor chose one way of doing it over another, THE Executor SHALL add to that entry's Reason why it was made that way.

### Requirement 2: The Reviewer reads the changes before the Records

**User Story:** As an Operator, I want the Reviewer to judge the changes on their own before it reads what the Executors said about them, so that its review stays impartial and its confirmation of each account means something.

#### Acceptance Criteria

1. WHERE the launch quotes Records, THE Reviewer SHALL form its Own_View of every change before it reads any Record.
2. THE Reviewer SHALL withdraw or soften no finding of its Own_View because a Record gives a reason for the change.
3. WHEN its Own_View is formed, THE Reviewer SHALL give one Record_Check for each Change_Entry the launch quotes.
4. IF a Change_Entry's Reason does not describe the change the Reviewer read, THEN THE Reviewer SHALL mark its Record_Check as not matching, with an exact quote of the entry and of the change.
5. IF a Change_Entry names a file the diff does not show changed, or the diff shows a file changed that no Change_Entry names, THEN THE Reviewer SHALL mark the Record_Check of that entry, or a Record_Check for that file, as not matching and name the file.
6. WHEN an Unsure_Item about a Change_Entry can be settled from the code, THE Reviewer SHALL say in that entry's Record_Check what the code shows, quoted.
7. IF a Record_Check that does not match shows the change itself is wrong, THEN THE Reviewer SHALL also report it as a finding at the severity the Findings section gives.
8. WHERE the launch quotes no Records, THE Reviewer SHALL review as it does today and give no Record_Checks.
9. WHEN the Reviewer reads files to settle Unsure_Items and the reads do not depend on each other, THE Reviewer SHALL make them in one message, not one read per turn.

### Requirement 3: Launchers pass the Records and show the checks

**User Story:** As an Operator, I want the hand-back to show each Executor's account of its work with the Reviewer's check beside it, so that I can tell at a glance which accounts were confirmed.

#### Acceptance Criteria

1. WHEN a Records_Launcher launches the Reviewer, THE Records_Launcher SHALL quote in the launch each Record of the Executors whose changes are under review, each with the task or group it came from.
2. WHEN a Records_Launcher launches the Reviewer, THE Records_Launcher SHALL put in the launch that the Records are to be read only after the Reviewer's Own_View is formed.
3. THE Hand_Back SHALL show each Record under review with its Record_Checks beside it.
4. IF a Record_Check does not match, THEN THE Records_Launcher SHALL list it under the Hand_Back's problems, quoted.
5. IF the Reviewer's Findings give no Record_Check for a Change_Entry the launch quoted, THEN THE Records_Launcher SHALL list that entry under the Hand_Back's problems as not checked.
6. THE Records_Launcher SHALL handle each Unsure_Item as it does today: fixed when it is a defect in a changed file, otherwise carried to the Hand_Back's problems.
7. WHEN a Record_Check settles an Unsure_Item from the code, THE Hand_Back SHALL show that item as settled, with what the code showed.
8. WHILE `implement-spec` resumes after an earlier hand-back, THE `implement-spec` skill SHALL take the Records of tasks ticked at that hand-back from that hand-back's report.
9. WHEN `start-task` shows an Executor's Summary on its executor route, THE `start-task` skill SHALL show the Record as part of the Summary, verbatim.

### Requirement 4: The documents that show the shapes agree

**User Story:** As an Owner, I want every page and eval that shows the Summary or the Findings to show the new shape, so that a reader is not told a field list the agents no longer return.

#### Acceptance Criteria

1. THE reference page `docs/reference.md` SHALL describe the Summary's Record and the Reviewer's Record_Checks.
2. THE guides that list the Summary's fields SHALL list the Record in place of the bare file list.
3. IF an eval grader of the Executor or the Reviewer asserts a field this change renames or removes, THEN THE grader SHALL be changed to assert the new field.
4. THE `review` skill, the `review-arm` agent and the `report` skill's templates SHALL be left unchanged.
