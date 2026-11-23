# Implementation Plan

## Overview

Waves 0 and 1 were built under the first design, which saved the summary to a file and passed it through two hooks. The Author dropped that design on 19 November 2026; tasks 1.1, 2.1, 2.2 and 3.1 stay ticked as the record of what was built, and wave 2 removes the script and the hook and rewrites the skill to the present design, where the focus travels in the `/compact` line the author pastes. Wave 2 also wires five of the Switching_Skills, writes the eval cases and updates the docs, each in its own files. Wave 3 follows the Author's direction of 19 November after wave 2: the focus leads with the work ahead, a design skill switches once with all its candidates and no question, `bugfix` switches in place of opening the pull request, and `readable-code` and `tighten-tests` are left to the offer; it also fixes a defect found during the run. Wave 4 tunes the skill from a trial in a real session: the offer is made only after substantial work, and the line always tells the summary to drop the finished work. Wave 5 is the trials, wave 6 adds `/clear` for unrelated work after them, and wave 7 is the Author's eval runs. Waves 8 and 9 add the Size_Hook, after the trials showed a switch costs more than it saves in a small session. The Author's part: the paid eval runs and the four real-session trials, which only the Author can do because only the Author can type `/compact`. The full suite at the end of every wave is `make validate`. No eval case is run by a task; task 6.1 names the runs the Author approves by approving this plan.

## Tasks

- [x] 1. Settle how the skill writes the Handoff_File
  - [x] 1.1 Try a shipped script with piped input under an `allowed-tools` rule
    - First design; its result is not used by the present design
    - Result, 19 Nov 2026: ran with no prompt and no denial, headless, default permission mode, Claude Code 2.1.328. Both variables were substituted, in the skill body and in the allowed-tools rule. Form that worked: `printf '<text>\n' | ${CLAUDE_PLUGIN_ROOT}/hooks/save-handoff.sh ${CLAUDE_SESSION_ID}`
    - Correction, 19 Nov 2026: a skill's Bash command does not get `CLAUDE_PLUGIN_ROOT` in its environment; the trial's script did not read it. The form that then worked set it in front of the script, with a second `allowed-tools` rule for that form

- [x] 2. Build the save script and the hook, then remove them; add the Size_Hook
  - [x] 2.1 Write `plugins/claude/ponderly/hooks/save-handoff.sh`
    - First design; built, and removed by task 2.3
  - [x] 2.2 Write `plugins/claude/ponderly/hooks/handoff.sh` and register it in `hooks/hooks.json`
    - First design; built, and removed by task 2.3
  - [x] 2.3 Remove the save script, the hook and its registration
    - Delete `plugins/claude/ponderly/hooks/save-handoff.sh` and `plugins/claude/ponderly/hooks/handoff.sh`, and restore `plugins/claude/ponderly/hooks/hooks.json` to what `git show HEAD:plugins/claude/ponderly/hooks/hooks.json` prints. Neither script was ever committed. Manual check: `git status --short plugins/claude/ponderly/hooks` prints nothing
    - _Requirements: 2.4, 3.4_

  - [x] 2.4 Write `plugins/claude/ponderly/hooks/switch-size.sh` and register it
    - The Size_Hook as the design's component row gives it, in POSIX `sh` and `awk` as `hooks/remind-rules.sh` is written, exit 0 on every path. In `hooks/hooks.json` add a `PreToolUse` entry with matcher `Skill`; leave every existing entry as it is. Ephemeral check: pipe a recorded input for each path against a temporary transcript
    - _Requirements: 6.1, 6.3, 6.4, 6.5_

  - [x] 2.5 Set the limits from the measured request counts and reword the decline
    - In `plugins/claude/ponderly/hooks/switch-size.sh`: the limit is 110000 when the one Next_Step starts `/ponderly:implement-spec`, counted as the `/ponderly:pr` case is counted today, and 150000 otherwise; `/ponderly:pr` no longer has a limit of its own. The deny reason asks for the design's decline: the size, the limit, "not worth it yet", each next step, and the closing line on how to switch anyway; it keeps its two cases for a command and for the author's own request. Update the header. Ephemeral check: a recorded input for each limit at the limit and one below it
    - _Requirements: 6.1, 6.2_

  - [x] 2.6 Read the size a compaction left when no request has run since
    - In `plugins/claude/ponderly/hooks/switch-size.sh`: a transcript line that holds `"subtype":"compact_boundary"` and comes after the last counted request sets the size to the `postTokens` in its `compactMetadata`; a request after that line sets it again from its `usage`, as now. A boundary line with no `postTokens` leaves the size as it was. Update the header. Ephemeral check: a transcript of a request at 182000, then a boundary with `postTokens` 33049, declines printing 33000; the same with one more request at 160000 after the boundary allows
    - _Requirements: 6.1, 6.3_

