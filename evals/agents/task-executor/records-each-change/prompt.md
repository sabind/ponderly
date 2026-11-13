---
description: Launched on a spec task that puts the same edit into two files and a different edit into a third, task-executor returns a Summary whose `files changed` names each changed file on exactly one line, each line with a reason, whether the two files given the same change share a line or not. It returns the status `done`, with `calc/ops.py`, `tests/test_ops.py` and `README.md` each listed once. Needs the Makefile's agent target, which grants Bash, Write and Edit, runs the scaffold, and puts the wrappers in bin on the PATH.
tags: [agent, task-executor]
max_turns: 20
allowed_tools: [Read, Glob, Grep, Agent]
expected_outcome: Claude launches one sub-agent with subagent_type ponderly:task-executor, giving it the mode sentence and the task, and does nothing else itself. The sub-agent adds the header comment to the top of calc/ops.py and tests/test_ops.py, adds the licence line to README.md, writes no test, runs python3 -m unittest, and returns its Summary with the status `done`. Under `files changed` each of the three files appears on exactly one line with a reason, and no file appears twice. Claude's reply is that Summary verbatim.
---
Launch one sub-agent with the Agent tool, `subagent_type` `ponderly:task-executor`, and give it exactly this prompt:

```text
This task is a leaf task from a spec; tests are tasks of their own.

Put the line `# Part of the calc package.` at the top of calc/ops.py and of tests/test_ops.py. In README.md, add the line `Released under the MIT licence.` at the end.
```

Do nothing else yourself: do not read, edit or test anything, do not answer anything the sub-agent asks, and do not launch it again; I cannot answer questions during this run. When the sub-agent returns, reply with its Summary verbatim, the whole of it and nothing else.
