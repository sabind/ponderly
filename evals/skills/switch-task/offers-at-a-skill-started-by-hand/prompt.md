---
description: 'When the author starts start-task by hand in a session that already holds a finished spec run and no switch message was shown since, Claude offers once, in a sentence, to switch tasks, with /ponderly:switch-task or a compact first, and begins none of start-task''s steps before the answer. Needs the Makefile''s eval-skill-switch-task target, which grants Write and Edit but no Bash.'
tags: [skill, switch-task]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Write, Edit, Skill]
expected_outcome: 'Claude offers once to switch tasks, by switch-task or a compact first, and asks whether to switch. It names no route, writes no file and edits none.'
---
/ponderly:start-task add divide(a, b) to calc/ops.py, raising ZeroDivisionError for a zero divisor, with its test

(About this session, not part of the task: earlier in this session you implemented a spec for subtract(a, b) over several files: you read calc/ops.py, tests/test_ops.py and the spec folder, changed calc/ops.py and tests/test_ops.py, ran `python3 -m unittest` and fixed a failure, and reported back; I accepted it and that task is finished. No switch message was shown since.)
