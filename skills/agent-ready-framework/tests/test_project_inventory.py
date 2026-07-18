from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "project_inventory.py"


class ProjectInventoryCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, relative: str, content: str = "") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_cli(
        self,
        root: Path | None = None,
        output_format: str = "json",
        locale: str = "zh-CN",
    ) -> subprocess.CompletedProcess[str]:
        target = root if root is not None else self.root
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(target),
                "--format",
                output_format,
                "--locale",
                locale,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def load_json(
        self, root: Path | None = None, locale: str = "zh-CN"
    ) -> dict[str, object]:
        result = self.run_cli(root=root, locale=locale)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload: object = json.loads(result.stdout)
        self.assertIsInstance(payload, dict)
        return dict(payload) if isinstance(payload, dict) else {}

    def test_classifies_new_code_only_and_documented_projects(self) -> None:
        empty = self.root / "empty"
        code = self.root / "code"
        documented = self.root / "documented"
        empty.mkdir()
        (code / "src").mkdir(parents=True)
        (code / "pyproject.toml").write_text(
            "[project]\nname='demo'\n", encoding="utf-8"
        )
        (code / "src" / "main.py").write_text("print('demo')\n", encoding="utf-8")
        documented.mkdir()
        (documented / "README.md").write_text("# Demo\n", encoding="utf-8")

        self.assertEqual(self.load_json(empty)["classification"], "new")
        code_inventory = self.load_json(code)
        self.assertEqual(code_inventory["classification"], "code-only")
        self.assertIn("pyproject.toml", code_inventory["files"]["manifests"])
        self.assertEqual(self.load_json(documented)["classification"], "documented")

    def test_extracts_traceable_commands_without_executing_them(self) -> None:
        package = {
            "name": "inventory-fixture",
            "scripts": {
                "build": "touch SHOULD_NOT_EXIST",
                "dev": "vite",
                "test": "vitest run",
            },
        }
        self.write("package.json", json.dumps(package))
        self.write("bun.lock")
        self.write("Makefile", "test:\n\t@echo test\n")
        self.write("justfile", "lint:\n    echo lint\n")

        inventory = self.load_json(locale="en")
        commands = inventory["commands"]
        invocations = {row["invocation"] for row in commands}
        sources = {row["source"] for row in commands}

        self.assertIn("bun run test", invocations)
        self.assertIn("make test", invocations)
        self.assertIn("just lint", invocations)
        self.assertIn("package.json#scripts.test", sources)
        self.assertFalse((self.root / "SHOULD_NOT_EXIST").exists())
        self.assertFalse(inventory["scan"]["commands_executed"])
        self.assertFalse(inventory["scan"]["project_files_written"])

    def test_discovers_monorepo_module_roots_and_language_signals(self) -> None:
        self.write("package.json", '{"name":"root"}')
        self.write("packages/ui/package.json", '{"name":"ui"}')
        self.write("packages/ui/src/index.ts", "export const ui = true;\n")
        self.write("packages/ui/README.md", "# UI package\n")
        self.write("services/api/go.mod", "module example.test/api\n\ngo 1.24\n")
        self.write("services/api/main.go", "package main\n")
        self.write("services/api/docs/current-state.md", "# Current state\n")
        self.write("SECURITY.md", "# Security rules\n")

        inventory = self.load_json()
        roots = {row["path"] for row in inventory["module_roots"]}
        languages = {row["language"] for row in inventory["language_signals"]}

        self.assertEqual(roots, {".", "packages/ui", "services/api"})
        self.assertIn("TypeScript", languages)
        self.assertIn("Go", languages)
        self.assertIn("packages/ui/README.md", inventory["files"]["documentation"])
        self.assertIn(
            "services/api/docs/current-state.md",
            inventory["files"]["documentation"],
        )
        self.assertIn("SECURITY.md", inventory["files"]["documentation"])

    def test_package_manager_precedence_and_lock_conflicts_are_explicit(self) -> None:
        package = {
            "name": "runner-conflict",
            "packageManager": "pnpm@10.0.0",
            "scripts": {"test": "vitest run"},
        }
        self.write("package.json", json.dumps(package))
        self.write("package-lock.json", "{}\n")
        self.write("pnpm-lock.yaml", "lockfileVersion: '9.0'\n")

        inventory = self.load_json(locale="en")
        warning_codes = {warning["code"] for warning in inventory["warnings"]}

        self.assertEqual(inventory["commands"][0]["invocation"], "pnpm run test")
        self.assertEqual(
            inventory["commands"][0]["runner_source"],
            "package.json#packageManager",
        )
        self.assertIn("package_runner_conflict", warning_codes)

    def test_ambiguous_lockfiles_do_not_invent_runner_invocation(self) -> None:
        package = {"name": "ambiguous-runner", "scripts": {"test": "vitest run"}}
        self.write("package.json", json.dumps(package))
        self.write("bun.lock", "{}\n")
        self.write("package-lock.json", "{}\n")

        inventory = self.load_json(locale="en")
        warning_codes = {warning["code"] for warning in inventory["warnings"]}

        self.assertIsNone(inventory["commands"][0]["invocation"])
        self.assertIn("package_runner_conflict", warning_codes)

    def test_reports_five_capability_evidence_candidates(self) -> None:
        self.write("README.md", "# Demo\n")
        self.write("AGENTS.md", "# Rules\n")
        self.write("docs/current-state.md", "# Current state\n\n## Next actions\n")
        self.write("docs/definition-of-done.md", "# Definition of Done\n")
        self.write(".github/workflows/ci.yml", "name: CI\n")

        inventory = self.load_json(locale="en")
        candidates = inventory["capability_candidates"]

        self.assertEqual(len(candidates), 5)
        self.assertTrue(all(item["status"] == "candidate" for item in candidates))
        self.assertEqual(
            [item["id"] for item in candidates],
            [
                "project_identity",
                "current_state",
                "next_actions",
                "acceptance",
                "red_lines",
            ],
        )
        self.assertEqual(candidates[0]["label"], "Project identity")
        self.assertEqual(
            candidates[2]["evidence"][0]["source"], "docs/current-state.md"
        )
        self.assertIn(".github/workflows/ci.yml", inventory["files"]["ci"])
        self.assertIn("AGENTS.md", inventory["files"]["agent_instructions"])

    def test_supports_chinese_and_english_json_and_markdown(self) -> None:
        self.write("README.md", "# Demo\n")
        chinese = self.load_json()
        english = self.load_json(locale="en")
        chinese_markdown = self.run_cli(output_format="markdown").stdout
        english_markdown = self.run_cli(output_format="markdown", locale="en").stdout

        self.assertEqual(chinese["capability_candidates"][0]["label"], "项目定位")
        self.assertEqual(
            english["capability_candidates"][0]["label"], "Project identity"
        )
        self.assertIn("# 项目只读盘点", chinese_markdown)
        self.assertIn("## 五项能力候选证据", chinese_markdown)
        self.assertIn("# Read-only project inventory", english_markdown)
        self.assertIn("## Five capability evidence candidates", english_markdown)

    def test_invalid_root_returns_contextual_error(self) -> None:
        missing = self.root / "does-not-exist"
        english = self.run_cli(root=missing, locale="en")
        chinese = self.run_cli(root=missing)

        self.assertEqual(english.returncode, 2)
        self.assertIn("Cannot inventory project root", english.stderr)
        self.assertIn("missing or inaccessible", english.stderr)
        self.assertEqual(chinese.returncode, 2)
        self.assertIn("无法盘点项目根目录", chinese.stderr)
        self.assertIn("路径不存在或不可访问", chinese.stderr)

    def test_git_metadata_cannot_read_outside_its_boundaries(self) -> None:
        project = self.root / "project"
        metadata = self.root / "metadata"
        project.mkdir()
        metadata.mkdir()
        secret = self.root / "secret"
        secret.write_text("a" * 40, encoding="utf-8")
        (project / ".git").write_text("gitdir: ../metadata\n", encoding="utf-8")
        (metadata / "HEAD").write_text("ref: ../secret\n", encoding="utf-8")

        inventory = self.load_json(project)
        warning_codes = {warning["code"] for warning in inventory["warnings"]}

        self.assertIsNone(inventory["git"]["head"])
        self.assertIsNone(inventory["git"]["git_dir"])
        self.assertIn("unsafe_git_dir", warning_codes)
        self.assertNotIn(secret.read_text(encoding="utf-8"), json.dumps(inventory))

        nested_project = self.root / "nested-project"
        nested_metadata = nested_project / "meta"
        nested_metadata.mkdir(parents=True)
        (nested_project / ".git").write_text("gitdir: meta\n", encoding="utf-8")
        (nested_metadata / "HEAD").write_text("ref: ../../secret\n", encoding="utf-8")

        nested_inventory = self.load_json(nested_project)
        nested_warning_codes = {
            warning["code"] for warning in nested_inventory["warnings"]
        }
        self.assertIsNone(nested_inventory["git"]["head"])
        self.assertIn("unsafe_git_ref", nested_warning_codes)
        self.assertNotIn(
            secret.read_text(encoding="utf-8"), json.dumps(nested_inventory)
        )


if __name__ == "__main__":
    unittest.main()
