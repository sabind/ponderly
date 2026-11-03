"""Every skill's and agent's frontmatter description is present and at most 1,024 characters.

Claude Code rejects a skill description over 1,024 characters, and the validator
gives no warning on the way there. Agent descriptions have no documented limit
but load into every session's context, so they are held to the same ceiling.
"""

import tempfile
import unittest
from pathlib import Path

from frontmatter import read_frontmatter

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "ponderly"
AGENTS_DIR = PLUGIN / "agents"
SKILLS_DIR = PLUGIN / "skills"

DESCRIPTION_LIMIT = 1024


class DescriptionLengthTest(unittest.TestCase):
    def test_descriptions_are_present_and_within_the_limit(self):
        paths = sorted(SKILLS_DIR.glob("*/SKILL.md")) + sorted(AGENTS_DIR.glob("*.md"))
        self.assertTrue(paths, "no skills/*/SKILL.md or agents/*.md found")
        for path in paths:
            with self.subTest(file=str(path.relative_to(ROOT))):
                fields = read_frontmatter(path)
                self.assertIsNotNone(fields, "no frontmatter block between --- fences")
                description = fields.get("description", "")
                self.assertTrue(description, "description is empty or missing")
                self.assertLessEqual(
                    len(description),
                    DESCRIPTION_LIMIT,
                    "description has {} characters; the limit is {}".format(len(description), DESCRIPTION_LIMIT),
                )


class ReadFrontmatterTest(unittest.TestCase):
    """``read_frontmatter`` reads each value the way YAML does, so a long description cannot hide on later lines."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "SKILL.md"

    def description_of(self, frontmatter):
        self.path.write_text("---\n" + frontmatter + "---\nBody.\n", encoding="utf-8")
        return read_frontmatter(self.path)["description"]

    def test_a_folded_block_joins_its_lines_with_spaces(self):
        self.assertEqual(self.description_of("description: >\n  Reads the ticket\n  and fixes it.\nname: bugfix\n"), "Reads the ticket and fixes it.\n")

    def test_a_literal_block_keeps_its_line_breaks(self):
        self.assertEqual(self.description_of("description: |\n  Reads the ticket\n  and fixes it.\n"), "Reads the ticket\nand fixes it.\n")

    def test_a_strip_marker_drops_the_final_line_break(self):
        self.assertEqual(self.description_of("description: >-\n  Reads the ticket.\n"), "Reads the ticket.")

    def test_a_quoted_value_across_lines_is_read_whole_without_its_quotes(self):
        self.assertEqual(self.description_of('description: "Reads the ticket\n  and fixes it."\n'), "Reads the ticket and fixes it.")

    def test_a_plain_value_across_lines_is_read_whole(self):
        self.assertEqual(self.description_of("description: Reads the ticket\n  and fixes it: carefully.\n"), "Reads the ticket and fixes it: carefully.")


if __name__ == "__main__":
    unittest.main()
