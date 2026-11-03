---
description: 'On the shop fixture''s branch shop-page-size, whose uncommitted changes move README.md to docs/README.md unchanged with git mv and edit shop/handlers.py to raise PAGE_SIZE to 20, review run with --json review.json, a path inside the repository that the scaffold ignores through .git/info/exclude, so the skill accepts it, writes the Final_Object with a read object, one key per lens whose arm returned, and files_unread among the counts, and its reply''s count line has the touched files no arm read entry. Requirement 5.4 and Property 2. The value of files_unread is not graded here. Needs the Makefile''s review target, which grants Bash and Write, runs the scaffold and puts the wrappers in bin on the PATH.'
tags: [skill, review]
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Agent, Write]
expected_outcome: 'Claude resolves the range from the merge base of main and HEAD to the working tree, with docs/README.md, moved from README.md unchanged, and shop/handlers.py the changed files, launches six review-arms, one per lens, and the wave-reviewer once, and, since git ignores the path through .git/info/exclude, accepts it and writes review.json at the workspace root, holding the Final_Object with a read object mapping each lens whose arm returned to the read list of that arm, and a counts object whose files_unread is the number of changed files present at the head that no taken arm''s read list names as read whole. Its reply gives the path written, the count line, which includes touched files no arm read with that number, and any change remark lines. It changes no tracked file and commits nothing.'
---
/ponderly:review --json review.json
