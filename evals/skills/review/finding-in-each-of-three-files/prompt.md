---
description: 'On the shop fixture''s branch shop-lookups, whose uncommitted change adds product_name to shop/handlers.py and the new modules shop/reports.py with average_price and price_range and shop/pricing.py with cheapest_product, each function opening a connection with connect and returning early on an empty result before connection.close(), review launches its arms and the wave-reviewer, keeps one finding at each of the four copies rather than collapsing them, the two in shop/reports.py included, or describing a copy in a sentence of another finding, and its reply lists a finding on each copy''s lines whose message names the connection or its close. Requirements 1.1, 1.5, 4.2, 6.1 and 11.5. Needs the Makefile''s review target, which grants Bash, runs the scaffold and puts the wrappers in bin on the PATH.'
tags: [skill, review]
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Agent]
expected_outcome: 'Claude resolves the range from the merge base of main and HEAD to the working tree, with shop/handlers.py changed and shop/reports.py and shop/pricing.py new, launches six review-arm agents at once, merges their arm blocks without collapsing findings that name each other''s file and line, launches the wave-reviewer once and folds its findings into the list. Its reply lists one finding per line as <severity> <category> <file>:<start_line>-<end_line> <message>, among them a finding on shop/handlers.py within lines 13 to 19, two on shop/reports.py, one within lines 4 to 10 and one within lines 13 to 19, and one on shop/pricing.py within lines 4 to 10, each for the connection opened with connect and left open when the query returns no rows, then the count line. It changes no file and commits nothing.'
---
/ponderly:review
