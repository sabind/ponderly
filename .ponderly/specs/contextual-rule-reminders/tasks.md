# Implementation Plan

## Overview

The two hook scripts come first, since everything else reads them: `remind-rules.sh` with its File_Kind sorting, record and sweep, and `remind-message.sh` with the fixed Message_Pointer. A shared test harness follows, together with the `hooks.json` wiring and the issue-form entries that `checks/test_issue_forms.py` demands as soon as the new events are registered; then the free checks, one file per concern so that no two tasks of a wave edit the same file. Then come the size checks, the docs, the version and the eval cases; last, the eval run and the scripted headless compaction run, whose results and cost go into the pull request.

Every behaviour is proved by a standard-library `unittest` file under `checks/`, run by `make validate`, one test per path in the style of `checks/test_hook_encoder.py`. Each test runs the script on a temporary plugin folder with a JSON input on stdin. The eval cases under `evals/hook/` show the reminders in a real session with the plugin loaded. Compaction is proved by a free check and by one headless run, not by an eval case, as the design says.

## Tasks

- [x] 1. The file reminder hook
  - [x] 1.1 Write `plugins/ponderly/hooks/remind-rules.sh`
    - POSIX `sh` in Validator_Shape, with a header comment in the voice of the two existing hooks: what the script is, which events run it, why it is one `awk` program, and that the `checks/test_reminder_*.py` files prove it.
    - Shell part, as the design's Components section gives it: `[ -d "${CLAUDE_PLUGIN_ROOT:-}/rules" ] || exit 0`; `mkdir -p "${CLAUDE_PLUGIN_ROOT}/state" 2>/dev/null`; `awk -v state="${CLAUDE_PLUGIN_ROOT}/state" '<program>' - "${CLAUDE_PLUGIN_ROOT}"/rules/*.md`; `find "${CLAUDE_PLUGIN_ROOT}/state" -type f \( -size 0 -o -mtime +0 \) -exec rm -f {} + 2>/dev/null` on `SessionStart` and `SessionEnd` only (have `awk` exit 1 on those two events, so the sweep runs as `awk ... || find ...`, and exit 0 otherwise); then `exit 0`. No `set -e`.
    - `awk` program in named functions, one job each: `read_input`, `valid_id`, `file_kind`, `kind_rules`, `sent_rules`, `print_reminder` (escaping as `load-rules-subagent.sh` does, then `fflush()`), `record` and `clear`, with the File_Kind tests, the order, the opening sentence and the record line format exactly as the design's Data Models section gives them.
    - Prove it with an ephemeral check in the executor's own folder: a Read of a test file, the same Read again, and a `compact` then the Read again, printing each output and the record file; delete the check afterwards.
    - _Requirements: 1.1–1.6, 2.1–2.5, 3.1, 4.1–4.4, 6.1–6.3, 7.1–7.4, 8.1–8.4, 9.1, 9.3_

  - [x] 1.5 Write the shared test harness `checks/reminder_harness.py`
    - Not a test file, so `make check` does not run it as one; the `checks/test_reminder_*.py` files import it. A module docstring; one function that builds a temporary plugin folder with a copy of `rules/` (or given rule texts), one that runs a hook script there with a given JSON on stdin and `CLAUDE_PLUGIN_ROOT` set or unset and returns the exit code, the decoded `additionalContext` or none, and the record file's lines, and one that builds a hook input JSON from its fields.
    - Prove it with an ephemeral check that runs `remind-rules.sh` through it once; delete the check afterwards.
    - _Requirements: 11.1_

  - [x] 1.2 Write the File_Kind tests in `checks/test_reminder_file_kinds.py`, using the harness
    - One test each: an Outside_File brings nothing; a file under `.ponderly/specs/` brings `communication` then `workflow`; `README.md` brings nothing; `tests/data.csv` brings nothing; `tests/helpers.py` brings `tests`; `test_parser.py`, `parser_test.go`, `parser.test.ts`, `parser.spec.js`, `ParserTest.java` and `ParserTests.cs` each bring `tests`; `src/app.py` brings `code-changes` then `comments`; `Dockerfile` and `.gitignore` are code; `NOTES.MD` is skipped; a path with no `tool_input.file_path` brings nothing.
    - _Requirements: 1.2, 1.5, 2.1–2.5_

  - [x] 1.3 Write the record, reset and failure tests in `checks/test_reminder_record.py`, using the harness
    - One test each: a second Read of the same kind brings nothing; a Write after a Read of the same kind brings nothing; a Write of a new test file with no Read brings `tests`; a sub-agent (with `agent_id`) and `main` each get the Rule once; `SessionStart` `compact` brings the Rule back; `SessionStart` `resume` does not; `SessionEnd` leaves no record file for the session; a record file with a modification time two days back is deleted by a `SessionStart`; an invalid `session_id` (`../x`) and an invalid `agent_id` write no record and print nothing; unset `CLAUDE_PLUGIN_ROOT`, a folder with no `rules/`, empty stdin and a JSON array each give exit 0 and no output; a read-only `state/` still gives the File_Reminder, twice for two Reads; the hook finishes within two seconds (bound raised by task 6.3) on a record holding every Rule for 50 Agents.
    - _Requirements: 3.1, 4.1–4.4, 6.1–6.3, 7.1–7.4, 8.1–8.5_

  - [x] 1.4 Write the property tests in `checks/test_reminder_properties.py`, using the harness
    - **Property 1: Each Rule once per Agent between Compactions**: one seeded sequence (`random.Random(1)`) of 200 `PostToolUse` inputs over three Agents and every File_Kind, asserting each Rule appears at most once per Agent and every brought Rule has appeared by the end.
    - **Property 3: The reminder is the rule files, intact**: one test with a rules folder holding quotes, backslashes, every control character from 0x01 to 0x1f and non-ASCII text, and one on the real rules, each asserting the decoded `additionalContext` is the opening sentence, a blank line and the exact rule bytes joined as `load-rules.sh` joins them.
    - **Property 4: A reminder hook never fails a tool call** is covered by the failure tests of 1.3; Property 2 by its `compact` test.
    - **Validates: Requirements 1.1–1.4, 3.1, 4.1, 4.4, 6.1, 6.2**

