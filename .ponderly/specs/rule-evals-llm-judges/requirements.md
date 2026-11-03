# Requirements Document

## Introduction

Ponderly's rule evals are the evidence an article about the plugin will quote, so they have to measure the behaviour the rules ask for, on the rules as they are today. The communication rule asks that a problem or decision be laid out as the person it changes will live it, but every grader of that behaviour is a regex that checks a proxy, such as a word appearing before a list. This work gives those cases a model judge with a written pass bar, adds one case where the natural phrasing of a choice is a library name, reruns every rule eval with and without the plugin on the current rules, and replaces the dated tables in `docs/evidence.md` with the new ones, saying honestly which comparisons are clean. The readers are Dan, writing the article, and anyone who reads the evidence page.

## Glossary

- **Judge_Grader**: An eval grader of type `llm` whose body states what the graded text is, a PASS bar and a FAIL bar.
- **Proxy_Grader**: A `regex` grader that checks a surface feature standing in for a behaviour, such as one word appearing before another, rather than the behaviour itself.
- **Reader_Terms**: Phrasing a problem, an explanation or a choice as what the person it changes sees, waits through or takes on, rather than as its mechanism, as `plugins/ponderly/rules/communication.md` says.
- **Rule_Target**: One of `make eval-rule-code-changes`, `eval-rule-collaboration`, `eval-rule-communication`, `eval-rule-tests` and `eval-rule-workflow`.
- **Ablation_Run**: One invocation of a Rule_Target, or of one case of it, with `--ablation with-without --runs 3`, so each case runs three times with the plugin and three times without.
- **Results_Table**: The table an Ablation_Run prints, with the WITH, W/OUT, Δ, RUNS, COST and NOTES columns.
- **Eval_Spend**: The sum of the COST figures that every Ablation_Run in this work printed.
- **Evidence_Page**: `docs/evidence.md`.
- **Routing_Grader**: A `tool_used` grader that checks for a call to one of the plugin's own skills, which cannot pass without the plugin.
- **System**: The eval cases, the Evidence_Page and the plugin manifest as changed by this work, and the runs that produce the Results_Tables.

## Requirements

### Requirement 1: Judge the reader's terms in the communication cases

**User Story:** As the article's author, I want `lays-out-before-asking` and `user-effect-before-mechanism` graded by a judge that reads whether the message is in Reader_Terms, so that their scores measure the behaviour the communication rule asks for and not a proxy.

#### Acceptance Criteria

1. THE System SHALL give `evals/rules/communication/lays-out-before-asking` a Judge_Grader that passes only when the message lays out each of the ceilings 3, 5 and 10 as what the uploader lives with, recommends one with its reason, and does so before the options are listed.
2. THE System SHALL give `evals/rules/communication/user-effect-before-mechanism` a Judge_Grader that passes only when the final message says what subscribers see in their inbox before it names the failing test or any file.
3. WHEN a Judge_Grader makes a regex grader of the same case redundant, THE System SHALL delete or narrow that Proxy_Grader.
4. THE System SHALL keep each regex grader of these cases that measures a behaviour no Judge_Grader of the case judges, such as the options on separate lines or no narration.
5. IF a Judge_Grader's pass bar could be met by a message that copies the case's README or prompt without laying anything out, THEN THE System SHALL state in the FAIL bar that such a message fails.

### Requirement 2: Judge the reader's terms where the collaboration cases use a proxy

**User Story:** As the article's author, I want any collaboration case that grades the layout of a decision by a proxy to get a Judge_Grader too, so that the collaboration results measure the same behaviour the same way.

#### Acceptance Criteria

1. THE System SHALL give `evals/rules/collaboration/one-open-decision-at-a-time` a Judge_Grader that passes only when the first decision, fixed or exponential backoff, is laid out in Reader_Terms, as what customers' uploads do in a burst under each, with a recommendation and its reason.
2. THE System SHALL leave `evals/rules/collaboration/short-list-asks-with-tool` without a Judge_Grader, because its choice is a short fixed list that the collaboration rule asks to be offered, not laid out.
3. WHEN a collaboration Proxy_Grader is made redundant by a Judge_Grader, THE System SHALL delete or narrow it as Requirement 1.3 says.

### Requirement 3: A case where the choice's natural name is a library

