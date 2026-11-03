---
description: The PostToolUse hook attaches the File_Reminder for a test file when Claude reads one, and it holds the Tests rule only. Needs the PostToolUse entry in hooks/hooks.json, which runs remind-rules.sh; without it no system reminder follows the Read and Claude replies NO REMINDER.
tags: [hook]
max_turns: 4
allowed_tools: [Read]
expected_outcome: 'Claude reads tests/test_parser.py once, then for the reminder that followed it writes "First line: Ponderly rules for the file just read or written." and "Headings: Tests".'
---
Read the file tests/test_parser.py with the Read tool, once. Then look at every system reminder that followed that tool result in your context, leaving out the file's own contents and anything loaded at session start. For each such reminder, write two lines: "First line: " followed by its first line quoted verbatim, then "Headings: " followed by the exact text of each H1 heading in that reminder, without the leading #, separated by commas. If no system reminder followed the tool result, reply exactly NO REMINDER.
