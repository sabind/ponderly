"""Proves hooks/switch-size.sh: it declines a switch from a small session and lets every other call run.

Each test feeds the hook one recorded PreToolUse input against a temporary
transcript, with no model call. The size is the input, cache-read and
cache-creation tokens of the last main-conversation assistant line, or the
postTokens of a main-conversation compaction line that comes after it.
"""

import json
import os
import tempfile
import unittest

from reminder_harness import make_plugin, run_hook_output

SCRIPT = "switch-size.sh"
SWITCH = "ponderly:switch-task"
ONE_STEP = "/ponderly:implement-spec x"
PR_STEP = "/ponderly:pr 12"
OTHER_STEP = "/ponderly:start-task x"


def usage_line(cache_read, cache_creation=1000, input_tokens=2, side_chain=False):
    return json.dumps({
        "type": "assistant",
        "isSidechain": side_chain,
        "message": {"usage": {
            "input_tokens": input_tokens,
            "cache_creation_input_tokens": cache_creation,
            "cache_read_input_tokens": cache_read,
        }},
    })


def boundary_line(post_tokens=None, side_chain=False):
    metadata = {"trigger": "manual", "preTokens": 184284}
    if post_tokens is not None:
        metadata["postTokens"] = post_tokens
    return json.dumps({
        "type": "system",
        "subtype": "compact_boundary",
        "isSidechain": side_chain,
        "content": "Conversation compacted",
        "compactMetadata": metadata,
    })


