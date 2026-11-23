# Requirements Document

## Introduction

When a Ponderly skill finishes and hands off to the next one, the session still carries everything the finished work read and said, and the next skill pays to re-read it on every turn. This feature makes each such hand-off a Task_Switch: the finishing skill stops and shows the author the command that compacts the session, with one line saying what to keep for the next task, and then the command that starts the next task. The author runs them, or ignores the compaction and starts the next skill. It is for anyone who runs more than one Ponderly skill in a session, and its value is a next task that starts from a short summary in place of the whole earlier conversation.

Claude Code lets no skill, hook or agent start a compaction; only the author's own `/compact` does, and it takes the text typed after it as instructions for the summary. So the feature never compacts for the author. It writes the line to copy and stops. It saves no file, and its one hook only reads the session's size to decline a switch that would not pay: a first build that saved the summary to a file and passed it through hooks was dropped on 19 November 2026 as more machinery than the goal needs.

## Glossary

- **Task_Switch**: The point where the session moves from one task to another: a Ponderly skill has finished and names the skill that comes next, or the author asks for work unrelated to what the session holds.
- **Natural_Switch**: A Task_Switch the author makes in their own words, outside any Switching_Skill's final step.
- **Switch_Skill**: The one skill that makes a Task_Switch, run by a Switching_Skill, by the author, or on the author's yes to an offer.
- **Switching_Skill**: A Ponderly skill whose final step makes a Task_Switch: `strategy`, `hld`, `lld`, `start-task`, `implement-spec` and `bugfix`. `readable-code` and `tighten-tests` are not among them; the offer of Requirement 4 covers a switch into or out of them.
- **Next_Step**: What the session does next: the command that starts the next skill, with its arguments, as the Switching_Skill would otherwise have named it, or at a Natural_Switch the author's new request in their words. A skill that ends with several candidates, as a strategy ends with several high level designs, has several Next_Steps, and the author picks one after the Compaction.
- **Compact_Focus**: The one line the Switch_Skill writes after `/compact`, saying what the session just finished, what it does next, and what the summary should keep for that.
- **Substantial_Work**: Work in the session that the next task would pay to re-read on every turn: a Ponderly skill run to its end, several files read or changed, sub-agents or long command output, or a long exchange. A question answered, one file read or a small edit is not. The model is shown no token count, so this is judged from what the conversation holds.
- **Compact_Line**: `/compact` followed by the Compact_Focus, on one line, ready to copy.
- **Switch_Message**: The Switch_Skill's last message at a Task_Switch, which shows the Compact_Line and the Next_Step.
- **Session_Size**: The total input tokens of the session's last request in the main conversation, read from the session's transcript; when a Compaction has happened since that request, the size the Compaction left; zero when it cannot be read.
- **Switch_Limit**: The Session_Size below which a Compaction costs more than it saves: 110,000 tokens when the only Next_Step starts `implement-spec`, and 150,000 otherwise. It comes from the cost of one switch and the number of requests each skill ran for in the Author's sessions, measured on 23 November 2026, and is corrected when those are measured again.
- **Size_Hook**: The plugin's hook that runs before the session invokes the Switch_Skill.
- **Compaction**: Claude Code replacing the conversation with a summary, started by the author's `/compact` or by Claude Code itself.

## Requirements

### Requirement 1: Stop at a task switch and present the compaction

**User Story:** As an author, I want a skill that has finished to stop and show me how to compact before the next task, so that I do not carry the finished task's whole conversation into the next one.

#### Acceptance Criteria

1. WHEN a Switching_Skill reaches a Task_Switch, THE Switching_Skill SHALL end its turn with a Switch_Message and SHALL NOT start the next skill itself.
2. THE Switch_Message SHALL say that the task is switching, show the Compact_Line on a line of its own ready to copy, and show each Next_Step on a line of its own.
3. THE Switch_Message SHALL say in one sentence that the author may skip the compaction and run the Next_Step as it is.
4. WHEN the author's next message is anything other than the Compact_Line, THE session SHALL act on that message and SHALL NOT ask for the compaction again at that Task_Switch.
5. IF a Switching_Skill ends without naming a next skill, as when the author stops or the skill fails, THEN THE Switching_Skill SHALL write no Switch_Message.
6. WHERE, at a Natural_Switch, the author's new request is unrelated to the work the session holds and nothing from that work needs carrying into it, THE Switch_Message SHALL show `/clear` in place of the Compact_Line, and SHALL say that it starts fresh and that the earlier conversation can be reached again with `/resume`. A Switching_Skill's own hand-off always shows the Compact_Line.

### Requirement 2: The skill writes the line that steers the compaction

**User Story:** As an author, I want the skill that did the work to say what the next task needs, so that I copy one line and do not write the compaction's focus myself.

#### Acceptance Criteria

