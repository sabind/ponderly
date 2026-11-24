---
description: 'When the author starts start-task by hand in a session that holds only a short earlier exchange, one question answered from one file, Claude makes no offer to switch tasks or compact and begins start-task''s first step, the route statement. Needs the Makefile''s eval-skill-switch-task target, which grants Write and Edit but no Bash.'
tags: [skill, switch-task]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Write, Edit, Skill]
expected_outcome: 'Claude begins start-task and names a route, and says nothing about switching tasks or compacting.'
---
/ponderly:start-task add divide(a, b) to calc/ops.py, raising ZeroDivisionError for a zero divisor, with its test

(About this session, not part of the task: earlier in this session I asked what add(a, b) in calc/ops.py returns, and you answered from that one file. Nothing else was read or changed.)
