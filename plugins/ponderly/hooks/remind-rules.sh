#!/bin/sh
# PostToolUse, SessionStart and SessionEnd hook: reminds each agent of the
# handbook rules for the kind of file it just read or wrote. On PostToolUse for
# Read or Write it sorts the file by its path into a spec, test or code file, and
# prints, as additionalContext, the text of each rule that kind brings which this
# agent has not been sent since the last compaction. It keeps what it sent in
# state/<session_id>, one "<agent> <rule>" line per rule, with <agent> the
# sub-agent's agent_id or main. SessionStart with source compact empties that
# file, and so does SessionEnd. Every SessionStart, whatever its source, and
# every SessionEnd also runs a find that deletes every empty or day-old file
# under state/. Every path exits 0 and nothing blocks the tool call.
#
# The plugin directory's validator only accepts a hook script that writes every
# path in full from CLAUDE_PLUGIN_ROOT, uses no other variable, no command
# substitution and calls no other file in the plugin. So the JSON reader, the
# file sorting and the record all sit in one awk program, which never decodes
# the input and needs no python3, node or jq; the shell only makes state/ and
# runs the sweep, which awk cannot do without system(). The
# checks/test_reminder_*.py files prove it.

[ -d "${CLAUDE_PLUGIN_ROOT:-}/rules" ] || exit 0

mkdir -p "${CLAUDE_PLUGIN_ROOT}/state" 2>/dev/null

# awk exits 1 on SessionStart and SessionEnd so that the sweep runs. A fatal awk
# error, such as an unwritable record or a rules/ with no .md file, exits
# non-zero too and runs the sweep on another event; that extra sweep is harmless,
# since it only deletes empty or day-old records.
awk -v state="${CLAUDE_PLUGIN_ROOT}/state" '
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
  return depth == 1 || (depth == 2 && key[1] == "tool_input" && key[2] == "file_path")
}
function keep(fields, depth, key, value) {
  if (depth == 1) fields[key[1]] = value
  else if (is_kept(depth, key)) fields["tool_input.file_path"] = value
}
function valid_id(s) {
  return s != "" && s !~ /[^A-Za-z0-9_-]/
}
function file_kind(path, cwd,    prefix, rel, name, folders, segments, n, i, ext) {
  sub(/\/$/, "", cwd)
  prefix = cwd "/"
  if (substr(path, 1, length(prefix)) != prefix) return "outside"
  rel = substr(path, length(prefix) + 1)
  if (index(rel, ".ponderly/specs/") == 1) return "spec"
  name = rel
  sub(/.*\//, "", name)
  folders = substr(rel, 1, length(rel) - length(name))
  ext = ""
  if (match(name, /\.[^.]*$/) && RSTART > 1) ext = tolower(substr(name, RSTART + 1))
  if (ext in skipped_ext || name in skipped_name) return "skipped"
  n = split(folders, segments, "/")
  for (i = 1; i <= n; i++) {
    if (tolower(segments[i]) in test_folder) return "test"
  }
  if (name ~ /^test_/ || name ~ /_test\./ || name ~ /\.test\./ || name ~ /\.spec\./ || name ~ /Test\.[^.]*$/ || name ~ /Tests\.[^.]*$/) return "test"
  return "code"
}
function kind_rules(kind) {
  if (kind == "spec") return "communication workflow"
  if (kind == "test") return "tests"
  if (kind == "code") return "code-changes comments"
  return ""
}
function sent_rules(file, agent, sent,    line, parts) {
  while ((getline line < file) > 0) {
    if (split(line, parts, " ") == 2 && parts[1] == agent) sent[parts[2]] = 1
  }
  close(file)
}
function emit(s,    i, n, c) {
  n = length(s)
  for (i = 1; i <= n; i++) {
    c = substr(s, i, 1)
    if (c in esc) c = esc[c]
    printf "%s", c
  }
}
function print_reminder(rules,    names, n, i, j, rule) {
  printf "{\"hookSpecificOutput\": {\"hookEventName\": \"PostToolUse\", \"additionalContext\": \""
  printf "Ponderly rules for the file just read or written. They are the same rules loaded at session start; follow them for this change.\\n\\n"
  n = split(rules, names, " ")
  for (i = 1; i <= n; i++) {
    rule = names[i]
    if (i > 1) printf "\\n"
    for (j = 1; j <= line_count[rule]; j++) {
      emit(rule_line[rule, j])
      printf "\\n"
    }
  }
  printf "\\n\"}}\n"
  fflush()
}
function record(file, agent, rules,    names, n, i) {
  n = split(rules, names, " ")
  for (i = 1; i <= n; i++) print agent " " names[i] >> file
  close(file)
}
function clear(file) {
  printf "" > file
  close(file)
}
function rule_name(path,    name) {
  name = path
  sub(/.*\//, "", name)
  sub(/\.md$/, "", name)
  return name
}
BEGIN {
  for (code = 1; code < 32; code++) esc[sprintf("%c", code)] = sprintf("\\u%04x", code)
  esc["\b"] = "\\b"; esc["\t"] = "\\t"; esc["\n"] = "\\n"; esc["\f"] = "\\f"; esc["\r"] = "\\r"
  esc["\""] = "\\\""; esc["\\"] = "\\\\"
  split("md mdx rst txt adoc csv tsv lock png jpg jpeg gif svg ico webp pdf", list, " ")
  for (i in list) skipped_ext[list[i]] = 1
  split("package-lock.json pnpm-lock.yaml go.sum", list, " ")
  for (i in list) skipped_name[list[i]] = 1
  literal_chars = "-+.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  split("test tests __tests__ spec", list, " ")
  for (i in list) test_folder[list[i]] = 1
}
# macOS awk also splits at newlines when split() is given a one-character
# separator, and a regular expression separator is far slower, so the input
# lines are joined with a space, which JSON reads the same outside a string.
FILENAME == "-" { input = input $0 " "; next }
FNR == 1 { rule = rule_name(FILENAME) }
{ line_count[rule]++; rule_line[rule, line_count[rule]] = $0 }
END {
  if (!read_input(input, fields)) exit 0
  event = fields["hook_event_name"]
  session = fields["session_id"]
  if (event == "SessionStart" || event == "SessionEnd") {
    if (valid_id(session) && (event == "SessionEnd" || fields["source"] == "compact")) clear(state "/" session)
    exit 1
  }
  if (event != "PostToolUse") exit 0
  if (fields["tool_input.file_path"] == "" || fields["cwd"] == "") exit 0
  agent = "main"
  if ("agent_id" in fields) agent = fields["agent_id"]
  if (!valid_id(session) || !valid_id(agent)) exit 0
  file = state "/" session
  n = split(kind_rules(file_kind(fields["tool_input.file_path"], fields["cwd"])), wanted, " ")
  sent_rules(file, agent, sent)
  todo = ""
  for (i = 1; i <= n; i++) {
    if (!(wanted[i] in sent) && (wanted[i] in line_count)) todo = todo " " wanted[i]
  }
  if (todo == "") exit 0
  # Printed and flushed before the record is written: a write to an unwritable
  # record is fatal in awk, and this order makes that cost a repeated rule.
  print_reminder(todo)
  record(file, agent, todo)
  exit 0
}
' - "${CLAUDE_PLUGIN_ROOT}"/rules/*.md ||
  find "${CLAUDE_PLUGIN_ROOT}/state" -type f \( -size 0 -o -mtime +0 \) -exec rm -f {} + 2>/dev/null

exit 0
