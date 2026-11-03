"""Shared harness for the checks/test_reminder_*.py files.

Builds a temporary plugin folder holding copies of the reminder hook scripts and
of rules/, runs a hook there with a JSON input on stdin, and reads back what it
printed and what it recorded, so no test writes state/ inside the repository.
Not a test file itself: make check does not run it, the reminder checks import it.
"""

import collections
import json
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugins", "ponderly")
HOOKS = ("remind-rules.sh", "remind-message.sh")

HookRun = collections.namedtuple("HookRun", "code context record")


def make_plugin(folder, rules=None, with_rules=True):
    """Fills folder with hooks/ copies of the reminder scripts and a rules/ folder; returns folder.

    rules is a mapping of rule name to text, written as rules/<name>.md; when it
    is None, rules/ is a copy of the plugin's real rules. with_rules False leaves
    rules/ out, for the runs where the hook must do nothing.
    """
    os.makedirs(os.path.join(folder, "hooks"), exist_ok=True)
    for name in HOOKS:
        shutil.copy2(os.path.join(PLUGIN, "hooks", name), os.path.join(folder, "hooks", name))
    if not with_rules:
        return folder
    if rules is None:
        shutil.copytree(os.path.join(PLUGIN, "rules"), os.path.join(folder, "rules"))
        return folder
    os.makedirs(os.path.join(folder, "rules"), exist_ok=True)
    for name, text in rules.items():
        with open(os.path.join(folder, "rules", name + ".md"), "wb") as f:
            f.write(text.encode("utf-8"))
    return folder


def record_path(plugin, session_id):
    """Returns the path of the session's record file, state/<session_id>, under the plugin folder.

    session_id is appended as written, so the path always starts with
    <plugin>/state/, even for an absolute or ../ id.
    """
    return os.path.join(plugin, "state") + os.sep + session_id


def run_hook(plugin, script, stdin, set_root=True):
    """Runs hooks/<script> of the plugin folder with stdin, a str, as its input.

    CLAUDE_PLUGIN_ROOT is the plugin folder when set_root is true and unset
    otherwise. Returns a HookRun of the exit code; the decoded additionalContext,
    or None when the hook printed nothing; and the lines of the record file of
    the input's session_id, or None when there is no such file, the input names
    no session, or the session_id is not a plain file name (it holds a /, a NUL
    or is . or ..). For such an id the record is always None, so a test that
    proves nothing was written lists state/ instead. Raises AssertionError when the hook prints anything other
    than the hook JSON.
    """
    env = dict(os.environ)
    if set_root:
        env["CLAUDE_PLUGIN_ROOT"] = plugin
    else:
        env.pop("CLAUDE_PLUGIN_ROOT", None)
    run = subprocess.run(
        [os.path.join(plugin, "hooks", script)],
        input=stdin.encode("utf-8"),
        capture_output=True,
        env=env,
        timeout=30,
    )
    return HookRun(run.returncode, _decode_context(run.stdout), _read_record(plugin, stdin))


def hook_input(event, session_id="session-1", cwd=None, tool_name=None, file_path=None,
               agent_id=None, source=None, tool_response=None):
    """Returns a one-line hook input JSON, as Claude Code writes it, holding only the fields given.

    file_path goes in tool_input; tool_response is any JSON value. Non-ASCII is
    written raw and / unescaped, as Claude Code writes them.
    """
    fields = {"session_id": session_id, "hook_event_name": event}
    if cwd is not None:
        fields["cwd"] = cwd
    if agent_id is not None:
        fields["agent_id"] = agent_id
    if source is not None:
        fields["source"] = source
    if tool_name is not None:
        fields["tool_name"] = tool_name
    if file_path is not None:
        fields["tool_input"] = {"file_path": file_path}
    if tool_response is not None:
        fields["tool_response"] = tool_response
    return json.dumps(fields, ensure_ascii=False)


def _decode_context(stdout):
    if not stdout:
        return None
    try:
        return json.loads(stdout.decode("utf-8"))["hookSpecificOutput"]["additionalContext"]
    except (ValueError, KeyError, TypeError) as err:
        raise AssertionError("hook output is not the hook JSON (%s): %r" % (err, stdout))


def _read_record(plugin, stdin):
    try:
        session_id = json.loads(stdin)["session_id"]
    except (ValueError, KeyError, TypeError):
        return None
    if not _is_plain_file_name(session_id):
        return None
    try:
        with open(record_path(plugin, session_id), encoding="utf-8") as f:
            return f.read().splitlines()
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
        return None


def _is_plain_file_name(name):
    return isinstance(name, str) and name not in ("", ".", "..") and "/" not in name and "\0" not in name
