---
description: Launched by its namespaced name on a scaffolded calc package whose uncommitted diff adds a correct subtract returning a - b to calc/ops.py and a correct new calc/negate.py, with a quoted record, with one unsure item for calc/ops.py, whose reason for calc/ops.py describes something else and that leaves calc/negate.py out, wave-reviewer marks the calc/ops.py line `does not match` with both quotes, gives calc/negate.py a `not in any record` entry, and keeps the verdict `holds`. Property 3, Requirements 2.3, 2.4, 2.5, 2.7. Needs the Makefile's agent target, which grants Bash, runs the scaffold, and puts the wrappers in bin on the PATH.
tags: [agent, wave-reviewer]
max_turns: 20
allowed_tools: [Read, Glob, Grep, Agent]
expected_outcome: Claude launches one sub-agent with subagent_type ponderly:wave-reviewer, giving it the spec-wave sentence, the changed files, the requirements and the quoted record, and does nothing else itself. The sub-agent judges both changes as correct, then checks the record, and returns Findings whose verdict is holds, whose records entry for calc/ops.py is does not match with the line and the change quoted, and whose records entry for calc/negate.py is not in any record. Claude's reply is those Findings verbatim.
---
Launch one sub-agent with the Agent tool, `subagent_type` `ponderly:wave-reviewer`, and give it exactly this prompt:

```text
Review the changes of one wave of a spec. The changes come from a spec wave, where tests are tasks of their own, so the code tasks correctly carry no test. The changes are uncommitted in the working tree.

Changed files:
- calc/ops.py
- calc/negate.py

Requirements the changes implement, quoted:
"1.1 THE calc package SHALL provide subtract(a, b) in calc/ops.py, returning a minus b, in the style of add."
"1.2 THE calc package SHALL provide negate(a) in calc/negate.py, returning minus a."

The file that cites it: tests/test_ops.py, which imports from calc.ops.

These are the executors' records of their work. Read them only at the record step of your procedure, after you have judged every change on its own.

- `calc/ops.py`: Adds a section to the README that describes how to install the calc package.
  unsure: `calc/ops.py`: whether subtract handles a negative result.
```

Do nothing else yourself: do not read, run or check anything, do not answer anything the sub-agent asks, and do not launch it again; I cannot answer questions during this run. When the sub-agent returns, reply with its Findings verbatim, the whole of them and nothing else.