- [x] 3. Write the `switch-task` skill
  - [x] 3.1 Write `plugins/claude/ponderly/skills/switch-task/SKILL.md`
    - First design; built, and rewritten by task 3.2
  - [x] 3.2 Rewrite `plugins/claude/ponderly/skills/switch-task/SKILL.md` to the present design
    - Frontmatter: keep the description's offer at a Natural_Switch and its length under 1,024 characters, with its first sentences saying what the skill now does; keep `argument-hint`; remove `allowed-tools`. Body: keep step 1 as it is; replace the summary and its save with writing the Compact_Focus in the design's one-line shape, leaving out what a named file holds and keeping the Compact_Line to 600 characters by the design's rule; end the turn with the design's Switch_Message. The skill runs no command and writes no file. Manual check: `make validate` shows no failure about this file's frontmatter or description
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

  - [x] 3.3 Change the `switch-task` skill to the revised focus and several next steps
    - In `plugins/claude/ponderly/skills/switch-task/SKILL.md`: the Compact_Focus takes the design's three-sentence shape, what was finished, what comes next and what it reads, what to keep; the Compact_Line is `/compact ` and the focus; the arguments may hold several Next_Steps, shown under "Then run one of:" with a line each; the description names the six Switching_Skills and says a skill started by hand in a session that holds earlier work gets the same offer once before its first step. Keep the description under 1,024 characters. Manual check: `make validate` passes, and one headless `--plugin-dir` run given two next steps replies with the Switch_Message listing both
    - _Requirements: 1.2, 2.1, 2.2, 2.5, 3.3, 4.9_

  - [x] 3.4 Tune the skill: offer only after Substantial_Work, and always drop the finished work
    - In `plugins/claude/ponderly/skills/switch-task/SKILL.md`: the description offers the skill only when the session holds Substantial_Work, named by its visible signs (a skill run to its end, several files read or changed, sub-agents or long command output, a long exchange), and says a short exchange, such as a question answered, one file read or a small edit, gets no offer; the by-hand case takes the same test. The Compact_Focus takes the design's four-sentence shape, with "Drop the detail of the finished work." as a sentence of its own that is never left out. Keep the description under 1,024 characters and every other part of it. Manual check: `make validate` passes; the launcher makes the trial runs
    - _Requirements: 2.1, 2.5, 4.3, 4.7, 4.9_

  - [x] 3.5 Show `/clear` for unrelated work with nothing to carry, and hold the line to 600 characters
    - In `plugins/claude/ponderly/skills/switch-task/SKILL.md`: when the skill was reached through the offer or by hand, not from a Switching_Skill's hand-off, and the next work is unrelated to what the session holds with nothing to carry, the message takes the design's `/clear` form; when in doubt, or when `carry:` holds anything, it shows the Compact_Line. A Switching_Skill's hand-off always shows the Compact_Line. Step 2 says to count the Compact_Line and shorten it until it is at most 600 characters before writing the message; a trial produced one of 609. The description keeps every part it has and stays under 1,024 characters. Manual check: `make validate` passes; the launcher makes the trial runs
    - _Requirements: 1.6, 2.2_

  - [x] 3.6 State the Session_Size in the Switch_Message
    - In `plugins/claude/ponderly/skills/switch-task/SKILL.md`, step 3: when a note gave the session's size, the first paragraph of either form ends with "This session holds about <size> tokens.", rounded to the nearest thousand; with no note, the message is as now. Change nothing else. Manual check: `make validate` shows no failure about this file; the launcher makes the trial runs
    - _Requirements: 6.3_

