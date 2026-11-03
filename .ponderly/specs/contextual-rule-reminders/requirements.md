# Requirements Document

## Introduction

Ponderly's six rules reach a session once, at its start, through the `SessionStart` hook, and reach each sub-agent once through the `SubagentStart` hook. In a long session that copy is buried under everything that follows, and agents drift from it; the customer-language part of the communication rule is the one they slip on most. A plugin cannot ship `.claude/rules/` or a `CLAUDE.md` that Claude Code loads, so hooks are the supported route. This task adds Rule_Reminders: when Claude reads or writes a file, the rules that govern that kind of file are attached right after the tool result, just before Claude writes its change, the way a native `paths:` rule loads when Claude touches a matching file; and every message the Operator sends carries a short Message_Pointer to the communication and collaboration rules, just before Claude replies. Each rule is attached once per Agent between Compactions. It serves the Operator, whose agents keep to the rules late in a long session, and the Owner, who keeps the plugin inside the directory's validator shape and its "sends nothing" promise.

Decided by the Owner before this spec, and taken as given: `PostToolUse` on `Read` is the main trigger, with `additionalContext` as the channel, since Claude Code requires a Read before an Edit; `PostToolUse` on `Write` is the fallback for a new file that had no Read; there is no `PreToolUse` hook, and a deny-once `PreToolUse` on `Write` is held in reserve, unbuilt, for evals that show first new test files breaking the rule; each rule attaches once per session and again after Compaction, with the reset hung off `SessionStart`'s `compact` source; and the two existing hooks keep loading the full rules, with reminders added on top.

Decided with the Owner while writing this spec: the Message_Pointer on every message, through `UserPromptSubmit`; the communication rule attaches with the workflow rule on Spec_Files; files are sorted with everything counting as a Code_File except a short Skipped_File list; the Reminder_Record lives in the plugin's own folder; sub-agents get Rule_Reminders with a record of their own; and a File_Reminder carries the whole rule, not a pointer.

## Glossary

