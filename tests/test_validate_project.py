#!/usr/bin/env python3
"""Regression tests for the skill repository validator."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_project.py"
SPEC = importlib.util.spec_from_file_location("validate_project", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


VALID_SHA = "0123456789abcdef0123456789abcdef01234567"


class WorkflowPolicyTests(unittest.TestCase):
    def write_workflow(self, root: Path, uses_line: str) -> None:
        workflow_dir = root / ".github" / "workflows"
        workflow_dir.mkdir(parents=True)
        (workflow_dir / "validate.yml").write_text(
            f"name: Validate\nsteps:\n  - name: Check action\n    {uses_line}\n",
            encoding="utf-8",
        )

    def test_full_sha_with_version_comment_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_workflow(
                root,
                f"uses: actions/checkout@{VALID_SHA} # v7.0.1",
            )

            VALIDATOR.validate_workflows(root)

    def test_mutable_action_ref_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_workflow(root, "uses: actions/checkout@main # v7.0.1")

            with self.assertRaisesRegex(SystemExit, "mutable action ref"):
                VALIDATOR.validate_workflows(root)

    def test_short_action_ref_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_workflow(root, "uses: actions/checkout@v7 # v7.0.1")

            with self.assertRaisesRegex(SystemExit, "full commit SHA"):
                VALIDATOR.validate_workflows(root)

    def test_missing_version_comment_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_workflow(root, f"uses: actions/checkout@{VALID_SHA}")

            with self.assertRaisesRegex(SystemExit, "version comment"):
                VALIDATOR.validate_workflows(root)


class DependabotPolicyTests(unittest.TestCase):
    def test_github_actions_update_configuration_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            github_dir = root / ".github"
            github_dir.mkdir()
            (github_dir / "dependabot.yml").write_text(
                "version: 2\nupdates:\n  - package-ecosystem: github-actions\n    directory: /\n",
                encoding="utf-8",
            )

            VALIDATOR.validate_dependabot(root)

    def test_missing_github_actions_update_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            github_dir = root / ".github"
            github_dir.mkdir()
            (github_dir / "dependabot.yml").write_text(
                "version: 2\nupdates: []\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(SystemExit, "must update GitHub Actions"):
                VALIDATOR.validate_dependabot(root)


class MarkdownPolicyTests(unittest.TestCase):
    def test_balanced_fences_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Example\n\n```php\n<?php\n```\n",
                encoding="utf-8",
            )
            (root / "SKILL.md").write_text("# Example\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
            (root / "references").mkdir()

            VALIDATOR.validate_markdown_fences(root)

    def test_unclosed_fence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n\n```php\n", encoding="utf-8")
            (root / "SKILL.md").write_text("# Example\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
            (root / "references").mkdir()

            with self.assertRaisesRegex(SystemExit, "unclosed"):
                VALIDATOR.validate_markdown_fences(root)

    def write_prose_fixture(self, root: Path, text: str) -> None:
        (root / "README.md").write_text(text, encoding="utf-8")
        (root / "SKILL.md").write_text("# Example\n", encoding="utf-8")
        (root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")
        (root / "references").mkdir()

    def test_valid_prose_ignores_code_and_inline_literals(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_prose_fixture(
                root,
                "# Example\n\n- Use `;` in the regular expression.\n\n```php\n$value = 1;\n```\n",
            )

            VALIDATOR.validate_prose_style(root)

    def test_semicolon_in_prose_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_prose_fixture(root, "# Example\n\nThis sentence has a semicolon; here.\n")

            with self.assertRaisesRegex(SystemExit, "forbidden prose punctuation"):
                VALIDATOR.validate_prose_style(root)

    def test_lowercase_bullet_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_prose_fixture(root, "# Example\n\n- start with lowercase.\n")

            with self.assertRaisesRegex(SystemExit, "lowercase prose"):
                VALIDATOR.validate_prose_style(root)

    def test_research_context_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_prose_fixture(root, "# Example\n\nPoggit is research context only.\n")

            with self.assertRaisesRegex(SystemExit, "research-only context"):
                VALIDATOR.validate_context_boundaries(root)


class ProjectDataTests(unittest.TestCase):
    def write_registries(self, root: Path, role: str = "lab-founder") -> None:
        (root / "roles.json").write_text(
            json.dumps({"roles": [{"id": "lab-founder"}]}),
            encoding="utf-8",
        )
        (root / "members.json").write_text(
            json.dumps({"members": [{"github": "https://github.com/NhanAZ", "roles": ["lab-founder"]}]}),
            encoding="utf-8",
        )
        (root / "projects.json").write_text(
            json.dumps(
                {
                    "projects": [
                        {
                            "id": "axolotl-bucket-labs",
                            "repository": "AxolotlBucketLabs/axolotl-bucket-labs",
                            "status": "active",
                            "assignments": [
                                {
                                    "member": "NhanAZ",
                                    "role": role,
                                    "repositoryPermission": "admin",
                                }
                            ],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        (root / "PROJECTS.md").write_text(
            "The organization currently has 1 active repositories in the registry.\n",
            encoding="utf-8",
        )

    def test_valid_registries_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_registries(root)

            repositories = VALIDATOR.validate_registries(root)

            self.assertEqual(repositories, {"axolotl-bucket-labs"})

    def test_unknown_project_role_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_registries(root, role="missing-role")

            with self.assertRaisesRegex(SystemExit, "unknown role"):
                VALIDATOR.validate_registries(root)

    def test_ruleset_must_match_registry_and_status_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ruleset_dir = root / ".github" / "rulesets" / "main-baseline"
            ruleset_dir.mkdir(parents=True)
            ruleset = {
                "name": "main-baseline",
                "target": "branch",
                "enforcement": "active",
                "conditions": {"ref_name": {"include": ["refs/heads/main"]}},
                "rules": [
                    {
                        "type": "required_status_checks",
                        "parameters": {
                            "required_status_checks": [
                                {"context": VALIDATOR.EXPECTED_STATUS_CHECK}
                            ]
                        },
                    }
                ],
                "bypass_actors": [],
            }
            (ruleset_dir / "axolotl-bucket-labs.json").write_text(
                json.dumps(ruleset),
                encoding="utf-8",
            )

            VALIDATOR.validate_rulesets(root, {"axolotl-bucket-labs"})

            ruleset["rules"][0]["parameters"]["required_status_checks"][0]["context"] = "wrong check"
            (ruleset_dir / "axolotl-bucket-labs.json").write_text(
                json.dumps(ruleset),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "must require"):
                VALIDATOR.validate_rulesets(root, {"axolotl-bucket-labs"})


if __name__ == "__main__":
    unittest.main()
