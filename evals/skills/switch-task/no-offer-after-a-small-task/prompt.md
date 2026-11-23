---
description: When the session holds only a short earlier exchange, one question answered from one file, and the author asks for something unrelated, Claude makes no offer to switch tasks or compact and starts the work. Needs the Makefile's eval-skill-switch-task target, which grants Write and Edit but no Bash.
tags: [skill, switch-task]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Write, Edit, Skill]
expected_outcome: "Claude writes fib.txt with the first ten Fibonacci numbers and says nothing about switching tasks or compacting."
---
Earlier in this session I asked what add(a, b) in calc/ops.py returns, and you answered from that one file. Nothing else was read or changed.

New request, unrelated to the calculator: write the first ten Fibonacci numbers, one per line, in a file called fib.txt.
