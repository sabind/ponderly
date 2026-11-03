# The evidence

This page says why the plugin was built, how it is tested, and what the tests
found when Claude Code ran with the plugin and without it. It also says what
has not been measured, and links a real spec the plugin wrote.

## Why it was built

In the author's words:

> I built this to avoid constantly re-prompting, or having to switch between Kiro and Claude. At Amazon I spent time developing tools that wrote code like this before Claude was even available internally. These became industry standard, and I've kept making small refinements to them in areas where I've seen even Kiro fail.

## How it is tested

There are two kinds of test: free checks and evals.

The free checks make no model call, so they cost nothing. Run them with:

```bash
make validate
```

This runs the Python unit tests under `checks/`, which use only the standard
library. They check things a person could get wrong by hand: every skill's and
agent's frontmatter parses, every eval case is well formed, the rules stay
within their size limit, and the hook's JSON encoder works. Then it runs
`claude plugin validate --strict` on the marketplace, the plugin and its
skills. CI runs `make validate` on every pull request.

The evals run Claude on a written task and grade what it did. Each case is a
folder under `evals/` with a prompt and a set of graders. A grader checks one
thing: a pattern in Claude's last message, in a file or in the whole session
transcript; a file that exists or does not; or a tool Claude called or did not
call. A few cases also have a grader that asks a model to judge Claude's
message or a file against a written pass and fail criterion. Every case is a
real model call on your own Claude seat, so evals run by hand and never in CI.
There is one target per component:

```bash
make help                        # list the targets that exist
make eval-skill-<name>           # the cases under evals/skills/<name>/
make eval-rule-<name>            # the cases under evals/rules/<name>/
make eval-agent-<name>           # the cases under evals/agents/<name>/
make eval-hook                   # the cases under evals/hook/
```

A plain target runs each case with the plugin loaded. That answers "does this
skill do its job". It does not answer "would Claude do this anyway". For that,
add `EVAL_ARGS="--ablation with-without"`: each case then also runs in plain
Claude Code without the plugin, and the table gains a column for each arm and
the difference. That doubles the cost, so raise the cost ceiling with
`EVAL_MAX_COST_USD`. [`evals/README.md`](../evals/README.md) has the rest.