- [x] 4. Wire the Switching_Skills
  - [x] 4.1 Change the final step of `strategy`, `hld` and `lld`
    - In each `SKILL.md`, the closing "Hand off" step and the `Hand-offs` line: after saying where the document is, invoke the Skill tool with `skill: ponderly:switch-task` and `args:` the next command; when the skill is missing, name the next command as today. Change those sentences only. Manual check: `make validate` shows no failure about these files
    - _Requirements: 1.1, 1.5, 3.2, 3.3_
  - [x] 4.2 Change the final step of `start-task` and `implement-spec`
    - `start-task`: step 7 and the `done` path of Executor_Route, where `pr` is recommended. `implement-spec`: the two places it hands off to `pr`. Same sentence shape as 4.1; the report skill's Message stays before the switch. Other branches edit these files, so change only the hand-off sentences. Manual check: `make validate` shows no failure about these files
    - _Requirements: 1.1, 1.5, 3.2, 3.3_
  - [x] 4.3 Make `bugfix` switch in place of opening the pull request
    - In `plugins/claude/ponderly/skills/bugfix/SKILL.md`, on the answer that today is `Open it now`, invoke `switch-task` with `/ponderly:pr <ticket>` in place of invoking `pr`, and rename the option `Open the pull request next`; the two stop answers are unchanged. The `Hand-offs` line gains ", through `ponderly:switch-task`"; when the skill is missing, name the command as today. Change the eval case `evals/skills/bugfix/hands-off-to-pr` to grade the `switch-task` call, without running it. `readable-code` and `tighten-tests` are not changed. Manual check: `make validate` passes
    - _Requirements: 1.1, 1.5, 3.2_
  - [x] 4.4 Replace the dollar figures in the effort proposal's cost line
    - In `implement-spec`, `readable-code`, `tighten-tests` and `review`, the cost sentence says only that `high` is expected to cost up to about a quarter more than `medium`; no dollar figure, since `$0` and `$1` in a skill's text are replaced by its arguments. Change that sentence only. Manual check: `make validate` passes, and no `$` followed by a digit is left in those four files outside a code block
    - A defect found during this run, kept in the branch on the Author's word; it cites no requirement of this spec

  - [x] 4.5 Remove the which-to-start question from `strategy`, `hld` and `lld`
    - Task 4.1 added a question asking which candidate to start. Remove it from step 7 and from the `Stops` and `How it asks` lines of each skill: step 7 says where the document is and invokes `switch-task` with every candidate's command, with no question first. Change those lines only. Manual check: `make validate` passes
    - _Requirements: 1.1, 3.2, 3.3_

  - [x] 4.6 Keep the `awk` command in `review` from being rewritten by its arguments
    - In `plugins/claude/ponderly/skills/review/SKILL.md`, the line that gives the two `awk` commands for finding a quote's line number writes `index($0, q)`, and `$0` in a skill's text is replaced by the first argument: a trial on 23 November 2026 with arguments `main...HEAD --json` delivered `index(main...HEAD, q)`. Write both as `index($(0), q)`, which `awk` reads the same way and the same trial showed is left alone. Change those two commands only. Manual check: no `$` followed by a digit is left in the file; `printf 'a\nfind me\n' | awk 'BEGIN {q = ARGV[1]; ARGV[1] = ""} index($(0), q) {print NR}' 'find me'` prints 2; the launcher repeats the trial on the fixed line
    - A defect found during this run, kept in the branch on the Author's word; it cites no requirement of this spec

