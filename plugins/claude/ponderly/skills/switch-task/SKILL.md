---
name: switch-task
description: Makes one task switch. Writes a short focus, then ends the turn with a message showing `/compact` with that focus and each next step, so the next task starts from a short summary, not the whole earlier conversation. Skills strategy, hld, lld, start-task, implement-spec and bugfix invoke it at their end instead of naming the next command. Also offer it, once and in one sentence, when the author asks for unrelated work and the session holds substantial work (a skill run to its end, several files read or changed, sub-agents or long command output, a long exchange), before that work starts; on a yes invoke it with that request as the argument; say it saves re-reading the earlier task each turn. A short exchange (a question answered, one file read, a small edit) gets no offer. A skill started by hand with such work held and no switch message shown for that step gets the same offer. If the author declines or answers anything else, start the work and do not offer again. Never offer it inside another skill's steps.
argument-hint: "[next step] [carry: what to keep]"
---

# Switch task

Write what the next task needs, then end the turn so the author can compact. Start no skill and no work of the next task, and type nothing on the author's behalf.

## Working with the author

- **Stops.** The turn ends with the Message of step 3.
- **How it asks.** Only in step 1, in prose, when there is no next step.
- **Hand-backs.** The Message of step 3.
- **Hand-offs.** The next step, shown in the Message.

## 1. Take the arguments

The whole text is `$ARGUMENTS`. What follows `carry:` is what the author wants kept, in their words; the rest is the Next_Step, the command that starts the next skill with its arguments, or the author's new request in their words. The rest may hold several Next_Steps, one for each candidate the skill ended with, as a strategy ends with several high level designs; take each as its own, and do not ask which comes next.

With no Next_Step in `$ARGUMENTS`, take the author's last request, which when the author has just said yes to an offer to switch is the unrelated request they made before the offer, not the yes. Only when there is neither, ask what the next step is, and wait.

Then choose the form of the message. It is the `/clear` form only when another Ponderly skill did not invoke this skill at its final step in this turn (the author typed the command or said yes to the offer, whatever the Next_Step looks like), and the next work is unrelated to what the session holds, and `carry:` holds nothing. When in doubt, or when `carry:` holds anything, it is the Compact_Line form. A Switching_Skill's hand-off always gets the Compact_Line form.

## 2. Write the Compact_Focus

For the `/clear` form, skip this step. Write the Compact_Focus as plain sentences on one line, in this order, leaving out the third when it has nothing to hold and never the fourth:

```
We just finished <the work, in a few words>. Next we <what the next task does>, which reads <paths>. Keep <the decisions the next task must follow, and the problems still open>. Drop the detail of the finished work.
```

- Name a file by its path and leave out what it holds; the next task reads it.
- Put what the author asked to carry under the decisions, and leave out what they said to drop.
- Keep only the decisions the author made that the next task must follow.
- Put the open problems under what to keep with the decisions.
- When the session holds no decision and no open problem the next task needs, leave out the third sentence and say only what was finished and what comes next, and still end with the fourth sentence.
- With several Next_Steps, name the kind of work and the document, not one step.

The Compact_Line is `/compact ` followed by the Compact_Focus, on one line with no line break, at most 600 characters. Before writing the message, count the Compact_Line's characters; when it runs past 600, shorten what to keep first, then drop paths a named folder already covers, and count again, until it is at most 600; never cut what comes next.

## 3. End the turn with the Switch_Message

When a note added beside the Skill call says "This session holds about <number> tokens.", the first paragraph of the message, in either form below, carries that sentence as its second sentence, with the number as the note gives it, before the sentence that introduces the `/compact` or `/clear` line. In the Compact_Line form the paragraph reads "This task is done and the next one is a different task. This session holds about <number> tokens. Compact first, so the next task does not re-read this one on every turn:", and the `/clear` form is built the same way. With no note, the first paragraph has no size sentence.

Write this, with the Compact_Line and each Next_Step in place, and nothing after it:

```
This task is done and the next one is a different task. Compact first, so the next task does not re-read this one on every turn:

/compact <Compact_Focus>

Then run:

<Next_Step>

You can skip the compaction and run the next step as it is.
```

For the `/clear` form, write this instead, with each Next_Step in place, and nothing after it:

```
This task is done and the next one is unrelated to it. Start fresh, so the next task carries none of this one; /resume brings this conversation back if you need it:

/clear

Then run:

<Next_Step>

You can skip the clear and run the next step as it is.
```

With several Next_Steps, "Then run:" reads "Then run one of:" and each command has a line of its own.

Run no command and write no file. Ask nothing once a Next_Step is known, and never check afterwards whether the author compacted. When the author's next message is anything other than the Compact_Line, act on it.