- **Operator**: The person working in a Claude Code session with the plugin installed, who reads Claude's replies and approves its work.
- **Owner**: The maintainer of the plugin, accountable for what its hooks run, write and send, and for its directory listing.
- **Rule**: One file under `plugins/ponderly/rules/`, named by its file name without `.md`: `code-changes`, `collaboration`, `comments`, `communication`, `tests` or `workflow`.
- **Session_Rules**: The full text of every Rule, as `load-rules.sh` prints it on `SessionStart` and `load-rules-subagent.sh` gives it on `SubagentStart`.
- **Agent**: The main conversation of a session, or one sub-agent within it, told apart by the hook input's `agent_id`, which only a sub-agent's tool calls carry.
- **Rule_Reminder**: Text a hook attaches to an Agent's context through `hookSpecificOutput.additionalContext`, carrying a File_Reminder or a Message_Pointer.
- **File_Reminder**: A Rule_Reminder attached after a `Read` or `Write` tool call, holding the full text of each Rule that the File_Kind of the tool's file brings and that the Agent has not yet been sent since the last Compaction.
- **Message_Pointer**: A Rule_Reminder attached to each message the Operator sends, naming the communication and collaboration Rules, saying they are already in context, and quoting one line from the communication Rule verbatim.
- **Pointer_Quote**: The line the Message_Pointer quotes: "Lay out a problem, an explanation or a decision as the person it changes will live it."
- **Working_Directory**: The `cwd` the hook input names.
- **File_Kind**: The class a file falls in for a File_Reminder: Outside_File, Spec_File, Skipped_File, Test_File or Code_File, decided in that order.
- **Spec_File**: A file under `.ponderly/specs/` in the Working_Directory; it brings `workflow` and `communication`.
- **Test_File**: A file in the Working_Directory, neither a Spec_File nor a Skipped_File, whose path relative to the Working_Directory has a folder named, in any case, `test`, `tests`, `__tests__` or `spec`, or whose name starts `test_`, holds `_test.`, `.test.` or `.spec.`, or ends in `Test` or `Tests` before its last extension; it brings `tests`.
- **Skipped_File**: A file in the Working_Directory that is a prose, data, lock or binary file by its name: the extensions `.md`, `.mdx`, `.rst`, `.txt`, `.adoc`, `.csv`, `.tsv`, `.lock`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico`, `.webp` and `.pdf`, and the lockfiles `package-lock.json`, `pnpm-lock.yaml` and `go.sum`; it brings no Rule.
- **Outside_File**: A file whose absolute path is not inside the Working_Directory; it brings no Rule.
- **Code_File**: Any other file in the Working_Directory, whatever its language, including build files and configuration; it brings `code-changes` and `comments`.
- **Compaction**: Claude Code summarising an Agent's earlier context, after which `SessionStart` fires with `source` `compact`.
- **Reminder_Record**: The file `${CLAUDE_PLUGIN_ROOT}/state/<session_id>`, one per session, holding one line per Agent and Rule already sent to that Agent since the session's last Compaction.
- **Validator_Shape**: The form of a hook script the plugin directory's validator follows: every path written in full from `${CLAUDE_PLUGIN_ROOT}`, no other shell variable, no command substitution, no package launcher, and no call to another file in the plugin.

## Requirements

### Requirement 1: A Read brings the Rules for that kind of file

**User Story:** As an Operator, I want the Rule that governs a file to appear right after Claude reads it, so that Claude writes its change with that Rule in front of it rather than buried at the session's start.

#### Acceptance Criteria

1. WHEN an Agent's `Read` tool call completes on a file, THE System SHALL attach a File_Reminder holding the full text of each Rule the file's File_Kind brings that the Agent has not been sent since the last Compaction.
2. WHEN a File_Reminder holds more than one Rule, THE System SHALL give the Rules in Rule name order, each under its own heading as the Rule file writes it.
3. THE System SHALL open each File_Reminder with one sentence saying the Rules below apply to the file just read and are the same Rules loaded at session start.
4. IF every Rule a file's File_Kind brings has already been sent to the Agent since the last Compaction, THEN THE System SHALL attach nothing.
5. IF the file's File_Kind is Skipped_File or Outside_File, THEN THE System SHALL attach nothing.
6. THE System SHALL keep each File_Reminder under 10,000 characters, counted as decoded UTF-8 characters.

### Requirement 2: Files are sorted by kind

**User Story:** As an Operator, I want each file sorted into the right File_Kind, including files in languages the plugin never listed, so that the code Rules are not used up early on a README and arrive when real code is opened.

#### Acceptance Criteria

1. THE System SHALL decide a file's File_Kind from its absolute path and the Working_Directory alone, without reading the file.
2. THE System SHALL test the File_Kinds in the order Outside_File, Spec_File, Skipped_File, Test_File, Code_File, and give the file the first that fits, so that a fixture such as `tests/data.csv` brings nothing.
3. WHEN a file in the Working_Directory fits no other File_Kind, THE System SHALL treat it as a Code_File, whatever its extension or lack of one.
4. THE System SHALL match folder names and extensions in any case, and file name shapes case-sensitively.
5. IF the hook input carries no `tool_input.file_path` or no `cwd`, THEN THE System SHALL attach nothing.

### Requirement 3: A Write brings the Rules when no Read came first

**User Story:** As an Operator, I want a new file Claude writes without reading to bring its Rules too, so that a first new test file is still written beside the tests Rule.

#### Acceptance Criteria

1. WHEN an Agent's `Write` tool call completes on a file, THE System SHALL attach a File_Reminder by the same File_Kind, Rule and once-only behaviour as for a `Read`, so that a `Write` after a `Read` of the same kind of file brings nothing.

### Requirement 4: Each Rule comes once per Agent until a Compaction

**User Story:** As an Operator, I want each Rule to come back only when its last copy has been summarised away, so that reminders do not fill the context.

#### Acceptance Criteria

1. WHEN a File_Reminder is attached, THE System SHALL record each Rule it holds in that Agent's Reminder_Record.
2. WHEN `SessionStart` fires with `source` `compact`, THE System SHALL empty every Reminder_Record of that session, so that the next matching `Read` or `Write` brings each Rule again.
3. WHEN `SessionStart` fires with `source` `startup`, `resume`, `clear` or `fork`, THE System SHALL leave that session's Reminder_Record as it is.
4. THE System SHALL send each Rule to an Agent at most once between two Compactions, except that tool calls Claude runs in parallel may each attach the same Rule once.

### Requirement 5: Every message carries the Message_Pointer

**User Story:** As an Operator, I want every message I send to carry a short reminder of the communication and collaboration Rules, so that Claude's reply to me, where the customer-language slip happens, is written just after it.

#### Acceptance Criteria

1. WHEN the Operator sends a message, THE System SHALL attach the Message_Pointer to it through `UserPromptSubmit`.
2. THE Message_Pointer SHALL name the communication and collaboration Rules by their headings, "Writing to the author" and "Working with the author", say they are already in context, and quote the Pointer_Quote verbatim.
3. THE Message_Pointer SHALL be at most 500 characters.
4. THE System SHALL attach the Message_Pointer on every message, whatever the Reminder_Record holds, and SHALL not record it there.
5. IF the Pointer_Quote no longer appears verbatim in the communication Rule, THEN the plugin's free checks SHALL fail and name the line.

### Requirement 6: Sub-agents get Rule_Reminders of their own

**User Story:** As an Operator, I want a sub-agent such as the task executor to get File_Reminders as the main conversation does, so that a long executor task keeps to the tests and code Rules too.

#### Acceptance Criteria

1. WHEN a `Read` or `Write` tool call inside a sub-agent completes, THE System SHALL attach File_Reminders to that sub-agent by the same behaviour as for the main conversation.
2. THE System SHALL keep each Agent's entries in the Reminder_Record apart, keyed by the hook input's `agent_id` for a sub-agent and by `main` for the main conversation, so that a Rule sent to one Agent does not count as sent to another.
3. THE System SHALL behave the same whether a sub-agent's hook input carries its parent's `session_id` or one of its own.

### Requirement 7: The Reminder_Record stays small and is cleaned up

**User Story:** As an Owner, I want the Reminder_Record kept inside the plugin's own folder and removed when it is no longer needed, so that the plugin writes nowhere else on the Operator's machine and leaves little behind.

#### Acceptance Criteria

1. THE System SHALL write the Reminder_Record only under `${CLAUDE_PLUGIN_ROOT}/state/`, in one file per `session_id`.
2. WHEN `SessionEnd` fires, THE System SHALL empty that session's Reminder_Record and delete every empty Reminder_Record under `${CLAUDE_PLUGIN_ROOT}/state/`.
3. WHEN `SessionStart` fires with `source` `startup`, THE System SHALL delete every Reminder_Record under `${CLAUDE_PLUGIN_ROOT}/state/` last changed more than one day earlier.
4. IF a `session_id` or `agent_id` holds any character other than an ASCII letter, a digit, `-` or `_`, or is empty, THEN THE System SHALL attach no File_Reminder and write, read and delete nothing for it.

### Requirement 8: A reminder never gets in the way

**User Story:** As an Operator, I want a failing reminder hook to cost me nothing but the reminder, so that no Read, Write or message of mine is blocked or slowed by it.

#### Acceptance Criteria

1. IF `CLAUDE_PLUGIN_ROOT` is unset or names a folder with no `rules/`, THEN THE System SHALL exit 0 with no output from every reminder hook.
2. IF the hook input is not the JSON the event documents, THEN THE System SHALL exit 0 with no output.
3. IF the Reminder_Record cannot be read or written, THEN THE System SHALL still attach the File_Reminder, so that a Rule repeats rather than goes missing.
4. THE System SHALL never block or deny a tool call or a message.
5. THE System SHALL finish each reminder hook within two seconds on a session whose Reminder_Record holds every Rule for 50 Agents.

### Requirement 9: The hooks keep the plugin's shape

**User Story:** As an Owner, I want the new hook scripts to keep the shape the existing ones have, so that the directory listing gains no hold and the plugin still needs no runtime beyond `sh` and `awk`.

#### Acceptance Criteria

1. THE System SHALL write every new hook script in Validator_Shape, as POSIX `sh` and `awk`, with no `python3`, `node` or `jq`.
2. THE System SHALL leave the output of `load-rules.sh` and `load-rules-subagent.sh` unchanged, byte for byte, for the same rules folder.
3. THE System SHALL send nothing over the network from any hook.

### Requirement 10: The reference, the forms and the version say what changed

**User Story:** As an Owner, I want the plugin's reference, issue forms and version to describe the new hooks, so that users and the directory reviewer know what the plugin now runs and writes.

#### Acceptance Criteria

1. THE System SHALL describe each new hook in the Hooks section of `docs/reference.md`, with its event, its trigger and what it attaches.
2. THE System SHALL say in the "What the plugin runs and sends" section of `docs/reference.md` that the hooks write the Reminder_Record under `${CLAUDE_PLUGIN_ROOT}/state/` and delete it as Requirement 7 says, and still send nothing anywhere.
3. THE System SHALL add each new hook to the `component` dropdown of every issue form.
4. THE System SHALL raise the plugin's minor version.

### Requirement 11: The behaviour is proved

**User Story:** As an Owner, I want each path of the new hooks proved by a free check and the reminders shown working in a real session, so that a later change that breaks them fails before it ships.

#### Acceptance Criteria

1. THE System SHALL add free checks under `checks/`, run by `make validate`, with one test per File_Kind, per once-only and reset path, per cleanup path and per failure case of Requirements 7.4 and 8.
2. THE System SHALL add eval cases under `evals/hook/`, tagged `hook`, that show a File_Reminder attaches on a `Read` of a matching file and does not repeat in the same session.
3. WHERE a Compaction can be staged in an eval case, THE System SHALL add an eval case under `evals/hook/` that shows a File_Reminder attaches again after it.
4. IF the eval spend on this branch would pass $15, THEN THE System SHALL stop and ask the Owner before running more.
