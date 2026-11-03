#!/bin/sh
# UserPromptSubmit hook: attaches a short pointer to every message the author
# sends, reminding Claude that the communication and collaboration rules,
# loaded at session start by load-rules.sh, are already in its context, and
# quoting the line of the communication rule most often missed. It prints the
# pointer as JSON additionalContext so Claude Code adds it as a system reminder
# rather than showing it as hook output.
#
# The pointer is fixed text here rather than read from rules/communication.md,
# so this hook, which runs on every message, reads no file and no stdin. A free
# check fails when the quoted line no longer appears verbatim in
# rules/communication.md, so a change to that line touches the two together.
# The plugin directory's validator only accepts a hook script that writes every
# path in full from CLAUDE_PLUGIN_ROOT and uses no other variable and no
# command substitution, so the JSON is one printf with its escapes written out.

[ -d "${CLAUDE_PLUGIN_ROOT:-}/rules" ] || exit 0

printf '{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "Ponderly reminder: the rules \\"Writing to the author\\" and \\"Working with the author\\", loaded at session start, are already in your context and apply to your reply. The one most often missed: \\"Lay out a problem, an explanation or a decision as the person it changes will live it.\\""}}\n'

exit 0
