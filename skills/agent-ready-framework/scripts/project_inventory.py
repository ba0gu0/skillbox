#!/usr/bin/env python3
"""Produce a deterministic, read-only inventory for Agent-Ready projects."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Sequence

from _inventory_catalog import (
    LANGUAGE_EXTENSIONS,
    LOCK_NAMES,
    MANIFEST_NAMES,
    MAX_FILES,
    RUNNER_NAMES,
    SKIP_DIRS,
    Locale,
    ecosystem,
    is_agent,
    is_ci,
    is_document,
    parse_options,
)
from _inventory_extractors import (
    Record,
    WarningRecord,
    extract_commands,
    read_text,
    relative,
    text,
    warn,
)

SCHEMA_VERSION = "1.0.0"


def scan_files(root: Path, warnings: list[WarningRecord], locale: Locale) -> list[Path]:
    files: list[Path] = []
    skipped_links = 0

    def on_error(error: OSError) -> None:
        warn(
            warnings,
            "directory_unreadable",
            str(error.filename or root),
            str(error),
            locale,
        )

    for directory, dirnames, filenames in root.walk(top_down=True, on_error=on_error):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        for filename in sorted(filenames):
            path = directory / filename
            if path.is_symlink():
                skipped_links += 1
                continue
            files.append(path)
            if len(files) == MAX_FILES:
                reason = text(
                    locale, "文件数超过安全上限", "file count exceeds the safety limit"
                )
                warn(
                    warnings,
                    "scan_limit_reached",
                    relative(directory, root),
                    reason,
                    locale,
                )
                break
        if len(files) == MAX_FILES:
            break
    if skipped_links:
        reason = text(
            locale,
            f"为避免越出项目边界，跳过 {skipped_links} 个符号链接",
            f"skipped {skipped_links} symlinks to stay within the project boundary",
        )
        warn(warnings, "symlinks_skipped", ".", reason, locale)
    return files


def file_groups(root: Path, files: list[Path]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {
        "agent_instructions": [],
        "documentation": [],
        "manifests": [],
        "lockfiles": [],
        "ci": [],
        "runners": [],
    }
    for path in files:
        item = relative(path, root)
        name = path.name.lower()
        if is_agent(item):
            groups["agent_instructions"].append(item)
        if is_document(item):
            groups["documentation"].append(item)
        if name in MANIFEST_NAMES or path.suffix.lower() in {".csproj", ".sln"}:
            groups["manifests"].append(item)
        if name in LOCK_NAMES:
            groups["lockfiles"].append(item)
        if is_ci(item):
            groups["ci"].append(item)
        if name in RUNNER_NAMES:
            groups["runners"].append(item)
    return {key: sorted(values) for key, values in groups.items()}


def module_roots(manifests: list[str]) -> list[Record]:
    grouped: dict[str, list[str]] = {}
    for item in manifests:
        parent = Path(item).parent.as_posix()
        grouped.setdefault(parent, []).append(Path(item).name)
    return [
        {
            "path": module,
            "kind": "repository_root" if module == "." else "module",
            "manifests": sorted(names),
            "ecosystems": sorted({ecosystem(name) for name in names}),
        }
        for module, names in sorted(grouped.items())
    ]


def language_signals(
    root: Path, files: list[Path], manifests: list[str]
) -> list[Record]:
    counts: dict[str, int] = {}
    evidence: dict[str, list[str]] = {}
    for path in files:
        language = LANGUAGE_EXTENSIONS.get(path.suffix.lower())
        if language is None:
            continue
        counts[language] = counts.get(language, 0) + 1
        if len(evidence.setdefault(language, [])) < 5:
            evidence[language].append(relative(path, root))
    for item in manifests:
        language = ecosystem(Path(item).name)
        if language != "Other" and len(evidence.setdefault(language, [])) < 5:
            evidence[language].append(item)
        counts.setdefault(language, 0)
    return [
        {"language": language, "source_file_count": counts[language], "evidence": paths}
        for language, paths in sorted(evidence.items())
    ]


def bounded_git_path(
    base: Path,
    raw_path: str,
    boundary: Path,
    warnings: list[WarningRecord],
    locale: Locale,
    code: str,
) -> Path | None:
    try:
        resolved = (base / raw_path).resolve(strict=False)
    except (OSError, RuntimeError, ValueError) as error:
        warn(warnings, code, ".git", str(error), locale)
        return None
    if not resolved.is_relative_to(boundary):
        reason = text(
            locale,
            "Git 元数据路径越出允许的项目边界",
            "Git metadata path escapes the allowed project boundary",
        )
        warn(warnings, code, ".git", reason, locale)
        return None
    return resolved


def git_status(root: Path, warnings: list[WarningRecord], locale: Locale) -> Record:
    marker = root / ".git"
    if not marker.exists():
        return {
            "detected": False,
            "git_dir": None,
            "branch": None,
            "head": None,
            "head_state": "not_applicable",
            "worktree_status": "not_applicable",
        }
    marker_path = bounded_git_path(
        root, ".git", root, warnings, locale, "unsafe_git_dir"
    )
    if marker_path is None:
        git_dir: Path | None = None
    elif marker_path.is_file():
        marker_text = read_text(marker_path, root, warnings, locale) or ""
        match = re.match(r"gitdir:\s*(.+)", marker_text)
        if match:
            git_dir = bounded_git_path(
                marker_path.parent,
                match.group(1).strip(),
                root,
                warnings,
                locale,
                "unsafe_git_dir",
            )
        else:
            warn(
                warnings,
                "invalid_git_marker",
                ".git",
                "gitdir target is missing",
                locale,
            )
            git_dir = None
    else:
        git_dir = marker_path
    head_path = (
        bounded_git_path(git_dir, "HEAD", git_dir, warnings, locale, "unsafe_git_head")
        if git_dir is not None
        else None
    )
    head_text = read_text(head_path, root, warnings, locale) if head_path else None
    branch: str | None = None
    commit: str | None = None
    state = "unknown"
    if head_text:
        value = head_text.strip()
        if value.startswith("ref: "):
            reference = value.removeprefix("ref: ")
            valid_reference = re.fullmatch(r"refs/[A-Za-z0-9._/-]+", reference)
            if valid_reference and ".." not in Path(reference).parts and git_dir:
                branch = reference.removeprefix("refs/heads/")
                ref_path = bounded_git_path(
                    git_dir,
                    reference,
                    git_dir,
                    warnings,
                    locale,
                    "unsafe_git_ref",
                )
                ref_text = (
                    read_text(ref_path, root, warnings, locale) if ref_path else None
                )
                candidate = ref_text.strip() if ref_text else ""
                if re.fullmatch(r"[0-9a-fA-F]{40,64}", candidate):
                    commit, state = candidate, "branch"
                elif ref_text is not None:
                    reason = text(
                        locale, "Git 引用不是提交哈希", "Git ref is not a commit hash"
                    )
                    warn(warnings, "invalid_git_ref", ".git", reason, locale)
            else:
                reason = text(locale, "Git 引用路径无效", "Git ref path is invalid")
                warn(warnings, "unsafe_git_ref", ".git", reason, locale)
        elif re.fullmatch(r"[0-9a-fA-F]{40,64}", value):
            commit, state = value, "detached"
    reason = text(
        locale,
        "静态扫描不执行 git，无法判断修改或未跟踪文件",
        "the static scan does not run git, so modified and untracked files are unknown",
    )
    warn(warnings, "git_worktree_not_evaluated", ".git", reason, locale)
    return {
        "detected": True,
        "git_dir": relative(git_dir, root) if git_dir is not None else None,
        "branch": branch,
        "head": commit,
        "head_state": state,
        "worktree_status": "not_evaluated",
    }


def make_evidence(source: str, kind: str, detail: str) -> Record:
    return {"source": source, "kind": kind, "detail": detail}


def document_candidates(
    root: Path,
    docs: list[str],
    pattern: str,
    warnings: list[WarningRecord],
    locale: Locale,
) -> list[str]:
    result: list[str] = []
    heading = re.compile(rf"(?im)^#{{1,6}}\s+.*(?:{pattern})")
    for item in docs:
        if re.search(pattern, item, re.IGNORECASE):
            result.append(item)
            continue
        content = read_text(root / item, root, warnings, locale)
        if content is not None and heading.search(content):
            result.append(item)
    return result


def capabilities(
    root: Path,
    groups: dict[str, list[str]],
    commands: list[Record],
    warnings: list[WarningRecord],
    locale: Locale,
) -> list[Record]:
    docs = groups["documentation"]
    description = [
        path for path in docs if Path(path).name.lower().startswith("readme")
    ]
    description += groups["manifests"][:5] + groups["agent_instructions"][:3]
    current_pattern = (
        r"current[-_ ]?state|project status|progress|当前状态|项目状态|当前进展"
    )
    upcoming_pattern = (
        r"next[-_ ]?(?:tasks|actions)|todo|roadmap|backlog|下一步|待办|任务队列"
    )
    done_pattern = (
        r"definition[-_ ]?of[-_ ]?done|\bdod\b|acceptance|verification matrix|"
        r"完成定义|验收标准|验证矩阵"
    )
    current = document_candidates(root, docs, current_pattern, warnings, locale)
    upcoming = document_candidates(root, docs, upcoming_pattern, warnings, locale)
    done = document_candidates(root, docs, done_pattern, warnings, locale)
    checks = [
        row for row in commands if row["category"] in {"test", "quality", "build"}
    ]
    rule_pattern = (
        r"security|guardrail|red lines?|rules|contributing|安全|红线|不可违反"
    )
    rules = document_candidates(root, docs, rule_pattern, warnings, locale)
    specs: list[tuple[str, str, list[Record]]] = [
        (
            "project_identity",
            text(locale, "项目定位", "Project identity"),
            [
                make_evidence(path, "file", "description candidate")
                for path in description
            ],
        ),
        (
            "current_state",
            text(locale, "当前状态", "Current state"),
            [make_evidence(path, "file", "state candidate") for path in current],
        ),
        (
            "next_actions",
            text(locale, "下一步行动", "Next actions"),
            [make_evidence(path, "file", "task candidate") for path in upcoming],
        ),
        (
            "acceptance",
            text(locale, "验收标准", "Acceptance criteria"),
            [make_evidence(path, "file", "acceptance candidate") for path in done]
            + [
                make_evidence(str(row["source"]), "command", str(row["name"]))
                for row in checks[:10]
            ]
            + [make_evidence(path, "ci", "CI candidate") for path in groups["ci"][:5]],
        ),
        (
            "red_lines",
            text(locale, "红线规则", "Red lines"),
            [
                make_evidence(path, "agent_instruction", "rule candidate")
                for path in groups["agent_instructions"]
            ]
            + [make_evidence(path, "file", "rule candidate") for path in rules],
        ),
    ]
    return [
        {
            "id": key,
            "label": label,
            "status": "candidate" if items else "missing",
            "evidence": items,
        }
        for key, label, items in specs
    ]


def has_entries(root: Path) -> bool:
    try:
        return any(item.name not in {".DS_Store", ".git"} for item in root.iterdir())
    except OSError:
        return True


def build_inventory(root: Path, locale: Locale) -> Record:
    warnings: list[WarningRecord] = []
    files = scan_files(root, warnings, locale)
    groups = file_groups(root, files)
    commands = extract_commands(root, groups, warnings, locale)
    documented = bool(groups["agent_instructions"] or groups["documentation"])
    classification = (
        "documented" if documented else "code-only" if has_entries(root) else "new"
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "root": root.as_posix(),
        "classification": classification,
        "scan": {
            "mode": "read_only_static",
            "files_examined": len(files),
            "commands_executed": False,
            "network_used": False,
            "project_files_written": False,
        },
        "git": git_status(root, warnings, locale),
        "files": groups,
        "module_roots": module_roots(groups["manifests"]),
        "language_signals": language_signals(root, files, groups["manifests"]),
        "commands": commands,
        "capability_candidates": capabilities(root, groups, commands, warnings, locale),
        "warnings": warnings,
    }


def markdown_section(title: str, value: object) -> list[str]:
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    return [f"## {title}", "", "```json", rendered, "```", ""]


def format_markdown(inventory: Record, locale: Locale) -> str:
    class_labels = {
        "new": text(locale, "新项目", "New project"),
        "code-only": text(locale, "有代码无文档", "Code only"),
        "documented": text(locale, "已有文档", "Documented"),
    }
    classification = str(inventory["classification"])
    lines = [
        f"# {text(locale, '项目只读盘点', 'Read-only project inventory')}",
        "",
        f"- Schema: `{inventory['schema_version']}`",
        f"- {text(locale, '项目根目录', 'Project root')}: `{inventory['root']}`",
        f"- {text(locale, '项目分类', 'Classification')}: "
        f"{class_labels[classification]} (`{classification}`)",
        "",
    ]
    sections = (
        (text(locale, "Git 状态", "Git status"), "git"),
        (text(locale, "发现的文件", "Discovered files"), "files"),
        (text(locale, "模块根", "Module roots"), "module_roots"),
        (text(locale, "语言信号", "Language signals"), "language_signals"),
        (text(locale, "可追溯命令候选", "Traceable command candidates"), "commands"),
        (
            text(locale, "五项能力候选证据", "Five capability evidence candidates"),
            "capability_candidates",
        ),
        (text(locale, "警告", "Warnings"), "warnings"),
    )
    for title, key in sections:
        lines += markdown_section(title, inventory[key])
    return "\n".join(lines).rstrip() + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    requested_root, output_format, locale = parse_options(argv)
    try:
        root = requested_root.expanduser().resolve(strict=True)
    except OSError as error:
        zh_prefix = f"无法盘点项目根目录 {requested_root}："
        zh_reason = f"路径不存在或不可访问（{error}）。"
        en_prefix = f"Cannot inventory project root {requested_root}: "
        en_reason = f"missing or inaccessible ({error})."
        message = text(
            locale,
            zh_prefix + zh_reason,
            en_prefix + en_reason,
        )
        print(message, file=sys.stderr)
        return 2
    if not root.is_dir():
        message = text(
            locale,
            f"无法盘点项目根目录 {root}：该路径不是目录。",
            f"Cannot inventory project root {root}: the path is not a directory.",
        )
        print(message, file=sys.stderr)
        return 2
    inventory = build_inventory(root, locale)
    if output_format == "json":
        print(json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(format_markdown(inventory, locale), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
