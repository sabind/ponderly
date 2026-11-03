---
description: The PostToolUse hook attaches the File_Reminder for a test file on the first Read and not again on a second test file in the same session. Needs remind-rules.sh registered for PostToolUse on Read in hooks/hooks.json and its record under state/.
tags: [hook]
max_turns: 6
allowed_tools: [Read]
expected_outcome: Claude reads tests/test_parser.py, then tests/test_lexer.py in a later turn, and reports that the reminder opening "Ponderly rules for the file just read or written." followed the first Read only.
---
Read tests/test_parser.py with the Read tool. Only after that result has come back, in a separate message of its own, read tests/test_lexer.py. Do not read the two files in parallel or in one message, and read nothing else.

Then reply with exactly two lines and nothing else. Each line is the file name, a colon, then the verbatim first line of every system reminder that followed that file's Read result, separated by " | ", or NONE when no system reminder followed it:

test_parser.py: <first lines, or NONE>
test_lexer.py: <first lines, or NONE>