- [x] 5. Prove and document
  - [x] 5.2 Write four eval cases, without running them
    - `evals/skills/switch-task/writes-the-compact-line`, `evals/skills/switch-task/offers-at-an-unrelated-request`, `evals/skills/switch-task/no-offer-for-a-follow-up` and `evals/skills/lld/switches-at-the-hand-off`, in the shape of the existing cases under `evals/skills/report/`, one grader per criterion. Add a `switch-task` target to the `Makefile` in the shape of the other skill targets, granting no Bash. Run `make validate`; do not run the cases
    - **Property 1: The switch touches nothing**
    - **Property 2: The line can be pasted**
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.4, 4.3, 4.5, 4.6_
  - [x] 5.3 Document the switch
    - `plugins/claude/ponderly/README.md`, the root `README.md` and `llms.txt` list `switch-task`; `docs/reference.md` gains its `###` section, with what happens at a switch and the citation from the design's Overview; the four issue forms under `.github/ISSUE_TEMPLATE/` list `switch-task (skill)` in their component dropdowns; `docs/guides/build-a-feature.md` shows the Switch_Message at the hand-off to `implement-spec`. Check that no shipped file names a terminal or session manager. Manual check: `make validate` shows no failure about the listings
    - _Requirements: 3.4, 5.4_

  - [x] 5.4 Bring the eval cases and the docs to the revised design
    - Eval cases: the graders of `writes-the-compact-line` and `lld/switches-at-the-hand-off` match a line that starts `/compact ` and is at most 600 characters, with no `Keep only:`; the `lld` case expects no question before the switch and several commands under "Then run one of:". Docs: `docs/reference.md`, `README.md`, `plugins/claude/ponderly/README.md` and `llms.txt` name the six Switching_Skills and say `readable-code` and `tighten-tests` are covered by the offer; the reference cites the three published sources from the design beside the Claude Code citation; `docs/guides/build-a-feature.md` shows the revised Switch_Message. Run no eval case. Manual check: `make validate` passes
    - _Requirements: 1.2, 2.1, 3.3, 5.4_

  - [x] 5.5 Bring the eval cases and the docs to the tuned skill
    - Eval cases: `offers-at-an-unrelated-request` describes an earlier task that is Substantial_Work; a new case `evals/skills/switch-task/no-offer-after-a-small-task` gives a short earlier exchange and an unrelated request, and grades that no offer is made and the work starts; `writes-the-compact-line` gains a grader that the line ends with the drop sentence. Docs: the `switch-task` section of `docs/reference.md` says when the offer is made and when not, and shows the four-sentence line; the example in `docs/guides/build-a-feature.md` ends with the drop sentence. Run no eval case. Manual check: `make validate` passes
    - _Requirements: 2.1, 4.3, 4.7_

  - [x] 5.6 Bring the eval cases and the docs to the `/clear` form
    - A new case `evals/skills/switch-task/clears-for-unrelated-work`: the skill is run with an unrelated request after Substantial_Work and no `carry:`, and the graders check that the message shows `/clear` on a line of its own, names `/resume`, shows the request under "Then run:", and holds no `/compact` line. `writes-the-compact-line` keeps grading the Compact_Line, since it gives a `carry:` and a next skill. The `switch-task` section of `docs/reference.md` says when `/clear` is shown and when the Compact_Line is. Run no eval case. Manual check: `make validate` passes
    - _Requirements: 1.6_

  - [x] 5.7 Write `checks/test_switch_size.py`
    - On `checks/reminder_harness.py`, one test per path, each one recorded input against a temporary transcript: below the limit declines with the size in the reason; at the limit allows with the size as context; zero prints nothing; a transcript whose last usage is a side-chain line reads the main line before it; a single `/ponderly:pr` next step uses 200,000; two next steps use 150,000; another skill prints nothing; another tool prints nothing; no transcript prints nothing; input that is not JSON exits 0
    - **Property 3: The hook never blocks anything but a small switch**
    - _Requirements: 6.1, 6.3, 6.4, 6.5_
  - [x] 5.8 Bring the eval cases and the docs to the Size_Hook
    - Eval cases: `lld/switches-at-the-hand-off` and `bugfix/hands-off-to-pr` run in small sandbox sessions, so each now grades the decline: the `switch-task` call is made, the reply names the next command on a line of its own and says compacting is not worth it yet, and holds no `/compact` line; rename a grader whose name no longer fits. The cases that type `/ponderly:switch-task` keep grading the message. Docs: `docs/reference.md` gains a `###` heading for `switch-size.sh` and says in the `switch-task` section when the switch is declined; the four issue forms list `PreToolUse hook`; the plugin README, root README and `llms.txt` say the switch is made only above the limit. Run no eval case. Manual check: `make validate` shows no failure about the listings
    - _Requirements: 6.2, 5.4_

  - [x] 5.9 Bring the hook's tests and the docs to the new limits
    - `checks/test_switch_size.py`: the tests that pin 200000 for a `/ponderly:pr` step become tests that it uses 150000; new tests pin 110000 for a single `/ponderly:implement-spec` step at the limit and one below it, with a `carry:` line after it, and 150000 for two next steps one of which is `implement-spec`; the below-limit test asserts the reason names the limit and how to switch anyway; the byte-order-mark test asserts what is printed as well as the exit code. Docs: `docs/reference.md`, `README.md`, `plugins/claude/ponderly/README.md`, `llms.txt` and the three guides give the limits as 110,000 before `implement-spec` and 150,000 otherwise, and the reference's decline bullet shows the new line. Run no eval case. Manual check: `make validate` passes
    - **Property 3: The hook never blocks anything but a small switch**
    - _Requirements: 6.1, 6.2, 6.5_

  - [x] 5.10 Test the size after a compaction, and say it in the reference
    - `checks/test_switch_size.py`: one test that a large request followed by a boundary line with a small `postTokens` is declined and prints that size; one that a request after the boundary is the size again; one that a boundary line without `postTokens` leaves the earlier request's size. `docs/reference.md`, the `### switch-size.sh` section: one sentence that straight after a compaction the hook reads the size the compaction left. Manual check: `make validate` passes
    - _Requirements: 6.1, 6.3_

