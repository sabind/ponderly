"""Proves the Reminder_Record of hooks/remind-rules.sh: once-only, reset, sweep and failure paths.

Each Agent of a session gets a Rule at most once between two Compactions, kept
in state/<session_id>; a compact SessionStart brings the Rules back, SessionEnd
and the sweep leave no stale record, and any bad id, missing setup, malformed
input or unwritable record makes the hook exit 0 without blocking the tool call,
still attaching the Rule when only the record fails. A bad id clears no file
outside state/. The hook stays within two seconds on a record holding every
Rule for 50 Agents.
"""

import os
import tempfile
import time
import unittest

from reminder_harness import hook_input, make_plugin, record_path, run_hook

SCRIPT = "remind-rules.sh"
CWD = "/repo"
CODE_FILE = "/repo/src/app.py"
OTHER_CODE_FILE = "/repo/src/util.py"
TEST_FILE = "/repo/tests/test_parser.py"
TWO_DAYS = 2 * 24 * 60 * 60
VICTIM_TEXT = "keep me\n"
AWKWARD_LINES = (
    '{"key": "va\\"lue", "list": [1, {"x": "}"}]}\n'
    "path\\to\\file \u00e9\u4e2d\U0001f468\u200d\U0001f469\n"
)


def post_tool(tool_name, file_path, session_id="session-1", agent_id=None):
    return hook_input("PostToolUse", session_id=session_id, cwd=CWD, tool_name=tool_name,
                      file_path=file_path, agent_id=agent_id)


