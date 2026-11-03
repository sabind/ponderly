"""Proves the Message_Pointer that hooks/remind-message.sh attaches to every author message.

The pointer must stay short, name the communication and collaboration rules by
their headings, and quote a line of rules/communication.md verbatim, so a change
to that line fails here, naming it, until the hook's fixed text follows. With no
rules/ folder the hook prints nothing and exits 0.
"""

import os
import tempfile
import unittest

from reminder_harness import PLUGIN, hook_input, make_plugin, run_hook

RULES = os.path.join(PLUGIN, "rules")
SCRIPT = "remind-message.sh"

POINTER_QUOTE = "Lay out a problem, an explanation or a decision as the person it changes will live it."


def read_rule(name):
    with open(os.path.join(RULES, name + ".md"), encoding="utf-8") as f:
        return f.read()


class ReminderMessageTest(unittest.TestCase):
    """The pointer's length, headings and quote, and its silence without rules/."""

    def pointer(self):
        with tempfile.TemporaryDirectory() as folder:
            plugin = make_plugin(folder)
            run = run_hook(
                plugin, SCRIPT, hook_input("UserPromptSubmit"))
        self.assertEqual(run.code, 0)
        self.assertIsNotNone(run.context, "remind-message.sh printed no pointer")
        return run.context

    def test_pointer_is_at_most_500_characters_so_every_message_stays_cheap(self):
        context = self.pointer()

        self.assertLessEqual(len(context), 500, "pointer is %d characters: %r" % (len(context), context))

    def test_pointer_names_the_headings_the_communication_and_collaboration_rules_carry(self):
        context = self.pointer()

        self.assertIn('"Writing to the author"', context)
        self.assertIn('"Working with the author"', context)
        self.assertEqual(read_rule("communication").splitlines()[0], "# Writing to the author")
        self.assertEqual(read_rule("collaboration").splitlines()[0], "# Working with the author")

    def test_quote_that_remind_message_sh_relies_on_appears_verbatim_in_the_communication_rule(self):
        context = self.pointer()

        self.assertIn('"%s"' % POINTER_QUOTE, context)
        self.assertIn(
            POINTER_QUOTE, read_rule("communication"),
            "rules/communication.md no longer holds the line remind-message.sh quotes: %r;"
            " change the hook's pointer and this check with it" % POINTER_QUOTE)

    def test_hook_prints_nothing_and_exits_0_when_the_plugin_has_no_rules_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            plugin = make_plugin(folder, with_rules=False)
            run = run_hook(
                plugin, SCRIPT, hook_input("UserPromptSubmit"))

        self.assertEqual(run.code, 0)
        self.assertIsNone(run.context)


if __name__ == "__main__":
    unittest.main()