- [x] 6. The Author's runs
  - [x] 6.1 The Author runs the eval cases, one sample first
    - First one run of the one case judged most likely to fail, and correct the skill or the case from it; repeat with the next most likely until a sample passes. Then `make eval-skill-switch-task`, 2 runs per case, `make eval-skill-lld EVAL_ARGS="--case switches-at-the-hand-off"`, 2 runs, and `make eval-skill-bugfix EVAL_ARGS="--case hands-off-to-pr"`, 2 runs. Record the scores and the cost here. Approving this plan approves these runs and no others
    - Record, 20 Nov 2026, run at the Author's request by the lead session in tabs of the Author's workspace, Opus 5.5, list prices. Samples at one run: the `lld` case 1.00 ($0.61); the `switch-task` target with the `lld` case, five of six at 1.00 ($1.20), `no-offer-for-a-follow-up` at 0.50 because its prompt named a `subtract` function the fixture lacked, with no offer made; its scaffold now adds the function; the `bugfix` case 1.00 ($0.39). Confirming runs, two per case, every case 1.00: `clears-for-unrelated-work`, `no-offer-after-a-small-task`, `no-offer-for-a-follow-up`, `offers-at-an-unrelated-request`, `writes-the-compact-line` ($1.26), `lld/switches-at-the-hand-off` ($1.23), `bugfix/hands-off-to-pr` ($0.75). Total $5.44
    - Record, 22 Nov 2026, after the Size_Hook: one run of each target. `lld/switches-at-the-hand-off` 1.00 ($0.62) and `bugfix/hands-off-to-pr` 1.00 ($0.37), both now grading the decline; the five `switch-task` cases $0.65, four at 1.00 and `clears-for-unrelated-work` at 0.50, because its command came after a paragraph of text, so the model invoked the skill as a tool and the hook declined it in a 19,000-token session; with the command first it scored 1.00 on two runs ($0.24). Total for the day $1.88
    - Record, 23 Nov 2026, after the limits changed to 110,000 and 150,000 and the decline was reworded: one run each of `lld/switches-at-the-hand-off` 1.00 ($0.61) and `bugfix/hands-off-to-pr` 1.00 ($0.39). The `lld` reply ended with the decline as designed: the size, the limit, both commands, and how to switch anyway
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 4.3, 4.5_
  - [x] 6.2 The Author runs four real-session trials
    - With `claude --plugin-dir plugins/claude/ponderly`, after confirming the session loaded this branch's copy: `lld` to `start-task`, `start-task` to `implement-spec`, `implement-spec` to `pr`, and one switch in the Author's own words. At each, paste the Compact_Line, then the Next_Step. Record for each: the Switch_Message, the first lines of the compacted session, whether the next skill asked for anything the Compact_Focus should have carried, and the cache-read tokens of the last turn before and the first turn after, from the transcript
    - Record, 19 and 20 Nov 2026. Run at the Author's request by the lead session, in tabs of the Author's workspace, on Opus 5.5, Claude Code 2.1.329; the Compact_Line was sent as one line, so a copy by hand is not yet tried. Figures are the total input of the last turn before the compaction and the first turn after, cache read plus cache write, from each session's transcript
    - `lld` to `start-task` (fixture project): one switch, no question, two commands under "Then run one of:"; 84,800 before, 78,000 after; `start-task` found the LLD from the summary and asked for nothing the line should have carried
    - `start-task` to `implement-spec`: the line kept three decisions and that the branch was not yet created; 97,500 before, 97,000 after; `implement-spec` offered to create that branch by name
    - `implement-spec` to `pr`: the report came first, then the Switch_Message; the line was 609 characters, over the limit; 159,200 before, 102,400 after; `pr` started from the summary and stopped for the fixture's missing GitHub remote
    - Natural_Switch, before the tuning of wave 4: offer made after a one-file question; the summary kept the finished task's detail; Claude Code's record gave 69,847 tokens before and 20,165 after, with no turn run after
    - Natural_Switch, after the tuning: no offer after a small task; offer after twelve files read; the line ended with the drop sentence and the summary dropped the finished detail; 155,572 before and 30,240 after by Claude Code's record, with no turn run after
    - What the figures mean: Claude Code restores the text of every skill already used, and recently read files, after a compaction, so a short hand-off saves little and a long run saves about a third. The Author kept `/compact` at the hand-offs on 20 Nov 2026, and `/clear` was added for unrelated work
    - _Requirements: 5.1, 5.2, 5.3_

