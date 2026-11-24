# Requirements Document

## Introduction

Ponderly 1.10.0 (pull request #110) shipped the `switch-task` skill with seven eval cases, and building it left three gaps in them. Two cases describe earlier work their workspace does not hold, so they pass only while the model answers without looking. No case grades the offer when the author starts a Ponderly skill by hand after substantial work, which the merged spec `compact-at-task-switch` asks for in its criterion 4.9. And the two hand-off cases grade only the decline, with nothing written down about whether the full switch message could be graded there. This task makes the two workspaces hold what their prompts describe, adds a case for the offer at a skill started by hand and its opposite after a short exchange, and records that a hand-off case cannot grade the full switch message at an acceptable cost, with what covers it instead. It is for the contributors who run and trust these cases. The `switch-task` skill and the size hook do not change.

## Glossary

- **Case**: A directory under `evals/` holding a `prompt.md`, a `graders/` directory and a `scaffold.sh` that builds its Workspace.
- **Workspace**: The repository a Case's scaffold builds, in which the model runs.
- **Described_Work**: The earlier work, files, folders and decisions a Case's prompt says the session or the repository holds.
- **Offer**: The one-sentence proposal to run `ponderly:switch-task` before starting the requested work, as the skill's description sets it.
- **Substantial_Work**: Earlier work in the session of the kind the skill's description names: a skill run to its end, several files read or changed, sub-agents or long command output, or a long exchange.
- **Short_Exchange**: Earlier work of the kind the skill's description says gets no Offer: a question answered, one file read or a small edit.
- **By_Hand_Start**: A message from the author that starts a Ponderly skill with its typed `/ponderly:<skill>` command, not through another skill's hand-off.
- **Hand_Off_Case**: Either of `evals/skills/lld/switches-at-the-hand-off` and `evals/skills/bugfix/hands-off-to-pr`, in which a skill invokes `ponderly:switch-task` at its end.
- **Switch_Message**: The message the `switch-task` skill ends its turn with, holding the `/compact` line and each next step.
- **Size_Hook**: `plugins/claude/ponderly/hooks/switch-size.sh`, which declines a `ponderly:switch-task` call in a session under its limit.
- **Paid_Run**: A run of a Case with `make eval-…`, which is a real model call on the Author's seat.
- **Author**: The person who approves this spec and its Paid_Runs.

## Requirements

### Requirement 1: A workspace holds what its prompt describes

**User Story:** As a contributor, I want the Workspace of a `switch-task` Case to hold the Described_Work, so that a model that checks the repository before replying finds the prompt true and the Case does not fail for a reason that has nothing to do with the skill.

#### Acceptance Criteria

1. THE Workspace of `evals/skills/switch-task/offers-at-an-unrelated-request` SHALL hold every file and folder its prompt names as read or changed: a `subtract(a, b)` function in `calc/ops.py`, its tests in `tests/test_ops.py`, and the spec folder for it.
2. THE Workspace of `evals/skills/switch-task/writes-the-compact-line` SHALL hold `.ponderly/specs/visit-counter/`, and that folder SHALL state the two decisions the prompt carries: counting with `calc.ops.add`, and skipping a repeated `event_id`.
3. THE two Cases SHALL keep their prompts' requests, their graders and their expected outcomes, so that what each proves does not change.
4. IF a `switch-task` Case's prompt names a path, a function or a decision as Described_Work, THEN THE Case's Workspace SHALL hold it, for all seven Cases this task leaves under `evals/skills/switch-task/`.

### Requirement 2: The offer at a skill started by hand is graded

**User Story:** As a contributor, I want a Case that grades the Offer at a By_Hand_Start after Substantial_Work, so that criterion 4.9 of the merged spec is proved by a run and a change to the skill's description that loses it is seen.

#### Acceptance Criteria

1. THE suite SHALL hold one Case under `evals/skills/switch-task/` whose prompt is a By_Hand_Start in a session described as holding Substantial_Work of an earlier, finished task, with a Workspace that holds that Described_Work.
2. WHEN that Case runs, ITS graders SHALL pass only when the reply makes the Offer, speaks of switching tasks or compacting, and waits for the Author's answer.
3. WHEN that Case runs, ITS graders SHALL pass only when the started skill's work has not begun: no file is written and none is edited.
4. IF the reply begins the started skill's first step with no Offer, THEN THE Case SHALL fail.

### Requirement 3: No offer at a skill started by hand after a short exchange

**User Story:** As a contributor, I want the opposite Case, a By_Hand_Start after only a Short_Exchange, so that the Case of Requirement 2 cannot be passed by a model that offers at every skill start.

#### Acceptance Criteria

1. THE suite SHALL hold one Case under `evals/skills/switch-task/` whose prompt is a By_Hand_Start of the same skill as the Case of Requirement 2, in a session described as holding only a Short_Exchange, with a Workspace that holds that Described_Work.
2. WHEN that Case runs, ITS graders SHALL pass only when the reply makes no Offer and does not speak of switching tasks or compacting.
3. WHEN that Case runs, ITS graders SHALL pass only when the started skill begins its first step.
4. IF the reply makes the Offer, THEN THE Case SHALL fail.

### Requirement 4: The limit of the hand-off cases is on record

**User Story:** As a contributor, I want it written down that a Hand_Off_Case grades only the decline and why, so that nobody reads the two Cases as proof of the full Switch_Message at a hand-off, or spends a Paid_Run finding out.

#### Acceptance Criteria

1. THE design of this spec SHALL state that a Hand_Off_Case cannot grade the full Switch_Message at an acceptable cost, and why: the Size_Hook reads the session's real size, declines under 150,000 tokens, or 110,000 before `implement-spec`, and has no override, so a Case would have to fill its session to that size, at an estimated $2 to $4 a run against $0.62 for the `lld` Case today.
2. THE design SHALL name what covers each part instead: `checks/test_switch_size.py` for what the Size_Hook prints when it allows the call, `evals/skills/switch-task/writes-the-compact-line` for the Switch_Message, and the part no Case or check covers, the size sentence the Switch_Message carries after an allowed call.
3. THE `evals/README.md` SHALL say the same in its own words, since a merged spec is not where a contributor looks for how the Cases work today.
4. THE two Hand_Off_Cases SHALL stay as they are.

### Requirement 5: The change stays inside the eval suite and costs nothing until the Author says so

**User Story:** As the Author, I want this task to touch only the eval Cases and their documentation and to run no Paid_Run by itself, so that the skill I shipped is not changed by a test fix and I decide what is spent.

#### Acceptance Criteria

1. THE task SHALL change no file under `plugins/claude/ponderly/skills/switch-task/` or `plugins/claude/ponderly/hooks/`, and none under `.ponderly/specs/compact-at-task-switch/`.
2. WHEN the task's changes are complete, `make validate` SHALL pass.
3. THE task SHALL make no Paid_Run; the task list SHALL name each Paid_Run that proves the changed and new Cases, one sample run first, for the Author to approve.
4. IF a sample Paid_Run of a new Case fails because of the Case, THEN THE Case SHALL be corrected before any further Paid_Run, and IF it fails because of the skill, THEN THE task SHALL stop and report it, since the skill is out of scope.
