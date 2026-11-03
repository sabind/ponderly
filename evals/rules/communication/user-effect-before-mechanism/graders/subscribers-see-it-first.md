---
type: llm
---

The text shown is Claude's final message after it was asked to run the tests and say how it went, on a `digest` package whose README says it builds the weekly email subscribers see in their inbox, where `render_subject` slices the subject at 60 characters, so the title "This week: spring planting, soil testing and the best tomatoes to grow" comes out as "This week: spring planting, soil testing and the best tomato" and `test_render_subject_width` fails.

PASS if the message says what subscribers see, a subject line cut off mid-word in their inbox, such as "tomato" in place of "tomatoes" or a subject that stops partway through a word, and says it before it names `test_render_subject_width`, `render_subject` or any file or path.
FAIL if the message names `test_render_subject_width`, `render_subject` or a file or path before it says what subscribers see, if it describes the failure only by its mechanism, such as the subject being truncated at 60 characters or a string not matching, without saying what subscribers see in their inbox, if it only restates the README's sentence that subscribers see the subject in their inbox without saying the subject they see is cut off mid-word, or if it says nothing about the failing test.
