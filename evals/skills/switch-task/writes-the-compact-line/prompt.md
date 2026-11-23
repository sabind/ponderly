---
description: Given a next step and what to carry, /ponderly:switch-task ends with the Switch_Message. Its Compact_Line is one line of at most 600 characters that starts with `/compact `, says what was finished, what the next task does and the path it reads, keeps the author's decision, and ends with the sentence that drops the detail of the finished work; the next step sits on a line of its own; no file is written and the next skill is not started. Needs the Makefile's eval-skill-switch-task target, which grants Write and Edit but no Bash, so a file written shows as a Write or Edit call.
tags: [skill, switch-task, the-switch-touches-nothing, the-line-can-be-pasted]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Write, Edit, Skill]
expected_outcome: "Claude replies with a message that says the task is switching, shows one `/compact ...` line of at most 600 characters, with no `Keep only:`, that says what the next task does, names .ponderly/specs/visit-counter/ and keeps the decision to count with calc.ops.add and ends with `Drop the detail of the finished work.`, then shows `Then run:` and `/ponderly:implement-spec .ponderly/specs/visit-counter` on a line of its own. It writes no file and does not start implement-spec."
---
/ponderly:switch-task /ponderly:implement-spec .ponderly/specs/visit-counter carry: we decided to count with calc.ops.add so the arithmetic stays in one place, and to skip a repeated event_id
