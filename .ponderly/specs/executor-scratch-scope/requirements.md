# Requirements Document

## Introduction

The `task-executor` agent shares the session's scratchpad with whatever launched it, and nothing tells it which files there are its own. Its definition says only "Remove every ephemeral check and scratch file before you finish." On 2026-11-01, during a `tighten-tests` run, an executor asked to back up, break and restore one source file ran `rm -rf` on the session's whole run folder, deleting the Baseline records, the Audit's records and the mutation results, and then reported "Then I deleted the copy and its directory." This change gives every executor one folder of its own, named in every ponderly launch prompt, outside which it deletes nothing; makes its Summary list every path it deleted so the launcher can check; keeps each launching skill's own records in a folder of the skill's that the prompt names as off-limits; and has `tighten-tests` run its Mutation_Checks itself after a fix, as it already does in step 8, so no executor is asked to break a source file. It serves the Operator, whose run records survive an executor, and the Owner, who can see from the Summary what was deleted. Issue #82.

## Glossary

- **Executor**: The plugin's `task-executor` agent, defined in `plugins/ponderly/agents/task-executor.md` and launched as `ponderly:task-executor`.
- **Launcher**: Whatever launches the Executor: one of the Launching_Skills, or a person or session by name.
- **Launching_Skills**: The plugin skills that launch the Executor: `start-task`, `implement-spec`, `readable-code` and `tighten-tests`.
- **Operator**: The person running a Launching_Skill in their session, who answers its questions and reads its hand-back.
- **Owner**: The maintainer of the plugin, accountable for what its skills and agents do.
- **Scratchpad**: The session's temporary directory, which the Launcher and every Executor it launches share.
- **Own_Folder**: The one folder under the Scratchpad that belongs to one Executor launch: it holds every scratch file that launch creates, and is the only folder the launch may delete.
- **Run_Folder**: The one folder under the Scratchpad where a Launching_Skill keeps its own records for a run, such as Baseline copies, coverage records and the source state.
- **Launcher_Path**: Any path a launch prompt names that is not inside the Own_Folder, such as a file in the Run_Folder the Executor is told to read.
- **Scratch_Work**: Any file or folder the Executor creates that is not part of the change: an ephemeral check, a backup, a log or a temporary copy.
- **Summary**: The fixed-shape report the Executor returns as its final text.
- **Deleted_List**: The Summary field that lists every path the Executor deleted.
- **Mutation_Check**: As `tighten-tests` defines it: a check that breaks, in one source file, the behaviour a test covers, shows that a test fails, and restores the file at once.
- **Backup_Folder**: As `tighten-tests` defines it: the folder in the system's temporary directory that holds the backup of the one source file a Mutation_Check has broken.

## Requirements

### Requirement 1: The Executor works in its Own_Folder

**User Story:** As an Operator, I want every Executor to keep its scratch work in one folder of its own, so that the records my run keeps in the Scratchpad survive it.

#### Acceptance Criteria

1. THE Executor SHALL keep all of its Scratch_Work inside its Own_Folder.
2. WHERE the launch prompt names an Own_Folder, THE Executor SHALL use that folder, creating it if it does not exist.
3. IF the launch prompt names no Own_Folder, THEN THE Executor SHALL create a new folder under the Scratchpad whose name no existing path uses, and use it as its Own_Folder.
4. WHEN the Executor finishes, whether `done` or `stopped`, THE Executor SHALL delete its Own_Folder.
5. THE Executor SHALL delete no path in the Scratchpad outside its Own_Folder: no Launcher_Path, no folder that holds a Launcher_Path, and no other file or folder.
6. IF a launch prompt asks the Executor to delete a path outside its Own_Folder, THEN THE Executor SHALL leave that path in place and name it, with the words that asked for it quoted, under `unsure` in its Summary.
7. THE Executor SHALL delete no file in the repository except one the change itself removes.

### Requirement 2: The Summary lists every deletion

**User Story:** As an Owner, I want the Executor's Summary to list every path it deleted, so that a deletion outside its Own_Folder is visible instead of hidden behind a description like "deleted the copy".

#### Acceptance Criteria

