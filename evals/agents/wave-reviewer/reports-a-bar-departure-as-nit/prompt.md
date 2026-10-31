---
description: Launched by its namespaced name with the review skill's repository-bar sentence, on a scaffolded calc package whose committed modules annotate every parameter and return and whose uncommitted diff adds calc/stats.py with a correct mean and no annotations and tests/test_stats.py with its test, wave-reviewer reports the missing annotations as a nit, since the change departs from the code around it at no concrete cost, and reports nothing at should-fix or blocker. Requirements 1.3, 4.3 and 4.5 of the review-skips-no-cost-departures spec. Needs the Makefile's agent target, which grants Bash, runs the scaffold, and puts the wrappers in bin on the PATH.
tags: [agent, wave-reviewer]
max_turns: 20
allowed_tools: [Read, Glob, Grep, Agent]
expected_outcome: Claude launches one sub-agent with subagent_type ponderly:wave-reviewer, giving it the range, the repository-bar sentence and the requirement, and does nothing else itself. The sub-agent runs git status and git diff, reads the new calc/stats.py, its test in tests/test_stats.py and the code around them, sees that calc/ops.py and calc/compare.py annotate every parameter and return while mean annotates none, and returns Findings with the missing annotations as a nit and no finding at should-fix or blocker, since mean is correct and comes with its test. Claude's reply is those Findings verbatim.
---
Launch one sub-agent with the Agent tool, `subagent_type` `ponderly:wave-reviewer`, and give it exactly this prompt:

```text
Review the changes from main to the working tree. These changes are a pull request reviewed for the review skill: judge style, structure, comments and tests against the repository's own bar, what its CLAUDE.md, AGENTS.md, .claude/rules/ files and contributing guide say and the code around the change already does, and list a team-rule departure with no concrete cost in this change under unsure, not as a finding, unless it also departs from that bar.

Changed files:
- calc/stats.py
- tests/test_stats.py

Requirement the changes implement, quoted from the pull request:
"1.1 THE calc package SHALL provide mean(values) in calc/stats.py, returning the arithmetic mean of a non-empty list of numbers, so that mean([1, 2]) is 1.5."
```

Do nothing else yourself: do not read, run or check anything, do not answer anything the sub-agent asks, and do not launch it again; I cannot answer questions during this run. When the sub-agent returns, reply with its Findings verbatim, the whole of them and nothing else.
