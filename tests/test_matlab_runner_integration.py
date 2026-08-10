from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPOSITORY_ROOT / "skills" / "matlab-runner"


class MatlabRunnerIntegrationTests(unittest.TestCase):
    def test_public_package_has_required_files(self):
        required = [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "PROVENANCE.yaml",
            "NORMALIZATION.md",
            "CHANGELOG.md",
            "references/client-setup.md",
            "references/file-session-safety.md",
            "references/numerical-safety.md",
            "references/resource-safety.md",
            "examples/README.md",
            "examples/matrix_report.m",
            "examples/plot_damped_sine.m",
            "examples/test_vector_norm.m",
            "tests/scenarios/final-acceptance.md",
        ]
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())

    def test_frontmatter_is_portable_and_discoverable(self):
        content = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        keys = {
            line.split(":", 1)[0].strip()
            for line in frontmatter.splitlines()
            if ":" in line
        }
        self.assertEqual(keys, {"name", "description"})
        self.assertIn("name: matlab-runner", frontmatter)
        self.assertRegex(frontmatter, r"description: [\"']?Use when ")

    def test_canonical_skill_is_coding_agent_neutral(self):
        content = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for forbidden in [
            ".opencode/skills",
            "OpenCode routing",
            "In OpenCode",
            "matlab_evaluate_matlab_code",
            "mcp__matlab__evaluate_matlab_code",
            "C:\\\\Users",
            "WINDIR",
        ]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, content)
        for expected in [
            "inspect the current tool catalog",
            "match capabilities and argument schemas",
            "actual exposed tool name",
            "Do not invent a client-specific prefix",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, content)

    def test_relative_references_are_complete(self):
        content = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for reference in [
            "file-session-safety.md",
            "numerical-safety.md",
            "resource-safety.md",
        ]:
            with self.subTest(reference=reference):
                self.assertIn(f"./references/{reference}", content)
                self.assertTrue((PACKAGE_ROOT / "references" / reference).is_file())

    def test_provenance_records_authorization_and_author(self):
        provenance = yaml.safe_load(
            (PACKAGE_ROOT / "PROVENANCE.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(provenance["schema_version"], 1)
        self.assertEqual(provenance["package_id"], "matlab-runner")
        self.assertEqual(
            provenance["contributor"],
            {
                "public_display_name": "njustar2002",
                "public_email": "njustar2002@vip.163.com",
            },
        )
        self.assertEqual(
            provenance["authorization"]["source_code_publication"],
            "approved",
        )
        self.assertEqual(
            provenance["authorization"]["approval_basis"],
            "repository-owner-confirmation",
        )
        self.assertEqual(
            provenance["authorization"]["target_license"], "MIT"
        )
        self.assertEqual(
            provenance["submission"]["sha256"],
            "4e6b2f3c83abffd28148bcc36d4f96906d64be14b282fed9db2d32c1d89ad5f3",
        )

    def test_repository_metadata_lists_matlab_runner(self):
        registry = (REPOSITORY_ROOT / "skills" / "registry.yaml").read_text(
            encoding="utf-8"
        )
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (REPOSITORY_ROOT / "README.zh-CN.md").read_text(
            encoding="utf-8"
        )
        contributors = (REPOSITORY_ROOT / "CONTRIBUTORS.md").read_text(
            encoding="utf-8"
        )
        for content in [registry, readme, readme_zh, contributors]:
            self.assertIn("matlab-runner", content)
        self.assertIn("njustar2002@vip.163.com", contributors)

    def test_public_tree_excludes_private_or_generated_artifacts(self):
        forbidden_names = {
            ".DS_Store",
            "opencode.json",
            "FINAL_SUBMISSION_AUDIT.md",
        }
        forbidden_suffixes = {".zip", ".tar", ".tgz", ".gz", ".7z", ".rar"}
        found = [
            path.relative_to(PACKAGE_ROOT).as_posix()
            for path in PACKAGE_ROOT.rglob("*")
            if path.name in forbidden_names
            or (path.is_file() and path.suffix.lower() in forbidden_suffixes)
        ]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
