---
description: 'Launched by its namespaced name with the correctness lens on the calc fixture''s branch calc-strategies, whose two new uncommitted strategy modules calc/add_strategy.py and calc/multiply_strategy.py each call _both_numbers, ignore its result and return {"success": True}, review-arm returns its arm block for the correctness lens with a finding in each module''s file rather than one finding that describes the other copy in a sentence. Requirements 1.1, 1.7 and 11.4. Needs the Makefile''s review-arm target, which grants Bash, runs the scaffold and puts the wrappers in bin on the PATH.'
tags: [agent, review-arm]
max_turns: 20
allowed_tools: [Read, Glob, Grep, Agent]
expected_outcome: 'Claude launches one sub-agent with subagent_type ponderly:review-arm, giving it the shared standard, the correctness lens, the range and the two changed files, and does nothing else itself. The sub-agent reads both new modules at the working tree, sees that each apply calls _both_numbers on line 10 without using its result and returns {"success": True} on line 11 even for an argument that is not a number, so apply("2", "3") reports success with the value "23", and returns an arm block beginning lens: correctness with one correctness finding on calc/add_strategy.py and another on calc/multiply_strategy.py, each naming the file and line of the other. Claude''s reply is that arm block verbatim.'
---
Launch one sub-agent with the Agent tool, `subagent_type` `ponderly:review-arm`, and give it exactly this prompt:

```text
Shared standard, quoted:
"Across every lens, a finding worth reporting is one a competent senior reviewer would expect the author to address before merge: true and verifiable against the code at head, a real concern that would improve the change, and specific enough to act on. A finding not worth reporting is an incorrect or unverifiable claim, a duplicate, a style nit below the project's bar, or advice that would not improve the change or would make it worse. A pre-existing problem in a touched file counts when it is verifiable. A finding sits where a change is needed. When a defect, code or text that does the wrong thing at head and that an edit there would fix, needs its own edit at several places, because each is wrong on its own, such as a stub and the interface it lacks or one mistake copied into several places, write one finding at each place you verified at head, in whatever file it is, touched or not, and one at each copy in the same file. When an edit at either of two places alone would fix the defect, such as a new call into a handler whose guard does not serve that call, or code and a document, configuration or manifest that now disagree, write one finding at the place the pull request changed, or one at each when it changed both, and when it changed neither side's lines, as when it only removed code, on the lines next to the removal. Each such finding names the file and line of the others, or of the other place when there is one finding, and never describes another place's defect as a sentence in place of a finding of its own; a place you suspect but have not verified at head is no finding and goes under unsure. A judgement about the change as a whole, such as that it reformats or reorders files beyond its purpose, mixes two purposes or is too large, names no line an edit would fix: it is not a finding and goes under unsure in one entry beginning `change remark:` that says what it is about, however many files it concerns. A message describes one defect and no aside restating a claim you did not verify: a second defect, even on the same lines, is a finding of its own."

Lens, quoted:
"## correctness

This lens looks for code that does the wrong thing: logic errors, wrong conditions and comparisons, off-by-one bounds, wrong computations, values used before they are set or after they change, state read now that is written later or elsewhere, such as a debounced or deferred save, a snapshot taken before an async step completes, or a callback that lands after the next action, so that the action in between sees stale state, mishandled `None`, empty and boundary inputs, and behaviour that contradicts what the title, the body, a docstring or the surrounding code says it should do. It carries the category `correctness`, where most of a review's real findings sit. A true positive names the input or state that produces the wrong result, traces it through the code at head and says what the code does instead. The commonest wrong finding overlooks an existing guard or rests on a premise the code does not bear out, so the arm checks for a guard, a caller's precondition or a type that already rules the case out before reporting. A false positive asserts a bug the code already prevents, guesses at a caller's behaviour without reading it, or proposes a simplification that changes the behaviour or data shape downstream code reads. Error handling, concurrency, resource use and speed belong to the reliability lens; a swallowed exception that makes a function return a wrong result sits on the boundary, and this lens reports it only when the wrong result is the point. A comment or docstring that is stale while the code is right belongs to the documentation lens."

Range: base main, head the working tree.

Changed files:
- calc/add_strategy.py
- calc/multiply_strategy.py

Pull request title: Add strategy modules for add and multiply
Pull request body: none given
```

Do nothing else yourself: do not read, run or check anything, do not answer anything the sub-agent asks, and do not launch it again; I cannot answer questions during this run. When the sub-agent returns, reply with its arm block verbatim, the whole of it and nothing else.
