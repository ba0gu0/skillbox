from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_docs.py"
CAPABILITIES: tuple[tuple[str, str], ...] = (
    ("project_identity", "AGENTS.md"),
    ("current_state", "docs/current-state.md"),
    ("next_actions", "docs/next-tasks.md"),
    ("acceptance", "docs/definition-of-done.md"),
    ("red_lines", "AGENTS.md"),
)


def write_file(root: Path, relative_path: str, content: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_valid_project(root: Path) -> tuple[str, ...]:
    files = (
        "AGENTS.md",
        "docs/current-state.md",
        "docs/next-tasks.md",
        "docs/definition-of-done.md",
    )
    write_file(
        root,
        "AGENTS.md",
        "# 项目入口\n\n"
        "## 红线规则\n\n- 不得伪造验证结果。\n\n"
        "[当前状态](docs/current-state.md)\n"
        "[下一步行动](docs/next-tasks.md)\n\n"
        "有效自动链接：<https://example.com>。<br>\n"
        "内联组件示例：`<Component>`。环境变量：`${HOME}`。\n",
    )
    write_file(
        root,
        "docs/current-state.md",
        "# 当前状态\n\n[验收标准](definition-of-done.md)\n",
    )
    write_file(root, "docs/next-tasks.md", "# 下一步任务\n\n- 完成文档校验\n")
    write_file(root, "docs/definition-of-done.md", "# 验收标准\n\n- 链接有效\n")
    return files


def run_validator(
    root: Path,
    files: tuple[str, ...],
    capabilities: tuple[tuple[str, str], ...] = CAPABILITIES,
    *,
    output_format: str = "json",
    locale: str = "en",
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT), "--root", str(root)]
    for relative_path in files:
        command.extend(("--file", relative_path))
    for capability, relative_path in capabilities:
        command.extend(("--require", f"{capability}={relative_path}"))
    command.extend(("--format", output_format, "--locale", locale))
    return subprocess.run(command, check=False, capture_output=True, text=True)


def error_codes(result: subprocess.CompletedProcess[str]) -> set[str]:
    payload = json.loads(result.stdout)
    return {issue["code"] for issue in payload["errors"]}


class ValidateDocsCliTests(unittest.TestCase):
    def test_valid_documents_and_relative_links_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)

            result = run_validator(root, files)

            self.assertEqual(result.returncode, 0, result.stdout)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["valid"])
            self.assertEqual(payload["errors"], [])
            self.assertEqual(payload["summary"]["files"], 4)
            self.assertEqual(
                set(payload["requirements"]), {item[0] for item in CAPABILITIES}
            )

    def test_indirect_entry_routes_are_loaded_automatically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_valid_project(root)
            write_file(
                root,
                "AGENTS.md",
                "# 项目入口\n\n## 红线规则\n\n- 不得伪造验证结果。\n"
                "[当前状态](docs/current-state.md)\n[文档索引](docs/index.md)\n",
            )
            write_file(root, "docs/index.md", "# 下一步索引\n\n[任务](next-tasks.md)\n")

            result = run_validator(root, ("AGENTS.md",))

            self.assertEqual(result.returncode, 0, result.stdout)
            payload = json.loads(result.stdout)
            self.assertIn("docs/index.md", payload["files"])
            self.assertIn("docs/next-tasks.md", payload["files"])

    def test_code_links_and_non_template_html_comments_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            write_file(
                root,
                "docs/next-tasks.md",
                "# 下一步任务\n\n"
                "<!-- generated section boundary -->\n"
                "内联示例：`[缺失](missing-inline.md)`。\n\n"
                "```markdown\n"
                "[缺失](missing-fenced.md)\n"
                "[引用]: missing-reference.md\n"
                "```\n",
            )

            result = run_validator(root, files)

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertNotIn("broken_link", error_codes(result))
            self.assertNotIn("template_comment", error_codes(result))

    def test_existing_capability_file_and_duplicate_file_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            write_file(root, "docs/policies.md", "# 红线规则\n\n- 不提交密钥\n")
            write_file(
                root,
                "AGENTS.md",
                (root / "AGENTS.md").read_text(encoding="utf-8")
                + "[红线](docs/policies.md)\n",
            )
            capabilities = tuple(
                (capability, "docs/policies.md")
                if capability == "red_lines"
                else (capability, path)
                for capability, path in CAPABILITIES
            )

            result = run_validator(root, (*files, files[0]), capabilities)

            self.assertEqual(result.returncode, 0, result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["requirements"]["red_lines"], "docs/policies.md")
            self.assertEqual(
                [item["code"] for item in payload["warnings"]], ["duplicate_file"]
            )

    def test_all_placeholder_families_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            write_file(
                root,
                "docs/next-tasks.md",
                "# {NEXT_TASK}\n"
                "<!-- TEMPLATE META -->\n"
                "{lower_case}\n"
                "{中文变量}\n"
                "[待填充]\n"
                "xxx\n"
                "<slug>\n"
                "＜中文占位＞\n",
            )

            result = run_validator(root, files)

            self.assertNotEqual(result.returncode, 0)
            codes = error_codes(result)
            self.assertTrue(
                {
                    "template_comment",
                    "brace_placeholder",
                    "chinese_brace_placeholder",
                    "fill_placeholder",
                    "xxx_placeholder",
                    "angle_placeholder",
                }.issubset(codes)
            )

    def test_broken_wildcard_and_escaping_links_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            write_file(
                root,
                "docs/next-tasks.md",
                "# 下一步任务\n"
                "[缺失](missing.md)\n"
                "[通配](generated/*.md)\n"
                "[越界](../../outside.md)\n",
            )

            result = run_validator(root, files)

            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(
                {"broken_link", "wildcard_link", "link_outside_root"}.issubset(
                    error_codes(result)
                )
            )

    def test_empty_file_set_is_rejected_in_default_chinese(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            create_valid_project(root)

            result = run_validator(root, (), output_format="text", locale="zh-CN")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("文档验证失败", result.stdout)
            self.assertIn("验证文件集为空", result.stdout)

    def test_file_path_outside_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            root = base / "repository"
            root.mkdir()
            files = create_valid_project(root)
            write_file(base, "outside.md", "# 外部文件\n")

            result = run_validator(root, (*files, "../outside.md"))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("path_outside_root", error_codes(result))

    def test_missing_and_duplicate_capabilities_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            capabilities = (
                ("project_identity", "AGENTS.md"),
                ("project_identity", "AGENTS.md"),
            )

            result = run_validator(root, files, capabilities)

            self.assertNotEqual(result.returncode, 0)
            codes = error_codes(result)
            self.assertIn("duplicate_capability", codes)
            self.assertIn("missing_capability", codes)

    def test_missing_capability_file_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            capabilities = tuple(
                (capability, "docs/missing-dod.md")
                if capability == "acceptance"
                else (capability, path)
                for capability, path in CAPABILITIES
            )

            result = run_validator(root, files, capabilities)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("capability_file_not_found", error_codes(result))

    def test_disconnected_capability_files_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            write_file(
                root, "AGENTS.md", "# 项目入口\n\n## 红线规则\n\n- 不得伪造结果。\n"
            )

            result = run_validator(root, files)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("capability_unreachable", error_codes(result))

    def test_empty_heading_does_not_satisfy_capability_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            files = create_valid_project(root)
            write_file(root, "docs/next-tasks.md", "# Empty\n")

            result = run_validator(root, files)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("capability_content_missing", error_codes(result))


if __name__ == "__main__":
    unittest.main()
