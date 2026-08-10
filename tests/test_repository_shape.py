from __future__ import annotations

import hashlib
import py_compile
import re
import tempfile
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPOSITORY_ROOT / "skills" / "math-glossary"


def provenance_digests(skills_root: Path) -> set[str]:
    digests = set()
    for provenance_path in sorted(skills_root.glob("*/PROVENANCE.yaml")):
        provenance = yaml.safe_load(
            provenance_path.read_text(encoding="utf-8")
        )
        digest = provenance.get("submission", {}).get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(
            r"[0-9a-f]{64}", digest
        ):
            raise AssertionError(
                f"Invalid submission SHA-256 in {provenance_path}"
            )
        digests.add(digest)
    return digests


def unregistered_archives(
    archives: list[Path], expected_digests: set[str]
) -> list[str]:
    return [
        archive.name
        for archive in archives
        if hashlib.sha256(archive.read_bytes()).hexdigest()
        not in expected_digests
    ]


class RepositoryShapeTests(unittest.TestCase):
    def test_required_repository_files_exist(self):
        required = [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "CONTRIBUTORS.md",
            "LICENSE",
            "THIRD_PARTY.md",
            "SECURITY.md",
            "PUBLISHING.md",
            ".github/workflows/ci.yml",
            "skills/registry.yaml",
        ]
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue(
                    (REPOSITORY_ROOT / relative_path).is_file()
                )

    def test_required_package_files_exist(self):
        required = [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "PROVENANCE.yaml",
            "NORMALIZATION.md",
            "requirements.txt",
            "requirements-ai.txt",
            "agents/openai.yaml",
            "references/glossary-schema.md",
            "references/glossary.schema.json",
            "references/glossary-usage-guide.md",
            "references/glossary-web-template.md",
            "references/user-manual.md",
            "scripts/glossary_backup.py",
            "scripts/glossary_build.py",
            "scripts/glossary_enrich_examples.py",
            "scripts/glossary_export.py",
            "scripts/glossary_web.py",
        ]
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())

    def test_skill_frontmatter_has_only_name_and_description(self):
        content = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        self.assertIsNotNone(match)
        keys = {
            line.split(":", 1)[0].strip()
            for line in match.group(1).splitlines()
            if ":" in line
        }
        self.assertEqual(keys, {"name", "description"})
        self.assertIn("name: math-glossary", match.group(1))

    def test_scripts_compile_with_current_python(self):
        for script in sorted((PACKAGE_ROOT / "scripts").glob("*.py")):
            with self.subTest(script=script.name):
                py_compile.compile(str(script), doraise=True)

    def test_private_archive_is_ignored_and_checksum_matches_when_present(self):
        gitignore = (REPOSITORY_ROOT / ".gitignore").read_text(
            encoding="utf-8"
        )
        self.assertIn(".intake/", gitignore)

        expected_digests = provenance_digests(REPOSITORY_ROOT / "skills")

        archives = list(
            (REPOSITORY_ROOT / ".intake" / "original-submissions").glob("*.zip")
        )
        if not archives:
            self.skipTest("Private intake archive is not present in this checkout")
        self.assertEqual(unregistered_archives(archives, expected_digests), [])

    def test_multiple_private_archives_are_supported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            archive_root = Path(temporary_directory)
            archives = [archive_root / "one.zip", archive_root / "two.zip"]
            archives[0].write_bytes(b"first private submission")
            archives[1].write_bytes(b"second private submission")
            expected_digests = {
                hashlib.sha256(archive.read_bytes()).hexdigest()
                for archive in archives
            }
            self.assertEqual(
                unregistered_archives(archives, expected_digests), []
            )

    def test_released_rights_gate_is_complete(self):
        registry = (
            REPOSITORY_ROOT / "skills" / "registry.yaml"
        ).read_text(encoding="utf-8")
        provenance = (PACKAGE_ROOT / "PROVENANCE.yaml").read_text(
            encoding="utf-8"
        )
        license_text = (REPOSITORY_ROOT / "LICENSE").read_text(
            encoding="utf-8"
        )
        self.assertIn("state: released", registry)
        self.assertIn("publication: public", registry)
        self.assertIn("publication_state: public", provenance)
        self.assertIn("initial_release: v0.1.0", provenance)
        self.assertIn(
            "https://github.com/VeryMath/AI4Math-MathTool",
            provenance,
        )
        self.assertIn("source_code_publication: approved", provenance)
        self.assertIn("target_license: MIT", provenance)
        self.assertIn("third_party_material_review: passed", provenance)
        self.assertIn("blockers: []", registry)
        self.assertIn("blockers: []", provenance)
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Yunfeng Lu and VeryMath contributors", license_text)
        self.assertFalse(
            (REPOSITORY_ROOT / "LICENSE_STATUS.md").exists()
        )

    def test_third_party_boundary_is_documented(self):
        notice = (REPOSITORY_ROOT / "THIRD_PARTY.md").read_text(
            encoding="utf-8"
        )
        for expected in [
            "does not vendor third-party source code",
            "Flask",
            "BSD-3-Clause",
            "openpyxl",
            "MIT/Expat",
            "PyYAML",
            "openai-python",
            "Apache-2.0",
            "mdict-utils",
            "User-supplied dictionaries",
            "do not share one server among multiple users",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, notice)

    def test_ci_runs_repository_and_package_tests(self):
        workflow = (
            REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml"
        ).read_text(encoding="utf-8")
        self.assertIn('python-version: ["3.9", "3.12"]', workflow)
        self.assertIn(
            "python -m unittest discover -s tests -v",
            workflow,
        )
        self.assertIn(
            "python -m unittest discover -s "
            "skills/math-glossary/tests -v",
            workflow,
        )

    def test_contributor_uses_course_romanization_policy(self):
        provenance = (PACKAGE_ROOT / "PROVENANCE.yaml").read_text(
            encoding="utf-8"
        )
        registry = (
            REPOSITORY_ROOT / "skills" / "registry.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("public_display_name: Yunfeng Lu", provenance)
        self.assertIn(
            "display_name_policy: course-roster-romanization",
            provenance,
        )
        self.assertNotIn("public-attribution-preference", registry)


if __name__ == "__main__":
    unittest.main()