- [x] 2. The message pointer hook
  - [x] 2.1 Write `plugins/ponderly/hooks/remind-message.sh`
    - POSIX `sh` in Validator_Shape with a header comment: `[ -d "${CLAUDE_PLUGIN_ROOT:-}/rules" ] || exit 0`, one `printf` of `{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "<the design's Message_Pointer text, JSON-escaped>"}}`, then `exit 0`. Reads no stdin.
    - Prove it with an ephemeral check: run it, `json.loads` the output, print the text; delete the check afterwards.
    - _Requirements: 5.1–5.4, 8.1, 9.1, 9.3_

  - [x] 2.2 Write the Message_Pointer tests in `checks/test_reminder_message.py`, using the harness
    - One test each: the decoded pointer is at most 500 characters; it names "Writing to the author" and "Working with the author"; its Pointer_Quote appears verbatim in `rules/communication.md`, with the failure message naming the line; with no `rules/` it prints nothing and exits 0.
    - _Requirements: 5.2, 5.3, 5.5, 8.1_

- [x] 3. Wiring
  - [x] 3.1 Register the hooks and ignore the record folder
    - `plugins/ponderly/hooks/hooks.json`: `remind-rules.sh` as a second hook in the `SessionStart` group; new `PostToolUse` (matcher `Read|Write`) and `SessionEnd` entries for `remind-rules.sh`; a new `UserPromptSubmit` entry for `remind-message.sh`; each command written as the existing ones are, `"\"${CLAUDE_PLUGIN_ROOT}/hooks/<script>\""`.
    - `.gitignore`: add `plugins/ponderly/state/`.
    - Run `make validate` once 4.2, in the same wave, has landed; `checks/test_issue_forms.py` fails until then.
    - _Requirements: 1.1, 3.1, 4.2, 5.1, 7.2, 7.3, 9.2_

  - [x] 3.2 Add the File_Reminder size tests to `checks/test_rules_size.py`
    - One test per File_Kind that brings Rules (spec, test, code): on the real rules, the decoded File_Reminder is under 10,000 characters. Update the module docstring to name the reminders.
    - _Requirements: 1.6_

- [x] 4. Documentation, forms and version
  - [x] 4.1 Update the docs
    - `docs/reference.md` Hooks: the intro says four scripts; a `### remind-rules.sh` and a `### remind-message.sh` section in the shape of the existing two (Event, What it loads), saying which File_Kind brings which Rule, once per agent until a compaction, and the pointer's text.
    - `docs/reference.md` and `plugins/ponderly/README.md` "What the plugin runs and sends": the hooks read the rules and the hook input, write the Reminder_Record under the plugin's `state/` folder, empty it on compaction and session end, delete empty and day-old record files with `find`, and still send nothing anywhere.
    - `evals/README.md` and `.github/CONTRIBUTING.md`: the `hook/<case>/` line names the reminder hooks too; the CONTRIBUTING compatibility list says "the hooks that load and remind the rules".
    - Run `make validate`.
    - _Requirements: 10.1, 10.2_

  - [x] 4.2 Add `PostToolUse hook`, `SessionEnd hook` and `UserPromptSubmit hook` to the `component` dropdown of every issue form under `.github/ISSUE_TEMPLATE/`, in the order `checks/test_issue_forms.py` expects
    - _Requirements: 10.3_

  - [x] 4.3 Bump `plugins/ponderly/.claude-plugin/plugin.json` from 1.6.0 to 1.7.0, and any other file `make validate` says must agree with it
    - _Requirements: 10.4_

