"""The rules fit both hooks: past 10,000 characters Claude Code replaces a hook's
output with a file path and a 2,000-character preview, so rules past that point
would not be seen.

The output of hooks/load-rules.sh, the decoded additionalContext of
hooks/load-rules-subagent.sh and the decoded additionalContext of each
hooks/remind-rules.sh reminder, for a spec, a test and a code file, each stay
under 10,000 characters, and each rule named in RULE_LIMITS stays at or under
its own limit, all counted as decoded UTF-8 characters. The reminders run
against a temporary copy of the plugin, so no state/ is written in the
repository.
"""

import json
import os
import subprocess
import tempfile
import unittest

from reminder_harness import hook_input, make_plugin, run_hook

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugins", "ponderly")
LOAD_RULES = os.path.join(PLUGIN, "hooks", "load-rules.sh")
LOAD_RULES_SUBAGENT = os.path.join(PLUGIN, "hooks", "load-rules-subagent.sh")
RULES = os.path.join(PLUGIN, "rules")

HOOK_LIMIT = 10000
RULE_LIMITS = {
    "collaboration": 1600,
    "communication": 1900,
    "tests": 1000,
    "code-changes": 2450,
    "comments": 1450,
}


class RulesSizeTest(unittest.TestCase):
    """The output of both hooks and each limited rule stay within their character limits."""

    def test_hook_output_is_under_the_limit(self):
        env = dict(os.environ, CLAUDE_PLUGIN_ROOT=PLUGIN)
        run = subprocess.run([LOAD_RULES], env=env, capture_output=True, check=True)
        count = len(run.stdout.decode("utf-8"))
        self.assertLess(
            count, HOOK_LIMIT, "load-rules.sh prints %d characters; the limit is %d" % (count, HOOK_LIMIT)
        )

    def test_subagent_context_is_under_the_limit(self):
        env = dict(os.environ, CLAUDE_PLUGIN_ROOT=PLUGIN)
        run = subprocess.run([LOAD_RULES_SUBAGENT], env=env, capture_output=True, check=True)
        context = json.loads(run.stdout.decode("utf-8"))["hookSpecificOutput"]["additionalContext"]
        count = len(context)
        self.assertLess(
            count,
            HOOK_LIMIT,
            "load-rules-subagent.sh gives %d characters of additionalContext; the limit is %d" % (count, HOOK_LIMIT),
        )

    def test_spec_file_reminder_is_under_the_limit(self):
        self.assert_reminder_under_the_limit(os.path.join(".ponderly", "specs", "task", "design.md"))

    def test_test_file_reminder_is_under_the_limit(self):
        self.assert_reminder_under_the_limit(os.path.join("tests", "test_app.py"))

    def test_code_file_reminder_is_under_the_limit(self):
        self.assert_reminder_under_the_limit(os.path.join("src", "app.py"))

    def assert_reminder_under_the_limit(self, relative_path):
        with tempfile.TemporaryDirectory() as folder:
            plugin = make_plugin(os.path.join(folder, "plugin"))
            cwd = os.path.join(folder, "repo")
            stdin = hook_input(
                "PostToolUse", cwd=cwd, tool_name="Read", file_path=os.path.join(cwd, relative_path)
            )
            context = run_hook(plugin, "remind-rules.sh", stdin).context
        self.assertIsNotNone(context, "remind-rules.sh sent no reminder for %s" % relative_path)
        count = len(context)
        self.assertLess(
            count,
            HOOK_LIMIT,
            "remind-rules.sh gives %d characters of additionalContext for %s; the limit is %d"
            % (count, relative_path, HOOK_LIMIT),
        )

    def test_each_rule_is_within_its_limit(self):
        for name, limit in RULE_LIMITS.items():
            with self.subTest(rule=name):
                with open(os.path.join(RULES, name + ".md"), encoding="utf-8") as f:
                    count = len(f.read())
                self.assertLessEqual(
                    count, limit, "rules/%s.md has %d characters; the limit is %d" % (name, count, limit)
                )


if __name__ == "__main__":
    unittest.main()
