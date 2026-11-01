---
description: 'On the shop fixture''s branch shop-orders, whose uncommitted shop/orders.py adds order_total with a planted defect, review run with --json review.json, a path inside the repository that the scaffold ignores through .git/info/exclude, so the skill accepts it, writes the Final_Object at the workspace root with pass "final" and the eight counts keys candidates, removed_by_merge, removed_by_review, failed_arms, departures_not_reported, folded, not_anchored and relaunched, launching six arms and the wave-reviewer once. Requirement 3.4 and Property 2. The finding on shop/orders.py is not graded here; not_reported is proved by the arm case. Needs the Makefile''s review target, which grants Bash and Write, runs the scaffold and puts the wrappers in bin on the PATH.'
tags: [skill, review]
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Agent, Write]
expected_outcome: 'Claude resolves the range from the merge base of main and HEAD to the working tree, with shop/orders.py the one changed file, launches six review-arms, one per lens, and the wave-reviewer once, and, since git ignores the path through .git/info/exclude, accepts it and writes review.json at the workspace root, holding the Final_Object with pass "final" and a counts object with the eight keys candidates, removed_by_merge, removed_by_review, failed_arms, departures_not_reported, folded, not_anchored and relaunched, failed_arms and relaunched as lists. Its reply gives the path written, the count line and any change remark lines. It changes no tracked file and commits nothing.'
---
/ponderly:review --json review.json