1. THE Compact_Focus SHALL say, in this order, what the session just finished, what the next task will do and which files it will read, and what to keep: the decisions the author made that the next task must follow and the problems still open. It SHALL end by telling the summary to drop the detail of the finished work.
2. THE Compact_Line SHALL be one line with no line break and SHALL be at most 600 characters.
3. THE Compact_Focus SHALL leave out what the next task can read from a file it names.
4. THE Switch_Skill SHALL save no file and run no command to make a Task_Switch.
5. IF the session holds no decision and no open problem the next task needs, THEN THE Compact_Focus SHALL leave that part out and SHALL still end by telling the summary to drop the detail of the finished work.

### Requirement 3: One shared switch, wired into every Switching_Skill

**User Story:** As a maintainer, I want one description of the Task_Switch that every Switching_Skill uses, so that the behaviour is the same everywhere and changes in one place.

#### Acceptance Criteria

1. THE plugin SHALL hold the Task_Switch's procedure, the Compact_Focus's contents and the Switch_Message's shape in one place.
2. THE final step of each Switching_Skill SHALL use that one place and SHALL NOT restate its procedure.
3. WHERE a Switching_Skill ends with several candidate Next_Steps, THE Switching_Skill SHALL make one Task_Switch that lists them all and SHALL NOT stop to ask the author which comes next.
4. THE feature SHALL add no hook and no script to the plugin other than the Size_Hook, SHALL name no terminal, editor or session manager in its shipped text, and SHALL type nothing on the author's behalf.

### Requirement 4: Offer the switch when the author changes task in their own words

**User Story:** As an author, I want the session to offer the switch when I start something unrelated, so that I save the tokens without having to remember the command.

#### Acceptance Criteria

1. THE Switch_Skill SHALL take two optional parameters: the Next_Step, and what to carry over in the author's words.
2. WHEN the author gives what to carry over, THE Compact_Focus SHALL hold it among the decisions to keep and SHALL leave out what the author said to drop.
3. WHEN the author asks for work unrelated to the task the session holds and the session already holds Substantial_Work of another task, THE session SHALL offer once, before starting the new work, to run the Switch_Skill, and SHALL say that it saves re-reading the earlier task on every turn.
4. WHEN the author accepts the offer, THE session SHALL run the Switch_Skill with the author's new request as the Next_Step.
5. WHEN the author declines the offer or answers with anything else, THE session SHALL start the new work and SHALL NOT offer again for that request.
6. WHILE a Ponderly skill is in the middle of its steps, THE session SHALL make no such offer.
7. IF the session holds no Substantial_Work, as at its start or after a short exchange, THEN THE session SHALL make no offer.
8. THE offer SHALL be carried by the Switch_Skill's own description and SHALL add no text to the plugin's rules.
9. WHEN the author starts a Ponderly skill by hand in a session that holds Substantial_Work of an earlier task, and no Switch_Message was shown for that step, THE session SHALL make the same offer once, before the skill's first step, with the typed command as the Next_Step.

### Requirement 6: Switch only when the session is large enough

**User Story:** As an author, I want the switch only when the session is big enough for compacting to pay, so that a small session is not charged for a compaction that saves nothing.

#### Acceptance Criteria

1. WHEN the session invokes the Switch_Skill and the Session_Size is above zero and below the Switch_Limit, THE Size_Hook SHALL decline the invocation and SHALL tell the session the Session_Size, not to retry, and to name each Next_Step to the author.
2. WHEN the Size_Hook has declined, THE session SHALL tell the author in one line the Session_Size, the Switch_Limit and that compacting is not worth it yet, SHALL name each Next_Step, SHALL say how the author can switch anyway, and SHALL write no Switch_Message.
3. WHEN the session invokes the Switch_Skill and the Session_Size is at or above the Switch_Limit, THE Size_Hook SHALL let the Switch_Skill run and SHALL give the session the Session_Size, and THE Switch_Message SHALL state it.
4. IF the Session_Size is zero, THEN THE Size_Hook SHALL let the Switch_Skill run and SHALL add nothing.
5. THE Size_Hook SHALL act on no other skill and no other tool, SHALL save no file, and SHALL exit 0 on every input, including one that is not JSON.
6. WHEN the author types the Switch_Skill's own command, THE Switch_Skill SHALL run whatever the Session_Size, since the author asked for it.

### Requirement 5: Proved in real sessions and measured before release

**User Story:** As the owner, I want the switch seen working at each kind of hand-off and its effect measured, so that the release rests on what happened and not on what the text says.

#### Acceptance Criteria

1. THE change SHALL be tried in a real session at four Task_Switches: `lld` to `start-task`, `start-task` to `implement-spec`, `implement-spec` to `pr`, and one Natural_Switch.
2. WHEN each trial is done, THE record of it SHALL show the Switch_Message, that the pasted Compact_Line compacted the session, and whether the next skill ran without asking for anything the Compact_Focus should have carried.
3. THE record SHALL give, for each trial, the tokens re-read per turn before and after the Compaction, from the session's transcript.
4. THE documentation SHALL cite the Claude Code documentation for the claim this feature rests on about what `/compact` does with the text after it.
