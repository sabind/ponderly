---
description: The UserPromptSubmit hook attaches the Message_Pointer to the operator's message.
tags: [hook]
max_turns: 2
expected_outcome: Claude quotes the Ponderly reminder that came with the prompt, its Pointer_Quote included, without using any tool.
---
Without using any tools, answer from what is already in your context: did any system reminder arrive together with this message, as opposed to the rules loaded at session start? If so, quote each such reminder verbatim, in full, one per paragraph. If not, reply exactly NO REMINDER.