## Notes

- Other open branches edit `start-task`, `implement-spec`, `lld` and `docs/reference.md`. Change only the sentences a task names; do not reflow or reorder.
- No plugin version change in these tasks; the release is the Author's call after task 6.2.
- A skill names `switch-task` and hands off; it does not restate the Compact_Focus's parts or the Switch_Message.
- The feature ships one hook, the Size_Hook of wave 8, and no other script. Task 5.1 of the first plan, the free checks of the hook, was never started and is gone with it.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["2.1", "2.2", "3.1"] },
    { "id": 2, "tasks": ["2.3", "3.2", "4.1", "4.2", "5.2", "5.3"] },
    { "id": 3, "tasks": ["3.3", "4.3", "4.4", "4.5", "5.4"] },
    { "id": 4, "tasks": ["3.4", "5.5"] },
    { "id": 5, "tasks": ["6.2"] },
    { "id": 6, "tasks": ["3.5", "5.6"] },
    { "id": 7, "tasks": ["6.1"] },
    { "id": 8, "tasks": ["2.4", "3.6", "5.8"] },
    { "id": 9, "tasks": ["5.7"] },
    { "id": 10, "tasks": ["2.5", "4.6", "5.9"] },
    { "id": 11, "tasks": ["2.6", "5.10"] }
  ]
}
```
