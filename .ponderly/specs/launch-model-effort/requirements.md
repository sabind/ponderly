# Requirements Document

## Introduction

Ponderly's skills launch four agents, and each agent's own file pins one model and one effort for every launch. Since the 1.8.0 pins, the agents at high effort spend most of their output on thinking. The wave reviewer on Opus at high also writes about four times the output of an executor per launch and re-reads about ten times its cached context, because it takes about 24 turns with one tool call each.

This change does four things:
- It makes medium the effort every agent runs at by default, and keeps Opus only for the wave reviewer, which reads across a whole wave or review.
- It has each launching skill propose an effort before it launches, so the author learns the cost before it is spent.
- It lets the skill that launches the task executor pick Haiku or Sonnet for each task by how small the task is, and moves the work to Sonnet without asking when Haiku falls short.
- It has the two code reviewers gather what they read in fewer turns.

The author gets the same work for fewer tokens, and each agent's token count can be compared before and after.

## Glossary

- **Agent_File**: One of the four agent definitions under `plugins/claude/ponderly/agents/`, whose frontmatter `model` and `effort` apply to a launch that passes neither.
- **Executor**: The `task-executor` agent, addressed as `ponderly:task-executor`.
- **Wave_Reviewer**: The `wave-reviewer` agent. In `implement-spec` it reads a whole wave of executor work. It also reads a whole readable-code or tighten-tests pass, and in `review` it reads a whole review with every lens's merged findings.
- **Lens_Arm**: The `review-arm` agent, which reads one pull request through one lens.
- **Document_Reviewer**: The `document-reviewer` agent, which reads one strategy, high level design or low level design draft.
- **Launching_Skill**: A skill that launches any of the four agents: `start-task`, `implement-spec`, `readable-code`, `tighten-tests`, `review`, `strategy`, `hld` and `lld`.
- **Executor_Skill**: A Launching_Skill that launches the Executor: `start-task`, `implement-spec`, `readable-code` and `tighten-tests`.
- **Executor_Launch**: One launch of the Executor by an Executor_Skill, for one task, one File_Group, or one fix.
- **Launch_Model**: The `model` value an Executor_Launch passes on the Agent tool call, `haiku` or `sonnet`.
- **Small_Task**: A task with all of these traits:
  - it changes at most one file;
  - it adds no new function, branch or test;
  - it needs no design choice;
  - it can be done from the task text and that one file.

  Examples are a wording change, a changed value or a rename inside one file.
- **Shortfall**: A result that falls short. It is one of:
  - a Summary with `status: stopped`;
  - a check under `checks run` that failed;
  - the launching skill's own verification failing;
  - a review finding sent back to the Executor.
- **Escalation**: Launching a new Executor on Sonnet for work whose last Executor_Launch ran on Haiku and came back with a Shortfall.
- **Effort_Proposal**: The statement a Launching_Skill makes to the author before it launches agents. It gives the effort it proposes for those launches and why, by the High_Effort_Criteria, and what the higher level is expected to cost against medium.
- **High_Effort_Criteria**: The conditions under which an Effort_Proposal proposes `high` for a reviewer launch in place of `medium`. They are a starting judgement, which the comparison in Requirement 4 is meant to correct.
- **Gathering_Step**: The first step of the Wave_Reviewer's and the Lens_Arm's procedure, in which the agent reads the diff and the files it reviews.
- **Token_Baseline**: The per-agent token counts of launches since 9 November 2026, before this change, as the lead's `agent_tokens.py` and `reviewer_turns.py` report them. They cover median turns, median and p90 output tokens, thinking share, median cache-read tokens and turns that hold one tool call.

## Requirements

### Requirement 1: Every agent runs at medium effort by default

**User Story:** As an author, I want every agent to run at medium effort unless I choose otherwise, so that the reviewers stop spending most of their output on thinking.

#### Acceptance Criteria

1. THE Executor, the Lens_Arm, the Document_Reviewer and the Wave_Reviewer Agent_Files SHALL each set `effort: medium`.
2. THE Lens_Arm and the Document_Reviewer Agent_Files SHALL set `model: sonnet`.
3. THE Wave_Reviewer Agent_File SHALL set `model: opus`, because it reads every executor's report and code, or every lens's output, at once.
4. THE Executor Agent_File SHALL keep `model: sonnet`, so that a launch passing no Launch_Model, such as the author launching the Executor by name, runs on Sonnet.
5. THE launches of the Lens_Arm, the Document_Reviewer and the Wave_Reviewer SHALL pass no `model`, so that their Agent_Files decide it.

### Requirement 2: The launching skill picks the Executor's model per task

**User Story:** As an author, I want each Executor_Launch to run on Haiku when the task is small and on Sonnet otherwise, so that small tasks cost less without large tasks losing quality.

