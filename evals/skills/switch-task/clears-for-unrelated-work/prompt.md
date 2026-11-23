---
description: When /ponderly:switch-task is typed with an unrelated request and no `carry:`, its message shows `/clear` on a line of its own in place of the compact line, says the new conversation starts fresh and that `/resume` brings the earlier one back, shows the request under `Then run:`, and holds no `/compact` line; no file is written and the request is not started. The command opens the message and is the whole body, as a typed command, because the switch-size hook declines a Skill-tool call in a small session and a sandbox session is always small; the session holds no earlier work, so nothing in it relates to the request. Needs the Makefile's eval-skill-switch-task target, which grants Write and Edit but no Bash, so a file written shows as a Write or Edit call.
tags: [skill, switch-task, the-switch-touches-nothing]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Write, Edit, Skill]
expected_outcome: "Claude replies with a message that says the next task is unrelated and starts fresh, shows `/clear` on a line of its own, names `/resume` as the way back to this conversation, then shows `Then run:` and the release-notes request on a line of its own. It shows no `/compact` line, writes no file and has not started the release-notes draft. The command comes first and alone because a typed command skips the switch-size hook, which would decline a Skill-tool call in a small sandbox session."
---
/ponderly:switch-task draft the release notes for the next version of the Ponderly plugin in a file called RELEASE_NOTES.md
