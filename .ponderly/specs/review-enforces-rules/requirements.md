# Requirements Document

## Introduction

When the `review` skill reads a pull request, its arms are told to judge style, structure, comments and tests by the reviewed repository's own bar, but nothing tells them to read the files that bar is written in, so a break of a rule the repository wrote down is caught only when an arm happens to open the file. Its findings say what is wrong, why it matters and what would fix it, in the reviewer's terms rather than those of the person who will live with the problem, and nothing in the review looks at the pull request's own title and body, the text a person reads first. This task has every arm read the repository's written rules and check the change against them, keeping how a rule is weighed as it is today; has every finding make its case as the user, operator or owner it lands on; and has the review suggest wording for the title and body where laying them out as that person would make the pull request easier to approach. It serves the Reviewer, who reads the findings, the Pull_Request_Author, who acts on them, and the Owner, who pays for each review.

## Glossary

- **Reviewer**: A person who runs the Review_Skill on a pull request and reads what it returns.
- **Pull_Request_Author**: The person who wrote the pull request and acts on the review.
- **Owner**: The person who pays for each review and reads its benchmark score.
- **Review_Skill**: The plugin skill `review`, `plugins/claude/ponderly/skills/review/SKILL.md`.
- **Arm**: One launch of the plugin's `review-arm` agent through one lens of the Review_Skill's `lenses.md`.
- **Wave_Review**: The one launch of the `wave-reviewer` agent by the Review_Skill.
- **Repository_Rules**: Those of the reviewed repository's `CLAUDE.md`, `AGENTS.md`, files under `.claude/rules/` and contributing guide that exist.
- **Repository_Bar**: The Repository_Rules and what the code around the change already does.
- **Team_Rules**: The handbook rules the plugin puts in every agent's context.
- **Rule_Break**: A change that does otherwise than a Repository_Rules sentence says.
- **Concrete_Cost**: A harm a departure causes in this change that the finding can show, such as a test that cannot fail or a comment that contradicts the code.
- **Affected_Role**: The user, the operator or the owner, chosen as the Team_Rules sentence "Lay out a problem, an explanation or a decision as the person it changes will live it" chooses the role that leads.
- **Case**: The part of a finding's message, after what is wrong and the fix, that says from the Affected_Role's point of view how they meet the problem, what the fix changes for them, and what of their experience suffers most if nothing changes.
- **Description**: The pull request's title and body as the Review_Skill receives them; "none given" when it receives none.
- **Description_Remark**: A suggestion on one passage of the Description that quotes it, says which Repository_Rules sentence it breaks or which Affected_Role it should be laid out for, and gives wording that meets it.
- **Final_List**: The findings the Review_Skill returns, or writes to the Findings_File.
- **Findings_File**: The JSON file the Review_Skill writes when run with `--json`.
- **Count_Line**: The line after the Final_List that gives the Review_Skill's counts.
- **System**: The Review_Skill, the `review-arm` and `wave-reviewer` agents, the lenses file, and their documentation and evals.

## Requirements

### Requirement 1: Check the change against the repository's written rules

**User Story:** As a Reviewer, I want every Arm to read the Repository_Rules and check the change against them, so that a rule the repository wrote down is upheld on every review and not only when an Arm happens to open its file.

#### Acceptance Criteria

1. THE Arm SHALL read each Repository_Rules file that exists before judging style, structure, comments or tests, in the turn in which it already reads the changed files.
2. WHEN a change makes a Rule_Break that the Arm's lens covers, THE Arm SHALL report it as a finding whose message quotes the Repository_Rules sentence it breaks.
3. WHERE a Repository_Rules file says which paths it applies to, THE Arm SHALL check against it only the changed files under those paths.
4. THE System SHALL weigh a departure from the Team_Rules as it does today: a finding when it has a Concrete_Cost and the Repository_Bar does not do otherwise, and otherwise left out of the findings and counted under `departures not reported`.
5. IF the reviewed repository has no Repository_Rules files, THEN THE Arm SHALL judge by the code around the change alone, as it does today.

### Requirement 2: Give a rule finding the severity of what it causes

**User Story:** As a Pull_Request_Author, I want a broken rule ranked by what it does to the change, so that a real defect is never sorted below a rule break that harms nothing.

#### Acceptance Criteria