**User Story:** As the article's author, I want one case whose choice is naturally phrased as a library name, so that a result shows whether Claude translates a technical choice into what users live with.

#### Acceptance Criteria

1. THE System SHALL add one case under `evals/rules/communication/` whose project offers a choice between the `requests` and `httpx` libraries for loading a gallery page's thumbnails, and whose README gives what visitors wait through under each.
2. THE System SHALL grade that case with a Judge_Grader that passes only when each option is laid out as what a visitor to the gallery sees, with a recommendation and its reason, before the question.
3. IF the message describes the options only by their technical features, such as async support, connection pooling or HTTP/2, THEN THE Judge_Grader SHALL fail it.
4. THE System SHALL grade, with regex graders, that both options are offered on separate lines and that no file in the workspace is changed.
5. THE System SHALL keep the case gradable with and without the plugin: no grader checks for a plugin skill call.

### Requirement 4: The free checks pass

**User Story:** As the plugin's owner, I want `make validate` to pass on the changed cases, so that every case is reachable, well formed and parses.

#### Acceptance Criteria

1. WHEN the grader and case changes are made, THE System SHALL pass `make validate`.
2. IF `make validate` fails, THEN THE System SHALL fix the cause before any Ablation_Run starts.

### Requirement 5: Rerun every rule eval with and without the plugin

**User Story:** As the article's author, I want every Rule_Target rerun on the current rules with the no-plugin baseline, so that the Evidence_Page's tables are current and comparable.

#### Acceptance Criteria

1. THE System SHALL run an Ablation_Run for each Rule_Target, as `evals/README.md` says, one at a time, never two at once.
2. WHERE `evals/README.md` asks for one `--case` per case with a Judge_Grader, THE System SHALL run those cases with one `--case` each.
3. THE System SHALL set `EVAL_MAX_COST_USD` on each invocation high enough that no Ablation_Run stops early.
4. IF an Ablation_Run stops early, prints a partial table or shows a 300-second timeout, THEN THE System SHALL rerun that target or case alone and keep only the complete table.
5. WHILE Eval_Spend is below $35, THE System SHALL carry on with the next Ablation_Run.
6. IF the next Ablation_Run could take Eval_Spend past $35, THEN THE System SHALL stop and ask Dan, saying the spend so far and what is left to run.
7. THE System SHALL write every run's results only under `evals/results/`, and leave nothing else in the repository.

### Requirement 6: Update the evidence page honestly

**User Story:** As a reader of the Evidence_Page, I want the new tables presented as an adherence check, with their date, plugin version and an honest note on what each grader can and cannot compare, so that I read them as proof the plugin delivers its rules and not as proof its way of working is better.

#### Acceptance Criteria

1. THE System SHALL replace each table on the Evidence_Page with the Results_Table its Ablation_Run printed, unchanged, under a heading that gives the run date and the plugin version.
2. THE System SHALL add the `tests` rule's table and remove it from the Not measured section.
3. THE System SHALL keep, for each Rule_Target, the note on what each case's graders can and cannot compare, saying where a comparison is clean and, for each case where it is not, why.
4. THE System SHALL say, for each case with a Routing_Grader, that its W/OUT score measures that the skill exists, not how Claude behaves.
5. THE System SHALL say which cases have a Judge_Grader and that a judge's verdict is a model's reading against a written bar.
6. THE System SHALL remove the section that lists rule changes made since the 2026-10-22 runs, since the new tables run on the current rules.
7. THE System SHALL introduce the rule tables as an adherence check: a measure of whether Claude follows the plugin's rules when the plugin is loaded.
8. THE System SHALL say, in one sentence, why the rule tables are not a benchmark: plain Claude was never told to behave this way, and the graders encode the rules' own preferences, so the plugin wins by construction.
9. THE System SHALL point to the ReviewBench and Martian results as the evidence with an outside answer key.

### Requirement 7: Bump the plugin version

**User Story:** As the plugin's owner, I want the version bumped, so that the release that carries the new evidence is distinguishable.

#### Acceptance Criteria

1. THE System SHALL change `version` in `plugins/ponderly/.claude-plugin/plugin.json` from 1.6.0 to 1.6.1, a patch bump, since nothing the plugin loads changes.
2. THE System SHALL name 1.6.1 as the plugin version in the Evidence_Page's headings.
