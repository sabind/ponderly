"""Proves how hooks/remind-rules.sh sorts a file into a File_Kind by its path.

A Read or Write of a file brings the rules of its kind: a spec file brings the
communication and workflow rules, a test file the tests rule, and any other file
in the working directory, whatever its extension, the code-changes and comments
rules, each in rule name order. A file outside the working directory, a
document or data file, and an input with no file path bring nothing. The path
alone decides, so no test creates the file it names.
"""

import tempfile
import unittest

from reminder_harness import hook_input, make_plugin, run_hook

CWD = "/work/repo"


def headings(context):
    """Returns the rule headings of a decoded File_Reminder, in order; [] when there is none."""
    if context is None:
        return []
    return [line for line in context.split("\n") if line.startswith("# ")]


class FileKindTest(unittest.TestCase):
    """Each File_Kind brings its rules, and the kinds are tested in the order the spec gives."""

    def reminder_for(self, file_path):
        with tempfile.TemporaryDirectory() as folder:
            plugin = make_plugin(folder)
            run = run_hook(plugin, "remind-rules.sh",
                           hook_input("PostToolUse", cwd=CWD, tool_name="Read", file_path=file_path))
        self.assertEqual(run.code, 0)
        return headings(run.context)

    def test_a_file_outside_the_working_directory_brings_nothing(self):
        self.assertEqual(self.reminder_for("/elsewhere/src/app.py"), [])

    def test_a_file_in_a_sibling_folder_sharing_the_working_directory_prefix_brings_nothing(self):
        self.assertEqual(self.reminder_for("/work/repository/src/app.py"), [])

    def test_a_spec_file_brings_communication_then_workflow(self):
        self.assertEqual(self.reminder_for(CWD + "/.ponderly/specs/task/design.md"),
                         ["# Writing to the author", "# Workflow"])

    def test_a_readme_brings_nothing(self):
        self.assertEqual(self.reminder_for(CWD + "/README.md"), [])

    def test_a_data_file_in_a_tests_folder_brings_nothing(self):
        self.assertEqual(self.reminder_for(CWD + "/tests/data.csv"), [])

    def test_a_helper_in_a_tests_folder_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/tests/helpers.py"), ["# Tests"])

    def test_a_file_in_a_capitalised_tests_folder_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/Tests/Helpers/Stub.swift"), ["# Tests"])

    def test_a_python_test_prefix_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/test_parser.py"), ["# Tests"])

    def test_a_go_test_suffix_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/parser_test.go"), ["# Tests"])

    def test_a_dot_test_name_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/parser.test.ts"), ["# Tests"])

    def test_a_dot_spec_name_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/parser.spec.js"), ["# Tests"])

    def test_a_java_test_class_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/ParserTest.java"), ["# Tests"])

    def test_a_csharp_tests_class_brings_the_tests_rule(self):
        self.assertEqual(self.reminder_for(CWD + "/ParserTests.cs"), ["# Tests"])

    def test_a_source_file_brings_code_changes_then_comments(self):
        self.assertEqual(self.reminder_for(CWD + "/src/app.py"), ["# Code changes", "# Comments"])

    def test_a_file_with_no_extension_is_a_code_file(self):
        self.assertEqual(self.reminder_for(CWD + "/Dockerfile"), ["# Code changes", "# Comments"])

    def test_a_dot_file_is_a_code_file(self):
        self.assertEqual(self.reminder_for(CWD + "/.gitignore"), ["# Code changes", "# Comments"])

    def test_an_upper_case_document_extension_is_skipped(self):
        self.assertEqual(self.reminder_for(CWD + "/NOTES.MD"), [])

    def test_an_input_with_no_file_path_brings_nothing(self):
        self.assertEqual(self.reminder_for(None), [])


if __name__ == "__main__":
    unittest.main()