class SwitchSizeTest(unittest.TestCase):
    """switch-size.sh declines a small switch, adds the size to a large one and ignores all else."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = folder.name
        self.plugin = make_plugin(os.path.join(self.folder, "plugin"))
        self.transcript = os.path.join(self.folder, "transcript.jsonl")

    def write_transcript(self, *lines):
        with open(self.transcript, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def switch_input(self, args=OTHER_STEP, skill=SWITCH, tool_name="Skill", transcript_path=None):
        return json.dumps(ensure_ascii=False, obj={
            "session_id": "s",
            "transcript_path": self.transcript if transcript_path is None else transcript_path,
            "cwd": "/x",
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "tool_input": {"skill": skill, "args": args},
            "tool_use_id": "t",
        })

    def run_switch(self, stdin):
        return run_hook_output(self.plugin, SCRIPT, stdin)

    def decision(self, output):
        return output["hookSpecificOutput"]["permissionDecision"]

    def test_a_session_below_the_limit_is_declined_with_its_size_in_the_reason(self):
        """Property 3: The hook never blocks anything but a small switch."""
        self.write_transcript(usage_line(cache_read=60000))
        code, output = self.run_switch(self.switch_input())
        self.assertEqual(code, 0)
        self.assertEqual(self.decision(output), "deny")
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("61000", reason)
        self.assertIn("Do not retry", reason)
        self.assertIn("each command on a line of its own", reason)
        self.assertIn("150000", reason)
        self.assertIn("type /ponderly:switch-task first in your message", reason)

    def test_a_session_at_the_limit_is_allowed_with_its_size_as_context(self):
        self.write_transcript(usage_line(cache_read=149000, cache_creation=1000, input_tokens=0))
        code, output = self.run_switch(self.switch_input())
        self.assertEqual(code, 0)
        self.assertEqual(self.decision(output), "allow")
        self.assertIn("150000", output["hookSpecificOutput"]["additionalContext"])

    def test_a_size_of_zero_prints_nothing(self):
        self.write_transcript(usage_line(cache_read=0, cache_creation=0, input_tokens=0))
        self.assertEqual(self.run_switch(self.switch_input()), (0, None))

    def test_a_side_chain_usage_line_is_skipped_for_the_main_line_before_it(self):
        self.write_transcript(usage_line(cache_read=60000), usage_line(cache_read=300000, side_chain=True))
        _, output = self.run_switch(self.switch_input())
        self.assertEqual(self.decision(output), "deny")
        self.assertIn("61000", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_a_session_at_the_150000_limit_of_a_pr_next_step_is_allowed(self):
        self.write_transcript(usage_line(cache_read=150000, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args="/ponderly:pr"))
        self.assertEqual(self.decision(output), "allow")

    def test_a_session_one_below_the_150000_limit_of_a_pr_next_step_is_declined(self):
        self.write_transcript(usage_line(cache_read=149999, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args=PR_STEP))
        self.assertEqual(self.decision(output), "deny")

    def test_a_single_implement_spec_next_step_at_110000_is_allowed(self):
        self.write_transcript(usage_line(cache_read=110000, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args=ONE_STEP))
        self.assertEqual(self.decision(output), "allow")

    def test_a_bare_implement_spec_command_as_the_only_next_step_uses_a_limit_of_110000(self):
        self.write_transcript(usage_line(cache_read=110000, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args="/ponderly:implement-spec"))
        self.assertEqual(self.decision(output), "allow")

    def test_a_command_that_only_starts_with_implement_spec_uses_a_limit_of_150000(self):
        self.write_transcript(usage_line(cache_read=110000, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args="/ponderly:implement-specx"))
        self.assertEqual(self.decision(output), "deny")

    def test_a_single_implement_spec_next_step_one_below_110000_is_declined_naming_its_limit(self):
        self.write_transcript(usage_line(cache_read=109999, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args=ONE_STEP))
        self.assertEqual(self.decision(output), "deny")
        self.assertIn("110000", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_an_implement_spec_next_step_followed_by_a_carry_part_uses_110000(self):
        self.write_transcript(usage_line(cache_read=110000, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args=ONE_STEP + "\ncarry: the plan so far"))
        self.assertEqual(self.decision(output), "allow")

    def test_two_next_steps_one_of_them_implement_spec_are_declined_one_below_150000(self):
        self.write_transcript(usage_line(cache_read=149999, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args=PR_STEP + "\n" + ONE_STEP))
        self.assertEqual(self.decision(output), "deny")

    def test_two_next_steps_one_of_them_implement_spec_are_allowed_at_150000(self):
        self.write_transcript(usage_line(cache_read=150000, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input(args=PR_STEP + "\n" + ONE_STEP))
        self.assertEqual(self.decision(output), "allow")

    def test_the_size_in_the_reason_is_rounded_down_to_the_thousand_below(self):
        self.write_transcript(usage_line(cache_read=60600, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input())
        self.assertIn("about 60000 tokens", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_the_size_in_the_context_is_rounded_down_to_the_thousand_below(self):
        self.write_transcript(usage_line(cache_read=150600, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input())
        self.assertEqual(self.decision(output), "allow")
        self.assertIn("150000", output["hookSpecificOutput"]["additionalContext"])

    def test_a_size_just_under_the_limit_is_declined_and_printed_as_the_thousand_below(self):
        self.write_transcript(usage_line(cache_read=149999, cache_creation=0, input_tokens=0))
        _, output = self.run_switch(self.switch_input())
        self.assertEqual(self.decision(output), "deny")
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("about 149000 tokens", reason)
        self.assertNotIn("about 150000 tokens", reason)

    def test_the_bare_skill_name_switch_task_is_another_skill_and_prints_nothing(self):
        self.write_transcript(usage_line(cache_read=60000))
        self.assertEqual(self.run_switch(self.switch_input(skill="switch-task")), (0, None))

    def test_another_skill_prints_nothing(self):
        self.write_transcript(usage_line(cache_read=60000))
        self.assertEqual(self.run_switch(self.switch_input(skill="ponderly:pr")), (0, None))

    def test_another_tool_prints_nothing(self):
        self.write_transcript(usage_line(cache_read=60000))
        self.assertEqual(self.run_switch(self.switch_input(tool_name="Bash")), (0, None))

    def test_a_missing_transcript_prints_nothing(self):
        missing = os.path.join(self.folder, "missing.jsonl")
        self.assertEqual(self.run_switch(self.switch_input(transcript_path=missing)), (0, None))

    def test_input_that_is_not_json_exits_0_and_prints_nothing(self):
        self.assertEqual(self.run_switch("not json {"), (0, None))

    def test_input_of_only_whitespace_exits_0_and_prints_nothing(self):
        self.assertEqual(self.run_switch(" \n\t \n"), (0, None))

    def test_input_after_a_byte_order_mark_exits_0_and_prints_nothing(self):
        self.write_transcript(usage_line(cache_read=60000))
        self.assertEqual(self.run_switch("\ufeff" + self.switch_input()), (0, None))

    def test_args_with_control_characters_are_declined_like_any_small_switch(self):
        self.write_transcript(usage_line(cache_read=60000))
        _, output = self.run_switch(self.switch_input(args=ONE_STEP + "\x01\x1f\u200b\u0000"))
        self.assertEqual(self.decision(output), "deny")

    def test_args_in_non_latin_script_are_declined_like_any_small_switch(self):
        self.write_transcript(usage_line(cache_read=60000))
        _, output = self.run_switch(self.switch_input(args="/ponderly:implement-spec \u4e2d\u6587 \u043f\u0440\u0438\u0432\u0435\u0442"))
        self.assertEqual(self.decision(output), "deny")

    def test_a_request_before_a_compaction_is_declined_at_the_size_the_compaction_left(self):
        self.write_transcript(usage_line(cache_read=181000), boundary_line(post_tokens=33049))
        _, output = self.run_switch(self.switch_input())
        self.assertEqual(self.decision(output), "deny")
        self.assertIn("about 33000 tokens", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_a_request_after_a_compaction_sets_the_size_from_its_usage_and_is_allowed(self):
        self.write_transcript(usage_line(cache_read=181000), boundary_line(post_tokens=33049), usage_line(cache_read=159000))
        _, output = self.run_switch(self.switch_input())
        self.assertEqual(self.decision(output), "allow")
        self.assertIn("160000", output["hookSpecificOutput"]["additionalContext"])

    def test_a_compaction_line_without_post_tokens_leaves_the_size_of_the_request_before_it(self):
        self.write_transcript(usage_line(cache_read=181000), boundary_line())
        _, output = self.run_switch(self.switch_input())
        self.assertEqual(self.decision(output), "allow")
        self.assertIn("182000", output["hookSpecificOutput"]["additionalContext"])

    def test_a_side_chain_compaction_line_is_skipped_for_the_request_before_it(self):
        self.write_transcript(usage_line(cache_read=181000), boundary_line(post_tokens=33049, side_chain=True))
        _, output = self.run_switch(self.switch_input())
        self.assertEqual(self.decision(output), "allow")
        self.assertIn("182000", output["hookSpecificOutput"]["additionalContext"])

    def test_a_compaction_line_with_post_tokens_of_zero_prints_nothing(self):
        self.write_transcript(usage_line(cache_read=181000), boundary_line(post_tokens=0))
        self.assertEqual(self.run_switch(self.switch_input()), (0, None))


if __name__ == "__main__":
    unittest.main()