1. THE Summary SHALL hold a Deleted_List naming, by its full path, every file and folder the Executor deleted during the launch, the Own_Folder included.
2. WHILE the Executor deleted nothing, THE Deleted_List SHALL say `nothing`.
3. THE Deleted_List SHALL name each path exactly as it was passed to the delete command, so a folder deleted with its contents is listed as that folder, not as the files it held.
4. WHEN a Launching_Skill reads a Summary, THE Launching_Skill SHALL check every entry of its Deleted_List against the Own_Folder it named and the files under `files changed`.
5. IF a Deleted_List entry is outside the Own_Folder the launch named and is not a file the change removes, THEN THE Launching_Skill SHALL report it to the Operator as a problem, quoting the entry, before using any record that path held.

### Requirement 3: Every ponderly launch names the Executor's folder and the Launcher's

**User Story:** As an Operator, I want each launch prompt a Launching_Skill writes to say exactly which folder is the Executor's and which paths are the skill's, so that the Executor never has to guess.

#### Acceptance Criteria

1. THE Launching_Skills SHALL name, in every Executor launch prompt, one Own_Folder for that launch, under the Scratchpad and outside any Run_Folder.
2. THE Launching_Skills SHALL give each Executor launched in the same run a different Own_Folder, so that Executors running at once never share one.
3. WHEN a launch prompt names any Launcher_Path, THE launch prompt SHALL say that the path is the Launcher's, that the Executor may read it, and that it must not change or delete it.
4. THE launch prompt SHALL state, in one sentence, that the Executor deletes only its Own_Folder and nothing else in the Scratchpad.
5. WHERE a Launching_Skill relaunches an Executor for the same group of files, THE relaunch prompt SHALL name a new Own_Folder and carry the same Launcher_Path sentences as the first launch.

### Requirement 4: Launching_Skills keep their records in a Run_Folder

**User Story:** As an Operator, I want each skill's own records for a run kept in one named folder, so that a launch prompt can name them as off-limits and the skill can clean them up as a whole.

#### Acceptance Criteria

1. THE `readable-code` skill SHALL keep its Baseline copies and synthesized outputs in its Run_Folder, and give each Executor the Baseline copy paths as Launcher_Paths.
2. THE `tighten-tests` skill SHALL keep its Baseline records, coverage records, source state and Audit records in its Run_Folder, and name the Run_Folder as a Launcher_Path in every Executor launch prompt.
3. WHEN a Launching_Skill reaches the step where it deletes its own records today, THE Launching_Skill SHALL delete its Run_Folder and nothing else.
4. IF a Run_Folder from an earlier run of the same skill already exists when a run starts, THEN THE Launching_Skill SHALL use a new Run_Folder and leave the old one in place.

### Requirement 5: `tighten-tests` runs every Mutation_Check itself

**User Story:** As an Operator, I want the `tighten-tests` session itself to run the Mutation_Check after a step 9 fix, as it does in step 8, so that no Executor is asked to break a source file it was told not to change.

#### Acceptance Criteria

1. WHEN a step 9 fix attempt returns, THE `tighten-tests` skill SHALL run the Mutation_Check for every test the fix changed in the session itself, using the Backup_Folder, as step 8 does.
2. THE `tighten-tests` skill SHALL never ask an Executor to run a Mutation_Check or to back up, change or restore a source file.
3. IF a step 9 Mutation_Check is interrupted, THEN THE next `tighten-tests` run SHALL restore the source file from the Backup_Folder, as its step 1 already does.

### Requirement 6: Documentation and version

**User Story:** As an Owner, I want the plugin's documentation and version to match the new behaviour, so that people who read the docs or update the plugin see the Deleted_List and the folder rule.

#### Acceptance Criteria

1. THE plugin documentation that lists the Summary's fields or describes the Executor's cleanup SHALL describe the Own_Folder rule and the Deleted_List.
2. THE plugin version SHALL move from 1.4.0 to 1.4.1.
3. THE change SHALL pass `make validate`.
4. WHERE the Owner approves its cost, THE Executor's Own_Folder behaviour SHALL be proven by an eval case under `evals/agents/task-executor/`, run by hand.
