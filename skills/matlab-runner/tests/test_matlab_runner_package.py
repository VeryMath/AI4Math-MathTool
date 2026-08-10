from __future__ import annotations

import re
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class MatlabRunnerPackageTests(unittest.TestCase):
    def test_canonical_files_exist(self):
        for relative_path in [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "PROVENANCE.yaml",
            "NORMALIZATION.md",
            "references/client-setup.md",
            "references/file-session-safety.md",
            "references/numerical-safety.md",
            "references/resource-safety.md",
        ]:
            with self.subTest(path=relative_path):
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())

    def test_frontmatter_is_portable(self):
        content = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        self.assertIsNotNone(match)
        keys = {
            line.split(":", 1)[0].strip()
            for line in match.group(1).splitlines()
            if ":" in line
        }
        self.assertEqual(keys, {"name", "description"})

    def test_tool_routing_uses_capabilities_not_fixed_prefixes(self):
        content = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("inspect the current tool catalog", content)
        self.assertIn("actual exposed tool name", content)
        for forbidden in [
            "matlab_evaluate_matlab_code",
            "mcp__matlab__evaluate_matlab_code",
            ".opencode/skills",
            "C:\\Users",
        ]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, content)

    def test_references_are_relative_and_present(self):
        content = (PACKAGE_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for filename in [
            "file-session-safety.md",
            "numerical-safety.md",
            "resource-safety.md",
        ]:
            self.assertIn(f"./references/{filename}", content)
            self.assertTrue((PACKAGE_ROOT / "references" / filename).is_file())

    def test_no_client_configuration_is_vendored(self):
        forbidden = {"opencode.json", ".DS_Store", "FINAL_SUBMISSION_AUDIT.md"}
        found = [path.name for path in PACKAGE_ROOT.rglob("*") if path.name in forbidden]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