#### Acceptance Criteria

1. WHEN an Executor_Skill makes an Executor_Launch for a Small_Task, THE Executor_Skill SHALL pass the Launch_Model `haiku`.
2. WHEN an Executor_Skill makes an Executor_Launch for a task that is not a Small_Task, THE Executor_Skill SHALL pass the Launch_Model `sonnet`.
3. IF an Executor_Skill cannot tell from the task text and the files it names whether a task is a Small_Task, THEN THE Executor_Skill SHALL treat it as not a Small_Task.
4. WHEN `implement-spec` or `start-task` states a task before launching it, THE skill SHALL name the Launch_Model beside the task, so the author sees which model each task ran on.

### Requirement 3: Work that falls short on Haiku moves to Sonnet without asking

**User Story:** As an author, I want work that Haiku did not finish to go to Sonnet on its own, a stop included, so that a wrong guess about a task's size costs one extra launch and not a question to me or a failed task.

#### Acceptance Criteria

1. WHEN a Shortfall follows an Executor_Launch that ran on Haiku, THE Executor_Skill SHALL make one Escalation without asking the author, whatever its rules say about relaunching after that Shortfall on Sonnet.
2. WHEN a Summary with `status: stopped` follows an Executor_Launch that ran on Haiku, THE Escalation SHALL carry the Haiku Summary's `stopped because`, quoted, and the files that already hold partial edits.
3. WHEN a Shortfall follows an Executor_Launch that ran on Sonnet, an Escalation included, THE Executor_Skill SHALL handle it as its rules say today, with the Launch_Model `sonnet` for any relaunch or fix they allow.
4. THE Executor_Skill SHALL never escalate an Executor_Launch beyond Sonnet.
5. IF the Agent tool runs a launch on a model other than its Launch_Model, such as when `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is set, THEN THE Executor_Skill SHALL carry on with the result as it would for any other launch.

### Requirement 4: The effect can be checked against the baseline

**User Story:** As an owner, I want the token use and the review quality after this change compared with the Token_Baseline, so that I know what the change saved and whether the reviewers still find what they found.

#### Acceptance Criteria

1. THE spec SHALL record the Token_Baseline as measured on 11 and 12 November 2026.
2. THE spec SHALL say how each agent's turns per launch, and turns holding exactly one tool call, are compared before and after the change, since Requirement 6 is meant to lower them.
3. THE spec SHALL say how the reviewers' findings at medium are compared with their findings at high without a paid eval run, and which paid run would settle it, with its cost.

### Requirement 5: The skill proposes the effort before it launches

**User Story:** As an author, I want each Launching_Skill to propose an effort and say what it costs before it launches agents, so that I learn the cost before it is spent and can change the level.

#### Acceptance Criteria

1. WHEN a Launching_Skill is about to make its first launch of a run, THE Launching_Skill SHALL make an Effort_Proposal to the author.
2. THE Effort_Proposal SHALL propose `medium` for every launch, except a reviewer launch that meets one of the High_Effort_Criteria, for which it SHALL propose `high` and name the criterion met.
3. WHERE the Effort_Proposal proposes `high`, THE Effort_Proposal SHALL say what a launch at high is expected to cost against medium, from the Token_Baseline.
4. WHERE a Launching_Skill already asks the author a set-up question before its first launch, THE Effort_Proposal SHALL be part of that question, and the author's answer SHALL set the effort.
5. WHERE a Launching_Skill asks no set-up question before its first launch, THE Launching_Skill SHALL state the Effort_Proposal before launching and take a level the author names in the request.
6. WHEN the chosen effort for a launch differs from its Agent_File's `effort`, THE Launching_Skill SHALL pass it as the launch's `effort`, and pass no `effort` otherwise.
7. THE High_Effort_Criteria SHALL be written in the spec as a starting judgement that the comparison in Requirement 4 is meant to correct.
8. IF a launch that passes `effort` fails because the Claude Code version is older than 2.1.292, THEN THE Launching_Skill SHALL launch again without `effort` and tell the author the chosen level could not be applied.

### Requirement 6: The code reviewers gather in few turns

**User Story:** As an owner, I want the Wave_Reviewer and the Lens_Arm to gather their diffs and files in a few turns, so that a launch does not re-read its growing context once for every file.

#### Acceptance Criteria

1. THE Wave_Reviewer's Gathering_Step SHALL get the diff of every listed tracked file in one command.
2. THE Lens_Arm's Gathering_Step SHALL get the diff of every changed file in one command.
3. THE Gathering_Step of both agents SHALL make reads that do not depend on each other in one message.
4. THE change SHALL be limited to the Gathering_Step of each agent, so that other edits to those files on sibling branches do not conflict with it.