1. THE System SHALL give a finding that is a Rule_Break the severity of the Concrete_Cost it shows, as for any other finding.
2. WHERE a Rule_Break shows no Concrete_Cost, THE System SHALL give it `low`, or the severity the broken Repository_Rules sentence itself implies, such as a rule against committing a secret.
3. THE System SHALL add no other ranking for a Rule_Break: the Final_List stays ordered high, medium, low, keeping the lenses' order within a severity.

### Requirement 3: Make each finding's case as the person it lands on

**User Story:** As a Pull_Request_Author, I want each finding to say what is wrong, the fix, and why it matters to the user, operator or owner who will live with it, so that I can see the stake and act on it without reconstructing it.

#### Acceptance Criteria

1. THE Arm SHALL write each finding's message as what is wrong, then what would fix it, then its Case, naming the Affected_Role, in at most 150 words on one line.
2. WHEN the Review_Skill launches the Wave_Review, THE Wave_Reviewer SHALL write each finding's `problem` as what is wrong, the fix and its Case, naming the Affected_Role, so that a finding the Review_Skill folds carries its Case into the Final_List.
3. IF the problem is small, as with a typo in a private name, THEN THE Arm SHALL write the message as what is wrong and the fix, naming the owner who maintains it in a few words, with no fuller Case.
4. WHILE the Wave_Reviewer is launched by anything other than the Review_Skill, THE Wave_Reviewer SHALL write its `problem` as it does today.

### Requirement 4: Suggest point-of-view wording for the title and body

**User Story:** As a Pull_Request_Author, I want the review to suggest wording for my title and body where laying them out as the person the change affects would help, so that a reader approaches the pull request through what it changes for them.

#### Acceptance Criteria

1. WHEN the Description is given, THE System SHALL read it against what the Repository_Rules and the repository's pull request template say a title or body should be and, where they say nothing, against the Team_Rules sentence "Lay out a problem, an explanation or a decision as the person it changes will live it", the repository's word prevailing where the two disagree, and return a Description_Remark for each passage that departs from that bar.
2. THE System SHALL return no Description_Remark for a passage that already meets that bar; a passage that describes only a mechanism does not meet it because another passage gives the Affected_Role's view.
3. IF the Description is "none given", THEN THE System SHALL return no Description_Remark.
4. THE Review_Skill SHALL show each Description_Remark as one line after the Count_Line, beginning `description remark:`, and never in the Final_List, so that a host posting the review can post the remarks as one top-level comment and the findings as line comments.
5. WHEN the Review_Skill writes the final Findings_File, THE System SHALL write each Description_Remark as a `not_reported` entry with `file` `null`, the quoted passage as its `quote`, the suggestion as its `problem` and `reason` `description remark`, so that it stays out of `findings`.

### Requirement 5: Keep the cost and the turns bounded

**User Story:** As an Owner, I want this change to add no launch and no turn to a review, and to know what it adds to each one, so that every review stays affordable.

#### Acceptance Criteria

1. THE System SHALL add no Arm, no Wave_Review and no other agent launch to a review.
2. THE System SHALL add no turn to an Arm's or the Wave_Reviewer's procedure: the reading of Requirement 1.1 and the check of Requirement 4.1 happen in steps that exist today.
3. THE System SHALL state in this spec's design the output each review is expected to add, in words per finding and in dollars per review at list price.

### Requirement 6: Leave the sibling changes room, document and prove

**User Story:** As an Owner, I want the change confined to the sentences it needs, the reference docs to match, and the behaviour proved before a benchmark, so that the unmerged sibling branches can be brought together with it and a regression shows up cheaply.

#### Acceptance Criteria

1. THE System SHALL leave unchanged the `effort:` lines, step 1 and step 3 of `agents/wave-reviewer.md` and `agents/review-arm.md`, step 3's effort text of the Review_Skill, step 4 and any `records:` section of `agents/wave-reviewer.md`, and every sentence of those three files this task does not need, without reflowing or reordering them.
2. THE System SHALL describe the Repository_Rules check, the Case in each finding and the Description_Remark in `docs/reference.md`'s `review`, `review-arm` and `wave-reviewer` entries.
3. THE System SHALL include an eval case for each of Requirements 1.2, 3.1 and 4.1, and SHALL update each existing eval case that quotes text this task changes.
4. THE System SHALL run no eval case or benchmark until the Owner asks for it.
5. WHEN the change is done, THE System SHALL pass `make validate`.