- [x] 6. Fixes agreed at the wave 2 hand-back
  - [x] 6.1 Match test folder names in any case
    - In `plugins/ponderly/hooks/remind-rules.sh`, `file_kind` lower-cases each folder segment before testing it against `test`, `tests`, `__tests__` and `spec`, so `Tests/Helpers/Stub.swift` is a Test_File. File name shapes stay case-sensitive.
    - In `docs/reference.md`, the sentence that lists the test folders says they match in any case.
    - Prove it with an ephemeral check: `Tests/Helpers/Stub.swift` and `TEST/x.py` bring `tests`; `src/Testing/x.py` is still code; delete the check afterwards.
    - _Requirements: 2.4_
  - [x] 6.2 Add the any-case folder test to `checks/test_reminder_file_kinds.py`
    - One test: `Tests/Helpers/Stub.swift` brings `tests`.
    - _Requirements: 2.4_
  - [x] 6.3 Add the clear-safety test and loosen the timing test in `checks/test_reminder_record.py`
    - One test: a `SessionEnd` and one a `SessionStart` `compact`, each with `session_id` `../victim`, leave a file at `<plugin>/victim` (made beforehand with content) unchanged.
    - The 50-Agent timing test's bound becomes two seconds.
    - _Requirements: 7.4, 8.5_

- [x] 5. Proof in a real session
  - [x] 5.1 Add `evals/hook/file-reminder-on-read/` and the scaffold flag
    - Makefile per-target block: `eval-hook: CASE_ARGS += --scaffold`.
    - `prompt.md` tagged `hook`, `allowed_tools: [Read]`, with a `scaffold.sh` that writes `tests/test_parser.py` in the workspace; the prompt has Claude read that file, then quote verbatim the first line of any system reminder that followed the tool result and the H1 headings in it.
    - Graders: a regex on the opening sentence "Ponderly rules for the file just read or written."; a regex for the `Tests` heading.
    - _Requirements: 11.2_

  - [x] 5.2 Add `evals/hook/file-reminder-once/`
    - Same scaffold shape, writing `tests/test_parser.py` and `tests/test_lexer.py`; Claude reads both, then quotes each system reminder that followed a tool result. Graders: the opening sentence appears; a `not_contains` regex that fails when it appears twice.
    - _Requirements: 11.2_

  - [x] 5.3 Add `evals/hook/message-pointer/`
    - No tool; Claude quotes verbatim any system reminder that came with the prompt. Grader: a regex on the Pointer_Quote.
    - _Requirements: 5.1, 11.2_

  - [x] 5.4 Run `make eval-hook EVAL_ARGS="--runs 1"`, then confirm at `--runs 2` if every grader passed, and record the table and cost
    - Keep a tally of all spend on the branch, starting from the design's $0.82; stop and ask the Owner before it would pass $15.
    - _Requirements: 11.2, 11.4_

  - [x] 5.5 Run the scripted headless compaction check and record it
    - In a scratch workspace outside the repository: `claude -p --plugin-dir plugins/ponderly` reads a test file; `claude -p --resume <id>` sends `/compact`; a third resumed run reads a second test file and quotes any system reminder after it. Record the three steps, the quoted reminder and the cost for the pull request's Testing section.
    - _Requirements: 4.2, 11.3, 11.4_

## Notes

- Hook scripts stay in Validator_Shape: every path written in full from `${CLAUDE_PLUGIN_ROOT}`, no other shell variable, no command substitution, no call to another plugin file, no `python3`, `node` or `jq`. `awk -v state="${CLAUDE_PLUGIN_ROOT}/state"` is the one way a path reaches `awk`.
- Do not change `load-rules.sh` or `load-rules-subagent.sh`; `checks/test_hook_encoder.py` must pass untouched.
- Tests follow the tests rule: one test per path, one input per test, no `subTest` or loop, except the seeded sequence that Property 1 names.
- Do not edit `evals/rules/**` or `docs/evidence.md`, and do not touch `~/.claude/plugins/` or other worktrees. Keep scratch work in the session's scratchpad. Commit nothing.
- Do not run the with/without comparison or any rule eval.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "2.1"] },
    { "id": 1, "tasks": ["1.5", "3.1", "4.1", "4.2"] },
    { "id": 2, "tasks": ["1.2", "1.3", "1.4", "2.2", "3.2", "4.3", "5.1", "5.2", "5.3"] },
    { "id": 3, "tasks": ["6.1"] },
    { "id": 4, "tasks": ["6.2", "6.3"] },
    { "id": 5, "tasks": ["5.4", "5.5"] }
  ]
}
```
