from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.build_release_notes import changed_skills
from scripts.compute_next_version import bump_from_labels, validate_version_tag


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_git(*args: str, cwd: Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


class ReleaseNotesTests(unittest.TestCase):
    def test_changed_skills_detects_consolidated_umbrella_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            run_git("init", "-q", cwd=repo)
            run_git("config", "user.email", "tests@example.invalid", cwd=repo)
            run_git("config", "user.name", "Repository Tests", cwd=repo)
            run_git("config", "commit.gpgsign", "false", cwd=repo)

            skill_file = repo / "skills" / "gecode" / "SKILL.md"
            skill_file.parent.mkdir(parents=True)
            skill_file.write_text("initial\n", encoding="utf-8")
            run_git("add", ".", cwd=repo)
            run_git("commit", "-qm", "initial", cwd=repo)
            base = run_git("rev-parse", "HEAD", cwd=repo)

            skill_file.write_text("changed\n", encoding="utf-8")
            run_git("add", ".", cwd=repo)
            run_git("commit", "-qm", "change", cwd=repo)
            head = run_git("rev-parse", "HEAD", cwd=repo)

            self.assertEqual(changed_skills(f"{base}..{head}", cwd=repo), ["gecode"])


class VersionTests(unittest.TestCase):
    def test_release_version_accepts_semver_tag(self) -> None:
        self.assertEqual(validate_version_tag("v1.0.0"), "v1.0.0")

    def test_release_version_rejects_non_semver_and_output_injection(self) -> None:
        invalid_versions = ("6.4.0", "v1.0", "v1.0.0-rc.1", "v1.0.0\nunsafe=true")
        for version in invalid_versions:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    validate_version_tag(version)

    def test_release_label_precedence_is_deterministic(self) -> None:
        self.assertEqual(bump_from_labels([]), "patch")
        self.assertEqual(bump_from_labels(["release:minor"]), "minor")
        self.assertEqual(
            bump_from_labels(["release:minor", "release:major"]), "major"
        )


class SkillGuidanceTests(unittest.TestCase):
    def read_reference(self, name: str) -> str:
        return (REPO_ROOT / "skills" / "gecode" / "references" / name).read_text(
            encoding="utf-8"
        )

    def test_propagator_guidance_uses_public_subsumption_helper(self) -> None:
        guidance = self.read_reference("propagator-implementation.md")
        self.assertIn("home.ES_SUBSUMED(*this)", guidance)
        self.assertIn("Never use the internal `ES_SUBSUMED_`", guidance)

    def test_ngl_guidance_includes_copy(self) -> None:
        guidance = self.read_reference("brancher-implementation.md")
        self.assertIn("`copy`", guidance.split("Implement an NGL class", 1)[1].splitlines()[0])

    def test_portfolio_guidance_uses_seb_builders(self) -> None:
        guidance = self.read_reference("search-engines.md")
        self.assertIn("SEBs", guidance)
        self.assertIn("rbs<Script, BAB>", guidance)
        self.assertNotIn("use `RBS<Script,BAB>`", guidance)

    def test_cmake_guidance_tracks_current_main_requirements(self) -> None:
        guidance = self.read_reference("cmake-consumption.md")
        self.assertIn("6.4.0", guidance)
        self.assertIn("C++17", guidance)
        self.assertIn("GECODE_INSTALL=OFF", guidance)


if __name__ == "__main__":
    unittest.main()
