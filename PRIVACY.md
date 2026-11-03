# Privacy

Last updated: 3 November 2026

ponderly is a plugin for Claude Code. It runs inside your own Claude Code
session, on your own machine. It has no server, and it sends nothing to its
publisher.

## What it stores

The plugin keeps one record of its own: the hooks write, for each session, one
file of the rules each agent has been sent, as `state/<session_id>` under the
plugin's folder. They empty that file on a compaction and when the session
ends, and delete each empty or day-old record file on every session start and
end.

Everything else the plugin writes is yours, written where you work and when
you ask: the designs and specs the skills write under `.ponderly/` in your
repository, the code changes, commits and branches they make there, and the
JSON file `review` writes to a path you name. The plugin keeps no copy.

## What it reads

The skills and agents read the repository you work in, its git history, and
the GitHub issues and pull requests you point them at, through the `git` and
`gh` commands already on your machine. What they read includes the GitHub
names and display names in the issues and comments they read, and the commit
authors' names and email addresses in git history. The plugin stores none of
these. The hooks read only the plugin's own rule files, the input Claude Code
gives them and their own record.

## What it sends

The plugin sends only to GitHub, through your own `git` and `gh`: the issue
comments, pull requests and pushes the skills make for you. The one other
thing it can send is a web search query from the `review-arm` agent, when the
host offers a web search tool. A query holds only the name of a tool outside
your repository and the behaviour in question, never your repository's code, a
file name from it, the repository's name or the pull request.

Claude Code itself sends your session to Anthropic, under Anthropic's own
terms. This page does not cover that.

The full list of commands the plugin runs is in
[What the plugin runs and sends](plugins/claude/ponderly/README.md#what-the-plugin-runs-and-sends).

## Questions

Ask on the [issues page](https://github.com/sabind/ponderly/issues).
