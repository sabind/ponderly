"""Proves the properties of hooks/remind-rules.sh that hold across many inputs.

Over a long run of reads and writes by several agents in one session, each agent
is sent each rule at most once and is sent every rule its files bring, since a
repeated rule wastes context and a missing one leaves the agent without it. The
rules a reminder carries are the rule files byte for byte, joined as
load-rules.sh joins them, since a mis-escaped rule would reach the agent garbled.
"""

import os
import random
import shutil
import subprocess
import tempfile
import unittest

from reminder_harness import PLUGIN, hook_input, make_plugin, run_hook

OPENING = (
    "Ponderly rules for the file just read or written."
    " They are the same rules loaded at session start; follow them for this change.\n\n"
)

# NUL is left out: awk cannot carry it as text and it never appears in a rule.
CONTROLS = [chr(c) for c in range(0x01, 0x20)]

CWD = "/work/repo"

# One path per File_Kind, with the rules the design says each kind brings.
FILES_BY_KIND = {
    "spec": (CWD + "/.ponderly/specs/task/tasks.md", {"communication", "workflow"}),
    "test": (CWD + "/tests/test_parser.py", {"tests"}),
    "code": (CWD + "/src/parser.py", {"code-changes", "comments"}),
    "skipped": (CWD + "/README.md", set()),
    "outside": ("/elsewhere/repo/src/parser.py", set()),
}

AGENTS = (None, "agent-a", "agent-b")


def marker(name):
    return "Marker line of the %s rule.\n" % name


def run_load_rules(rules):
    """Returns what load-rules.sh prints, as bytes, for a rules folder holding exactly rules."""
    with tempfile.TemporaryDirectory() as folder:
        os.makedirs(os.path.join(folder, "hooks"))
        shutil.copy2(os.path.join(PLUGIN, "hooks", "load-rules.sh"), os.path.join(folder, "hooks"))
        os.makedirs(os.path.join(folder, "rules"))
        for name, text in rules.items():
            with open(os.path.join(folder, "rules", name + ".md"), "wb") as f:
                f.write(text.encode("utf-8"))
        env = dict(os.environ, CLAUDE_PLUGIN_ROOT=folder)
        run = subprocess.run([os.path.join(folder, "hooks", "load-rules.sh")], capture_output=True, env=env, check=True)
    return run.stdout


def joined_by_load_rules(rules):
    """Returns what load-rules.sh prints after its header for a rules folder holding exactly rules, as str.

    The header is what load-rules.sh prints for a rules folder with no .md file.
    """
    header = run_load_rules({})
    output = run_load_rules(rules)
    assert output.startswith(header), output
    return output[len(header):].decode("utf-8")


def read_rule(name):
    with open(os.path.join(PLUGIN, "rules", name + ".md"), "rb") as f:
        return f.read().decode("utf-8")


class ReminderPropertiesTest(unittest.TestCase):
    """remind-rules.sh sends each rule once per agent, and sends the rule files intact."""

    def test_each_rule_reaches_each_agent_exactly_once_over_a_seeded_session(self):
        """Property 1: Each Rule once per Agent between Compactions.

        200 seeded PostToolUse inputs, Read and Write over three agents and every
        File_Kind, run one after another: no rule appears twice for one agent, and
        by the end each agent has been sent every rule its files bring.
        """
        names = ("code-changes", "comments", "tests", "communication", "workflow", "collaboration")
        rng = random.Random(1)
        with tempfile.TemporaryDirectory() as folder:
            plugin = make_plugin(folder, rules={name: marker(name) for name in names})
            sent = {agent: [] for agent in AGENTS}
            brought = {agent: set() for agent in AGENTS}
            for step in range(200):
                agent = rng.choice(AGENTS)
                kind = rng.choice(sorted(FILES_BY_KIND))
                path, rules = FILES_BY_KIND[kind]
                stdin = hook_input("PostToolUse", cwd=CWD, tool_name=rng.choice(("Read", "Write")),
                                   file_path=path, agent_id=agent)
                run = run_hook(plugin, "remind-rules.sh", stdin)
                self.assertEqual(run.code, 0, "step %d: %s" % (step, stdin))
                brought[agent] |= rules
                if run.context is not None:
                    sent[agent] += [name for name in names if marker(name) in run.context]
        for agent in AGENTS:
            self.assertEqual(len(sent[agent]), len(set(sent[agent])), "agent %r was sent %r" % (agent, sent[agent]))
            self.assertEqual(set(sent[agent]), brought[agent], "agent %r" % agent)

    def test_reminder_carries_awkward_rule_text_byte_for_byte(self):
        """Property 3: The reminder is the rule files, intact.

        Rule files holding quotes, backslashes, every control character from 0x01
        to 0x1f and non-ASCII text decode to the opening sentence, a blank line and
        the two rules a code file brings, joined as load-rules.sh joins them.
        """
        rules = {
            "code-changes": "Say \"quoted\" and 'single' and \\ and \\\" and \\\\n.\n" + "".join(CONTROLS) + "\n",
            "comments": "".join("line " + c + " end\n" for c in CONTROLS) + "é ß 日本語 € 🙂 👩‍👩‍👧\n",
        }
        with tempfile.TemporaryDirectory() as folder:
            plugin = make_plugin(folder, rules=rules)
            stdin = hook_input("PostToolUse", cwd=CWD, tool_name="Write", file_path=FILES_BY_KIND["code"][0])
            run = run_hook(plugin, "remind-rules.sh", stdin)
        self.assertEqual(run.code, 0)
        self.assertEqual(run.context, OPENING + joined_by_load_rules(rules))

    def test_reminder_carries_the_real_code_rules_byte_for_byte(self):
        """Property 3: The reminder is the rule files, intact.

        On the plugin's real rules a code file's reminder decodes to the opening
        sentence, a blank line and code-changes.md then comments.md, joined as
        load-rules.sh joins them.
        """
        with tempfile.TemporaryDirectory() as folder:
            plugin = make_plugin(folder)
            stdin = hook_input("PostToolUse", cwd=CWD, tool_name="Read", file_path=FILES_BY_KIND["code"][0])
            run = run_hook(plugin, "remind-rules.sh", stdin)
        self.assertEqual(run.code, 0)
        rules = {name: read_rule(name) for name in ("code-changes", "comments")}
        self.assertEqual(run.context, OPENING + joined_by_load_rules(rules))


if __name__ == "__main__":
    unittest.main()
