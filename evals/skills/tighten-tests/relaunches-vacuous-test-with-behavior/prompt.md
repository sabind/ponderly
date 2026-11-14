---
description: 'The clamp-tests branch adds a tautological test alongside many overlapping tests. The author answers the readability, baseline, coverage, Keep_List and Audit approval questions in advance, keeping the tautology so the mutation check must exercise the Vacuous_Test relaunch.'
tags: [skill, tighten-tests]
max_turns: 40
allowed_tools: [Read, Glob, Grep, Bash, Agent, Skill]
expected_outcome: 'After the Audit is approved, the executor keeps test_clamp_gives_the_same_answer_twice because the author put it on the Keep_List. The mutation check shows it still passes when clamp is replaced with a constant. The skill relaunches that file executor with the exact test name and the required clamp behavior, then the session itself reruns the mutation check and reports whether it now fails. No source file is left changed.'
---
/ponderly:tighten-tests

I am the author and cannot answer questions during this run. Take these answers and do not ask: readability has run; if the baseline suite fails, Go on; use Mutation_Checks alone if there is no coverage tool; the only test on my Keep_List is `test_clamp_gives_the_same_answer_twice`; no other test must stay; I approve the Audit and its Verdicts. Continue through the mutation checks and hand-back.
