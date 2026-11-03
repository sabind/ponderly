---
type: llm
---

The text shown is Claude's last message after it was asked to pick, together with the author, the retry ceiling for an upload worker whose README offers 3, 5 or 10 attempts: 3 recovers about 80% of failed jobs and adds about 6 seconds of queue delay, 5 recovers about 95% and adds about 15 seconds, 10 recovers about 97% and adds about 45 seconds, and a job dropped after its last attempt means the uploader has to send the file again. The options are the closing list of choices the question offers, 3, 5 and 10, each on its own line; bullets earlier in the message that describe each ceiling are part of the layout, not that list.

PASS if, before that closing list of options, the message says for each ceiling what the uploader lives with: how often an uploader's file is dropped and has to be sent again, and how long the uploaders whose jobs sit behind a failing one wait for their files to appear. Before the options it also recommends one ceiling and gives the reason in the uploader's terms, such as fewer files to send again being worth a longer wait, or the extra wait not being worth the few files it saves.
FAIL if the message only repeats the README's table or its percentages and seconds without saying what they mean for the uploader, describes the ceilings only by attempts, success rates or queue mechanics, leaves out the dropped file to send again or the wait behind a failing job, gives no recommendation or a recommendation with no reason, or puts the layout or the recommendation only after the options are listed.
