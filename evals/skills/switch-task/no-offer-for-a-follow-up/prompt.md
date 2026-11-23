---
description: When the author's next request is a follow-up to the task the session holds, Claude does the work and makes no offer to switch tasks or compact. Needs the Makefile's eval-skill-switch-task target, which grants Write and Edit but no Bash.
tags: [skill, switch-task]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Write, Edit, Skill]
expected_outcome: "Claude adds a test of subtract with negative numbers to tests/test_ops.py and says nothing about switching tasks or compacting."
---
Earlier in this session you added subtract(a, b) to calc/ops.py with its tests in tests/test_ops.py, ran `python3 -m unittest`, and reported back.

Follow-up on that same function: add a test to tests/test_ops.py for subtract with negative numbers.
