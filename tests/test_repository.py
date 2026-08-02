from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import main, validate_reference_graph


class RepositoryStructureTests(unittest.TestCase):
    def test_repository_is_structurally_valid(self) -> None:
        self.assertEqual(main(), 0)

    def test_reference_graph_allows_transitive_routing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir)
            references = skill / "references"
            references.mkdir()
            (skill / "SKILL.md").write_text(
                "Read `references/first.md`.\n", encoding="utf-8"
            )
            (references / "first.md").write_text(
                "Continue to `second.md`.\n", encoding="utf-8"
            )
            (references / "second.md").write_text("Done.\n", encoding="utf-8")

            self.assertEqual(validate_reference_graph(skill), [])

    def test_reference_graph_rejects_missing_and_unreachable_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir)
            references = skill / "references"
            references.mkdir()
            (skill / "SKILL.md").write_text(
                "Read `references/missing.md`.\n", encoding="utf-8"
            )
            (references / "orphan.md").write_text("Unreachable.\n", encoding="utf-8")

            errors = validate_reference_graph(skill)

            self.assertTrue(any("does not exist" in error for error in errors))
            self.assertTrue(any("not reachable" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