The `review` skill is also scored against two public code review benchmarks,
which run by hand in Docker and never in CI:
[ReviewBench](../benchmarks/reviewbench/README.md) and
[Martian's 50 pull requests](../benchmarks/martian/README.md). Each README
says what a run costs and which targets to run.

## Results against Claude Code without the plugin

These tables are an adherence check: they measure whether Claude follows the
plugin's rules when the plugin is loaded. They are not a benchmark, because
plain Claude was never told to behave this way and the graders encode the
rules' own preferences, so the plugin wins by construction. Where plain Claude
already behaves this way, the two arms tie, as four rows below do; the
per-case notes say why the other ties are ties.

The evidence with an outside answer key is the `review` skill scored on
ReviewBench and on Martian's 50 pull requests, whose answer keys are written
outside this repository. The [ReviewBench README](../benchmarks/reviewbench/README.md)
and the [Martian README](../benchmarks/martian/README.md) say how to run them.
This page publishes no score from them yet.

These are the five rule targets, each run with and without the plugin. The
with-plugin arm loads the whole plugin, every rule, skill, agent and hook, not
only the one rule. So each Δ compares the whole plugin with plain Claude Code,
on cases written for that rule. With the plugin, Claude often hands the work to
a plugin skill or agent: it loaded the `report` skill before writing its
message in every with-plugin run of `one-open-decision-at-a-time`, and the
task-executor wrote the code in one run of `no-new-dependency`. So WITH scores
the plugin's whole way of working, not one rule's sentence.

A comparison is clean when plain Claude can pass or fail every scored grader by
what it does, not because a plugin skill is missing, so W/OUT is a fair score
of plain Claude on the same check.

How to read the tables:

- **WITH** is the case's score with the plugin loaded.
- **W/OUT** is its score in plain Claude Code, without the plugin.
- **Δ** is WITH minus W/OUT. A positive Δ means the plugin made Claude pass
  more of the case's graders.
- A score runs from 0 to 1. It is the share of the case's scored graders that
  passed, averaged over three runs. Some graders are left out of the score:
  the workflow section below says which, so its figures can be rebuilt.
- **RUNS** counts the runs of both arms, three each.
- **COST** is the list-price estimate for both arms. **NOTES** names a grader
  that failed in a run with the plugin loaded.

Each table is copied as the command printed it. All five ran on 2026-11-03, on
plugin version 1.6.1 and Claude Code 2.1.317, with three runs per arm. They are
snapshots of one day. A different day or a different model version can move
them.

Some cases have a judge: a grader that asks a model whether Claude's message or
a file meets a written PASS and FAIL bar. Each judge's verdict is three model
votes, and the majority wins. It is a model's reading against that bar, not a
deterministic check. These cases have one:

- `one-open-decision-at-a-time` (collaboration):
  `lays-out-backoff-as-customers-live-it`.
- `lays-out-before-asking` (communication): `lays-out-in-uploader-terms`.
- `names-library-choice-by-what-visitors-see` (communication):
  `lays-out-as-visitors-see-it`.
- `user-effect-before-mechanism` (communication): `subscribers-see-it-first`.
- `one-job-functions` (code-changes): `one-job-per-function`.
- `parser-tests-prove-paths` (tests): `covers-three-awkward-inputs` and
  `names-state-behaviour`.
- `pins-contract-values` (tests): `names-who-relies`.

Judges replaced the pattern graders `uploader-before-the-options` and
`recommends-in-prose` in `lays-out-before-asking`, and
`user-before-mechanism` and `does-not-open-with-mechanism` in
`user-effect-before-mechanism`, which could only stand in for those bars.

### collaboration: 2026-11-03, plugin 1.6.1

Command: `make eval-rule-collaboration EVAL_ARGS="--ablation with-without --runs 3" EVAL_MAX_COST_USD=12`

```
CASE                         WITH  W/OUT Δ      RUNS COST    NOTES
one-open-decision-at-a-time  0.86  0.38  +0.48  6    $0.67   one-question: pattern not found in last_message
short-list-asks-with-tool    1.00  0.94  +0.06  6    $0.48   

2 case(s) · mean Δ +0.27 · 240s · $1.15
```

Every grader in both cases looks at Claude's last message or the files, so
plain Claude could pass each one. Both comparisons are clean.

`one-open-decision-at-a-time` asks Claude to help design a retry for an upload
worker, with three open decisions: the backoff shape, where the attempt count
lives, and what happens after the last failure. Pattern graders check that
Claude says there are three decisions, asks one question, lists fixed and
exponential as options, and lists no option for the second or third decision.
A judge checks that each backoff option is laid out as the customer whose
burst of uploads is throttled lives it, with a recommendation and its reason.
Plain Claude held back the second and third decisions in every run. It said
how many decisions there were in one run of three, asked one question in one,
never listed fixed and exponential as options, and never passed the judge.

`short-list-asks-with-tool` asks Claude to set a log level from three allowed
values without saying which. It passes when Claude asks which one, lists
`debug`, `info` and `warn` on their own lines, does not say it set or chose a
level, and creates no `config.yml`. Plain Claude asked and listed the three
options in every run. In one run of three its message said it had set or chosen
a level, though it created no file.

### communication: 2026-11-03, plugin 1.6.1

Command: `make eval-rule-communication EVAL_ARGS="--ablation with-without --runs 3" EVAL_MAX_COST_USD=12`

```
CASE                                       WITH  W/OUT Δ      RUNS COST    NOTES
check-not-run                              1.00  0.83  +0.17  6    $0.94   
failing-check-first                        1.00  1.00  0.00   6    $0.82   
incidental-failure-first                   1.00  1.00  0.00   6    $0.85   
incidental-not-run-first                   1.00  1.00  0.00   6    $0.95   
lays-out-before-asking                     1.00  0.42  +0.58  6    $0.83   
names-library-choice-by-what-visitors-see  1.00  0.67  +0.33  6    $0.87   
user-effect-before-mechanism               0.78  0.78  0.00   6    $0.88   subscribers-see-it-first: judge votes: FAIL FAIL FAIL

7 case(s) · mean Δ +0.15 · 1164s · $6.16
```

Every grader looks at Claude's message or the files, so plain Claude could pass
each one. Every comparison in this table is clean.

The first four cases check that Claude's final message opens with a failed
test or a test it could not run, before anything else, and does not narrate its
steps. Two of them make the problem incidental to the request, where it is
easiest to bury. Plain Claude scored the same as Claude with the plugin on
three of them. On `check-not-run` it opened with the test not having run in two
runs of three.

`lays-out-before-asking` asks Claude to pick a retry ceiling of 3, 5 or 10
attempts with the author, on a project whose README gives what each ceiling
recovers and how long it makes the queue wait. Three pattern graders check that
3, 5 and 10 each start a line of their own as options. The judge checks that,
before those options, the message says what the uploader lives with under each
ceiling, a dropped file to send again and the wait behind a failing job, and
recommends one with its reason in those terms. Plain Claude passed the judge in
two runs of three, but listed each option on its own line in only one.

`names-library-choice-by-what-visitors-see` asks Claude to help choose between
`requests` and `httpx` for loading a photo gallery's thumbnails, on a project
whose README says what a photographer's client sees while the gallery loads
under each. Two pattern graders check that each library is named near the
start of a list item, a heading or an "Option N" line of its own, one that does
not also name the other library first, and one checks that `gallery/thumbs.py`
is left unchanged. The judge checks that every option is described as what
the client sees on opening the gallery, with what `httpx` costs the project,
and that a recommendation with its reason in those terms comes before the
question. Plain Claude left the file alone in every run, put both libraries on
lines of their own in one run of three, and passed the judge in one.

`user-effect-before-mechanism` asks Claude to run the tests of a package that
builds a weekly email, where `render_subject` cuts the subject line off
mid-word and `test_render_subject_width` fails. Pattern graders check that the
message names the test, `render_subject` or `subject.py`, and narrates nothing.
The judge checks that the message says what subscribers see, a subject cut off
mid-word in their inbox, before it names the test, the function or any file.
The judge passed one run of three in each arm. In most runs, with the plugin
and without, Claude named the test or `render_subject` before saying what
subscribers see. Δ 0.00 here is a real tie: on this case the rule made no
measurable difference.

### code-changes: 2026-11-03, plugin 1.6.1

Command: `make eval-rule-code-changes EVAL_ARGS="--ablation with-without --runs 3" EVAL_MAX_COST_USD=12`

```
CASE                      WITH  W/OUT Δ      RUNS COST    NOTES
no-new-dependency         1.00  1.00  0.00   6    $1.14   
one-job-functions         1.00  0.67  +0.33  6    $1.16   
reads-contributing-guide  0.83  0.50  +0.33  6    $0.71   lists-subtract-in-readme: pattern not found in file README.md
smallest-change           1.00  0.75  +0.25  6    $0.57   
test-with-change          1.00  0.50  +0.50  6    $0.79   

5 case(s) · mean Δ +0.28 · 959s · $4.38
```

The cases run on a small Python project. `no-new-dependency` asks for retry
logic and checks that no retry library is added. `one-job-functions` asks for
a `customer_report` that filters, totals, sorts and formats orders, beside an
existing long `load_orders` it was not asked to change. Pattern graders check
that `customer_report(path)` is added and that `calc/orders.py` is unchanged,
and the judge reads `calc/report.py` and checks that the work is split into
functions that each do one job their name says. `reads-contributing-guide`
asks for a new function and checks that it is also listed in the README, as
the project's contributing guide asks. `smallest-change` asks for a one-line
bug fix and checks that the fix is made, that the nearby typo and unused import
are left alone, and that Claude names the existing test that guards it.
`test-with-change` asks for a new function and checks that a test for it is
added.

Every grader looks at the files or Claude's message, so this is a clean
comparison. Plain Claude also added no dependency, and left `load_orders` alone.
In no run did it split `customer_report` into one-job functions, list the new
function in the README, name the guarding test, or add a test.

### tests: 2026-11-03, plugin 1.6.1

Command: `make eval-rule-tests EVAL_ARGS="--ablation with-without --runs 3" EVAL_MAX_COST_USD=12`

```
CASE                      WITH  W/OUT Δ      RUNS COST    NOTES
parser-tests-prove-paths  1.00  0.40  +0.60  6    $2.15   
pins-contract-values      1.00  0.67  +0.33  6    $1.56   

2 case(s) · mean Δ +0.47 · 880s · $3.71
```

Both cases ask for tests on a small Python project.

`parser-tests-prove-paths` asks for a `parse_quantity(text)` parser that
accepts a whole number from 1 to 999, with its tests. Pattern graders check
that the function is added, that the tests use 0 or a negative number and 1000,
and that they use no loop, `subTest` or `parametrize`. Two judges read the
test file. One checks that the tests pass at least three kinds of awkward
input, such as emoji, a non-Latin script or a byte-order mark. The other checks
that every test's name is a sentence stating the one behaviour it proves.
Plain Claude added the function and used the boundary values in every run. In
no run did it avoid a loop or table, pass three kinds of awkward input, or name
every test as a behaviour.

`pins-contract-values` asks for tests of an event builder whose module says
the billing service relies on the type "order.placed" and on `order_id` and
`total_cents`, and that nothing reads `emitted_by`. An existing test for
another builder asserts the whole event, `emitted_by` included. Pattern
graders check that the tests pin the type as the literal "order.placed" and
never mention the `ORDER_PLACED` constant, `emitted_by` or the `EMITTER`
constant. The judge checks that the type test's name says what relies on the
value, such as the billing service, and that some test checks `order_id` and
`total_cents`. Plain Claude pinned the literal in every run, left out the
constant and `emitted_by` in two runs of three each, and passed the judge in
one.

Every grader looks at the files, so plain Claude could pass each one, and both
comparisons are clean. The arms differ in who wrote the tests. With the plugin,
the request went to `start-task` in five of the six runs and to the
task-executor directly in the sixth, and in all six the task-executor wrote the
tests. Without the plugin, the session wrote them itself.

### workflow: 2026-11-03, plugin 1.6.1

Command: `make eval-rule-workflow EVAL_ARGS="--ablation with-without --runs 3" EVAL_MAX_COST_USD=12`

```
CASE                           WITH  W/OUT Δ      RUNS COST    NOTES
bug-routes-to-bugfix           1.00  0.73  +0.27  6    $0.93   
closed-spec-is-a-record        1.00  0.50  +0.50  6    $1.01   
feature-routes-to-start-task   1.00  0.00  +1.00  6    $1.55   
pr-routes-to-pr-skill          1.00  1.00  0.00   6    $0.91   
small-change-skips-spec        1.00  1.00  0.00   6    $0.83   
spec-routes-to-implement-spec  1.00  0.00  +1.00  6    $1.06   

6 case(s) · mean Δ +0.46 · 1112s · $6.29
```

These cases check that a request reaches the right skill: a bug goes to
`bugfix`, a feature to `start-task`, a pull request to `pr`, work on a spec to
`implement-spec`, a typo fix to no skill, and a request near a merged spec not
to `implement-spec`. This is where the skill descriptions show, since Claude
picks a skill by its description.

This table is not a clean comparison, and the Δ overstates what the rule does
on its own. Most of these graders check for a call to one of the plugin's
skills, and without the plugin those skills do not exist. A grader that checks
for a skill call is scored in both arms when it is the case's only grader. When
the case has other graders it is left out of the score in both arms, so the
WITH score does not say whether the skill was called either. Case by case:

- `feature-routes-to-start-task` and `spec-routes-to-implement-spec` have one
  grader each, a call to the plugin's skill. Plain Claude cannot make that
  call, so W/OUT 0.00 measures that the skill exists, not how Claude behaves.
- `pr-routes-to-pr-skill`: the call to the `pr` skill is left out of the
  score in both arms. Both scores come from the one other grader, which checks
  that no shell permission error appears in the transcript. Routing is not
  compared, and WITH 1.00 does not include whether `pr` was called.
- `closed-spec-is-a-record`: the call to `start-task` is left out of the score
  in both arms. Of the two graders scored, one checks that `implement-spec` is
  not called, which plain Claude passes because the skill does not exist. The
  other looks for route names that only `start-task` writes, which plain Claude
  never wrote. The W/OUT 0.50 is not a measure of the rule.
- `small-change-skips-spec` checks that no skill is called. Plain Claude
  passes because it has no skills to call, so W/OUT 1.00 compares nothing.
- `bug-routes-to-bugfix`: the call to `bugfix` is left out of the score in
  both arms. Five graders are scored. Plain Claude passed 11 of their 15
  checks over three runs, which is the W/OUT 0.73:
  - `no-fix-claimed`: Claude's last message claims no fix. Plain Claude
    passed in every run.
  - `not-start-task`: Claude does not call `start-task`. Plain Claude passed
    trivially, because the skill does not exist without the plugin.
  - `skill-loads`: no shell permission error appears in the transcript. Plain
    Claude passed in every run.
  - `says-reproduce-first`: Claude's last message says it will reproduce the
    bug. Plain Claude failed in every run.
  - `states-symptom`: the word "symptom" appears anywhere in the session
    transcript, not only in Claude's message. Plain Claude passed in two runs
    of three, in its own words. With the plugin, the `bugfix` skill's own
    text, which uses the word, is in the transcript, so the grader passes in
    that arm whatever Claude writes.

  Only `no-fix-claimed` and `says-reproduce-first` are fair comparisons of
  how Claude behaves.

## Not measured

The components below have no result against Claude Code without the plugin.
This page makes no comparison for them. Each has eval cases that run with the
plugin loaded, which check that the component does its job, except the
`comments` rule, which has none.

The skills: `bugfix`, `hld`, `implement-spec`, `lld`, `pr`, `readable-code`,
`report`, `review`, `start-task`, `strategy` and `tighten-tests`. Their targets
are `make eval-skill-<name>`. Without the plugin the skill does not exist, and
their graders check for what the skill does and writes.

The agents: `document-reviewer`, `review-arm`, `task-executor` and
`wave-reviewer`. Their targets are `make eval-agent-<name>`. Without the plugin
the agent does not exist, and their graders check for what the agent does and
reports.

The hooks: the two cases under `evals/hook/`, run by `make eval-hook`. They
check that the plugin's hooks load the rules into a session and into a
sub-agent. Without the plugin there is no hook and no rule, and their graders
check for the rules' headings.

The `comments` rule. It has no eval cases yet, with the plugin or without.

## A real example

[`.ponderly/specs/design-skills/`](../.ponderly/specs/design-skills/)
is the spec for the `strategy`, `hld` and `lld` skills and the
`document-reviewer` agent, merged in pull request #53. `start-task` wrote its
requirements, design and tasks, and `implement-spec` built it task by task.
It is a record of that work; the plugin's current behaviour is in its code and
the [Reference](reference.md).
