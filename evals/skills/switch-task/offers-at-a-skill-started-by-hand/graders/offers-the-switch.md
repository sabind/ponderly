---
type: llm
---

The author started start-task by hand with a typed command, in a session that already holds a finished calculator task, the subtract spec run, and no switch message was shown since.

PASS if the reply offers, once and briefly, to switch tasks with the switch-task skill (or a compact first) before starting start-task's work, AND asks the author whether to switch and does nothing further. A sentence saying what the switch saves, before or after the question, is part of the offer.
FAIL if the reply begins any of start-task's steps, such as stating a route, offers more than once, or makes no offer.
