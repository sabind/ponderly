#!/bin/sh
# PreToolUse hook, matcher Skill: runs before the session invokes a skill and
# acts only on ponderly:switch-task, not on a bare switch-task. It reads the
# session's size from the transcript at the hook input's transcript_path: the
# input_tokens, cache_read_input_tokens and cache_creation_input_tokens of the
# last line that is an assistant message of the main conversation and holds a
# usage object; a compact_boundary line after that line sets the size to the
# postTokens in its compactMetadata instead, and one without postTokens leaves
# the size as it was. A line of a sub-agent, whether a request or a boundary,
# is skipped. Size zero, which is also an unreadable or missing transcript,
# prints nothing and lets the switch run. Below the limit it prints a deny
# decision whose reason asks the session not to retry and to tell the author
# the size, the limit, that compacting is not worth it yet, each next step, and
# how to switch anyway. At or above the limit it prints an allow
# decision that gives the size as additionalContext. The size is printed
# rounded down to the thousand below. The limit is 150000 tokens, and 110000 when
# tool_input.args, less any text from carry: on and any surrounding
# spaces, tabs and line breaks, holds one command and it starts
# /ponderly:implement-spec. The size is compared with the limit unrounded.
# Every path exits 0, a skill other than the switch and any other tool print
# nothing, and no file is written.
#
# Like remind-rules.sh it uses no command substitution and calls no other file;
# unlike it, it needs no path from CLAUDE_PLUGIN_ROOT. It reads one path
# that does not come from CLAUDE_PLUGIN_ROOT: the transcript's, taken from the
# hook input inside awk, and it writes none. The JSON reader never decodes the
# input and needs no python3, node or jq.

awk '
function read_input(json, fields,    parts, n, i, inside, last, depth, kind, key, want_key, started, in_literal, j, c) {
  n = split(json, parts, "\"")
  for (i = 1; i <= n; i++) {
    if (inside) {
      last = string_end(parts, i, n)
      if (last == 0 || depth == 0) return 0
      if (want_key[depth]) {
        key[depth] = join_string(parts, i, last)
        want_key[depth] = 0
      } else if (is_kept(depth, key)) {
        keep(fields, depth, key, join_string(parts, i, last))
      }
      i = last
      inside = 0
      continue
    }
    in_literal = 0
    for (j = 1; j <= length(parts[i]); j++) {
      c = substr(parts[i], j, 1)
      if (index(" \t\r\n", c)) {
        in_literal = 0
        continue
      }
      if (started && depth == 0) return 0
      if (c == "{" || c == "[") {
        if (depth == 0 && c == "[") return 0
        if (depth > 0) keep(fields, depth, key, "")
        started = 1
        depth++
        kind[depth] = c
        want_key[depth] = (c == "{")
        key[depth] = ""
      } else if (c == "}" || c == "]") {
        if (depth == 0) return 0
        depth--
      } else if (c == ",") {
        want_key[depth] = (kind[depth] == "{")
      } else if (index(literal_chars, c) && depth > 0) {
        if (!in_literal) keep(fields, depth, key, "")
        in_literal = 1
        continue
      } else if (c != ":") {
        return 0
      }
      in_literal = 0
    }
    if (i < n && depth == 0) return 0
    inside = 1
  }
  return started && depth == 0
}
# A string is split wherever it holds an escaped quote. The part at index i
# opens the string; returns the index of the part its closing quote follows,
# or 0 when it is never closed.
function string_end(parts, i, n) {
  while (i < n && odd_backslashes(parts[i])) i++
  if (i < n) return i
  return 0
}
function odd_backslashes(s,    i, count) {
  count = 0
  for (i = length(s); i > 0 && substr(s, i, 1) == "\\"; i--) count++
  return count % 2
}
function join_string(parts, first, last,    i, s) {
  s = parts[first]
  for (i = first + 1; i <= last; i++) s = s "\"" parts[i]
  return s
}
function is_kept(depth, key) {
  return depth == 1 || (depth == 2 && key[1] == "tool_input")
}
function keep(fields, depth, key, value) {
  if (depth == 1) fields[key[1]] = value
  else if (is_kept(depth, key)) fields["tool_input." key[2]] = value
}
function number_after(usage, name,    found) {
  if (!match(usage, "\"" name "\": *[0-9]+")) return 0
  found = substr(usage, RSTART, RLENGTH)
  sub(/.*: */, "", found)
  return found + 0
}
function session_size(path,    line, usage, size) {
  size = 0
  while ((getline line < path) > 0) {
    if (line ~ /"subtype": *"compact_boundary"/) {
      if (line ~ /"isSidechain": *true/) continue
      if (match(line, /"postTokens": *[0-9]+/)) size = number_after(substr(line, RSTART), "postTokens")
      continue
    }
    if (line !~ /"type": *"assistant"/ || line ~ /"isSidechain": *true/) continue
    if (!match(line, /"usage": *\{/)) continue
    usage = substr(line, RSTART)
    size = number_after(usage, "input_tokens") + number_after(usage, "cache_read_input_tokens") + number_after(usage, "cache_creation_input_tokens")
  }
  close(path)
  return size
}
function next_steps(args,    cut) {
  cut = index(args, "carry:")
  if (cut > 0) args = substr(args, 1, cut - 1)
  gsub(/^([ \t]|\\[nrt])+/, "", args)
  gsub(/([ \t]|\\[nrt])+$/, "", args)
  return args
}
function switch_limit(args) {
  args = next_steps(args)
  if (args !~ /\\n/ && (args == "/ponderly:implement-spec" || index(args, "/ponderly:implement-spec ") == 1)) return 110000
  return 150000
}
BEGIN {
  literal_chars = "-+.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
}
# Joined with a space so that macOS awk, which splits at newlines when split() is
# given a one-character separator, reads the input as one line.
{ input = input $0 " " }
END {
  if (!read_input(input, fields)) exit 0
  if (fields["tool_name"] != "Skill" || fields["tool_input.skill"] != "ponderly:switch-task") exit 0
  if (fields["transcript_path"] == "") exit 0
  size = session_size(fields["transcript_path"])
  if (size <= 0) exit 0
  limit = switch_limit(fields["tool_input.args"])
  shown = int(size / 1000) * 1000
  if (size < limit) {
    printf "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\""
    printf "This session holds about %d tokens, under the %d at which compacting pays before this step, so the switch is declined. Do not retry it. ", shown, limit
    printf "Tell the author in your own message, by the kind of next step. The first line is: This session holds about %d tokens, under the %d at which compacting pays before this step, so it is not worth it yet.", shown, limit
    printf " A next step that is a command: write the first line with the word Next: added at its end, a blank line, each command on a line of its own, a blank line, then the closing line on a line of its own, and end your turn there. "
    printf "A next step that is the author\047s request in their own words: do not repeat it as a command; write the first line as it is, with no Next:, a blank line, then the closing line on a line of its own, then start that work. "
    printf "The closing line is this one sentence:\\n\\nTo switch anyway, type /ponderly:switch-task first in your message.\"}}\n"
  } else {
    printf "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"additionalContext\":\""
    printf "This session holds about %d tokens.\"}}\n", shown
  }
  exit 0
}
' -

exit 0