class ReminderRecordTest(unittest.TestCase):
    """Rules come once per Agent until a compact, records are cleaned up, and failures stay silent."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.plugin = make_plugin(os.path.join(folder.name, "plugin"))

    def run_rules(self, stdin, set_root=True):
        return run_hook(self.plugin, SCRIPT, stdin, set_root=set_root)

    def write_victim(self):
        victim = os.path.join(self.plugin, "victim")
        with open(victim, "w", encoding="utf-8") as f:
            f.write(VICTIM_TEXT)
        return victim

    def read_text(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def state_entries(self):
        state = os.path.join(self.plugin, "state")
        if not os.path.isdir(state):
            return []
        return os.listdir(state)

    def test_second_read_of_the_same_kind_brings_nothing(self):
        first = self.run_rules(post_tool("Read", CODE_FILE))
        second = self.run_rules(post_tool("Read", OTHER_CODE_FILE))
        self.assertIn("# Code changes\n", first.context)
        self.assertEqual(second.code, 0)
        self.assertIsNone(second.context)

    def test_write_after_a_read_of_the_same_kind_brings_nothing(self):
        read = self.run_rules(post_tool("Read", CODE_FILE))
        write = self.run_rules(post_tool("Write", OTHER_CODE_FILE))
        self.assertIn("# Code changes\n", read.context)
        self.assertEqual(write.code, 0)
        self.assertIsNone(write.context)

    def test_write_of_a_new_test_file_with_no_read_brings_the_tests_rule(self):
        write = self.run_rules(post_tool("Write", TEST_FILE))
        self.assertEqual(write.code, 0)
        self.assertIn("# Tests\n", write.context)
        self.assertEqual(write.record, ["main tests"])

    def test_read_whose_tool_response_holds_a_large_awkward_file_still_brings_the_rule(self):
        content = AWKWARD_LINES * 2000
        stdin = hook_input("PostToolUse", cwd=CWD, tool_name="Read", file_path=TEST_FILE,
                           tool_response={"type": "text", "file": {"filePath": TEST_FILE, "content": content}})
        run = self.run_rules(stdin)
        self.assertEqual(run.code, 0)
        self.assertIn("# Tests\n", run.context)

    def test_sub_agent_and_main_each_get_the_rule_once(self):
        main = self.run_rules(post_tool("Read", TEST_FILE))
        sub_agent = self.run_rules(post_tool("Read", TEST_FILE, agent_id="agent-7"))
        self.assertIn("# Tests\n", main.context)
        self.assertIn("# Tests\n", sub_agent.context)
        self.assertEqual(sub_agent.record, ["main tests", "agent-7 tests"])

    def test_compact_session_start_brings_the_rule_back(self):
        self.run_rules(post_tool("Read", TEST_FILE))
        self.run_rules(hook_input("SessionStart", source="compact"))
        again = self.run_rules(post_tool("Read", TEST_FILE))
        self.assertIn("# Tests\n", again.context)

    def test_resume_session_start_does_not_bring_the_rule_back(self):
        first = self.run_rules(post_tool("Read", TEST_FILE))
        self.run_rules(hook_input("SessionStart", source="resume"))
        again = self.run_rules(post_tool("Read", TEST_FILE))
        self.assertIn("# Tests\n", first.context)
        self.assertIsNone(again.context)

    def test_session_end_leaves_no_record_file_for_the_session(self):
        self.run_rules(post_tool("Read", TEST_FILE))
        end = self.run_rules(hook_input("SessionEnd"))
        self.assertEqual(end.code, 0)
        self.assertFalse(os.path.exists(record_path(self.plugin, "session-1")))

    def test_session_start_deletes_a_record_last_changed_two_days_ago(self):
        self.run_rules(post_tool("Read", TEST_FILE, session_id="old-session"))
        old = record_path(self.plugin, "old-session")
        two_days_ago = time.time() - TWO_DAYS
        os.utime(old, (two_days_ago, two_days_ago))
        self.run_rules(hook_input("SessionStart", session_id="new-session", source="startup"))
        self.assertFalse(os.path.exists(old))

    def test_invalid_session_id_writes_no_record_and_prints_nothing(self):
        run = self.run_rules(post_tool("Read", TEST_FILE, session_id="../x"))
        self.assertEqual(run.code, 0)
        self.assertIsNone(run.context)
        self.assertEqual(self.state_entries(), [])
        self.assertFalse(os.path.exists(record_path(self.plugin, "../x")))

    def test_session_end_with_a_dot_dot_session_id_leaves_the_file_outside_state_unchanged(self):
        victim = self.write_victim()
        end = self.run_rules(hook_input("SessionEnd", session_id="../victim"))
        self.assertEqual(end.code, 0)
        self.assertEqual(self.read_text(victim), VICTIM_TEXT)

    def test_compact_session_start_with_a_dot_dot_session_id_leaves_the_file_outside_state_unchanged(self):
        victim = self.write_victim()
        start = self.run_rules(hook_input("SessionStart", session_id="../victim", source="compact"))
        self.assertEqual(start.code, 0)
        self.assertEqual(self.read_text(victim), VICTIM_TEXT)

    def test_invalid_agent_id_writes_no_record_and_prints_nothing(self):
        run = self.run_rules(post_tool("Read", TEST_FILE, agent_id="../x"))
        self.assertEqual(run.code, 0)
        self.assertIsNone(run.context)
        self.assertEqual(self.state_entries(), [])

    def test_unset_plugin_root_exits_0_with_no_output(self):
        run = self.run_rules(post_tool("Read", TEST_FILE), set_root=False)
        self.assertEqual(run.code, 0)
        self.assertIsNone(run.context)

    def test_plugin_folder_with_no_rules_exits_0_with_no_output(self):
        with tempfile.TemporaryDirectory() as folder:
            bare = make_plugin(folder, with_rules=False)
            run = run_hook(bare, SCRIPT, post_tool("Read", TEST_FILE))
        self.assertEqual(run.code, 0)
        self.assertIsNone(run.context)

    def test_empty_stdin_exits_0_with_no_output(self):
        run = self.run_rules("")
        self.assertEqual(run.code, 0)
        self.assertIsNone(run.context)

    def test_json_array_on_stdin_exits_0_with_no_output(self):
        run = self.run_rules("[" + post_tool("Read", TEST_FILE) + "]")
        self.assertEqual(run.code, 0)
        self.assertIsNone(run.context)

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root writes through a read-only folder")
    def test_read_only_state_still_brings_the_rule_on_each_of_two_reads(self):
        state = os.path.join(self.plugin, "state")
        os.makedirs(state)
        os.chmod(state, 0o555)
        self.addCleanup(os.chmod, state, 0o755)
        first = self.run_rules(post_tool("Read", TEST_FILE))
        second = self.run_rules(post_tool("Read", TEST_FILE))
        self.assertEqual(first.code, 0)
        self.assertEqual(second.code, 0)
        self.assertIn("# Tests\n", first.context)
        self.assertIn("# Tests\n", second.context)

    def test_hook_finishes_within_two_seconds_on_a_record_holding_every_rule_for_50_agents(self):
        rules = sorted(name[:-3] for name in os.listdir(os.path.join(self.plugin, "rules")))
        lines = ["agent-%d %s\n" % (agent, rule) for agent in range(50) for rule in rules]
        os.makedirs(os.path.join(self.plugin, "state"))
        with open(record_path(self.plugin, "session-1"), "w", encoding="utf-8") as f:
            f.write("".join(lines))
        started = time.monotonic()
        run = self.run_rules(post_tool("Read", CODE_FILE))
        elapsed = time.monotonic() - started
        self.assertIn("# Code changes\n", run.context)
        self.assertLess(elapsed, 2.0)


if __name__ == "__main__":
    unittest.main()
