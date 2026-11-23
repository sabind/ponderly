---
description: When the session already holds another task's work and the author asks for something unrelated, Claude offers once, in a sentence, to switch with /ponderly:switch-task, says it saves re-reading the earlier task on every turn, and starts none of the new work before the answer. Needs the Makefile's eval-skill-switch-task target, which grants Write and Edit but no Bash.
tags: [skill, switch-task]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Write, Edit, Skill]
expected_outcome: "Claude replies with one offer to run switch-task, saying that it saves re-reading the subtract work on every turn, and asks whether to switch. It writes no file and has not started the release-notes draft."
---
Earlier in this session you implemented a spec for subtract(a, b) over several files: you read calc/ops.py, tests/test_ops.py and the spec folder, changed calc/ops.py and tests/test_ops.py, ran `python3 -m unittest` and fixed a failure, and reported back; I accepted it and that task is finished.

New request, unrelated to the calculator: draft the release notes for the next version of the Ponderly plugin, in a file called RELEASE_NOTES.md.
