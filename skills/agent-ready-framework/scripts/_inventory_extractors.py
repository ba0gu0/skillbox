"""Read helpers and traceable command extraction for project_inventory."""

from __future__ import annotations

import json
import re
from pathlib import Path

from _inventory_catalog import MAX_READ_BYTES, Locale, command_category

type Record = dict[str, object]
type WarningRecord = dict[str, str]


def text(locale: Locale, zh_cn: str, en: str) -> str:
    return zh_cn if locale == "zh-CN" else en


def relative(path: Path, root: Path) -> str:
    try:
        value = path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
    return value or "."


def warn(
    warnings: list[WarningRecord], code: str, path: str, reason: str, locale: Locale
) -> None:
    message = text(
        locale,
        f"无法完整盘点 {path}：{reason}。",
        f"Could not fully inventory {path}: {reason}.",
    )
    warnings.append({"code": code, "path": path, "message": message})


def read_text(
    path: Path, root: Path, warnings: list[WarningRecord], locale: Locale
) -> str | None:
    display = relative(path, root)
    try:
        if path.stat().st_size > MAX_READ_BYTES:
            reason = text(locale, "文件超过只读解析上限", "file exceeds the read limit")
            warn(warnings, "file_too_large", display, reason, locale)
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        warn(warnings, "read_failed", display, str(error), locale)
        return None


def package_runner(
    module: str, lockfiles: list[str], declared: object
) -> tuple[tuple[str, str, str] | None, set[str]]:
    choices = {
        "bun.lock": ("bun", "bun run"),
        "bun.lockb": ("bun", "bun run"),
        "pnpm-lock.yaml": ("pnpm", "pnpm run"),
        "yarn.lock": ("yarn", "yarn"),
        "package-lock.json": ("npm", "npm run"),
    }
    lock_candidates = [
        (*choices[Path(item).name.lower()], item)
        for item in lockfiles
        if Path(item).parent.as_posix() == module and Path(item).name.lower() in choices
    ]
    if isinstance(declared, str):
        runner = declared.partition("@")[0]
        prefixes = {
            "bun": "bun run",
            "npm": "npm run",
            "pnpm": "pnpm run",
            "yarn": "yarn",
        }
        if runner in prefixes:
            conflicts = {
                item
                for lock_runner, _, item in lock_candidates
                if lock_runner != runner
            }
            return (runner, prefixes[runner], "package.json#packageManager"), conflicts
    lock_runners = {runner for runner, _, _ in lock_candidates}
    if len(lock_runners) == 1:
        runner, prefix, source = lock_candidates[0]
        return (runner, prefix, source), set()
    return None, {item for _, _, item in lock_candidates}


def package_commands(
    path: Path,
    root: Path,
    locks: list[str],
    warnings: list[WarningRecord],
    locale: Locale,
) -> list[Record]:
    content = read_text(path, root, warnings, locale)
    item = relative(path, root)
    if content is None:
        return []
    try:
        payload: object = json.loads(content)
    except json.JSONDecodeError as error:
        warn(warnings, "invalid_json", item, str(error), locale)
        return []
    if not isinstance(payload, dict):
        warn(
            warnings, "invalid_package_json", item, "JSON root is not an object", locale
        )
        return []
    scripts: object = payload.get("scripts")
    if scripts is None:
        return []
    if not isinstance(scripts, dict):
        warn(
            warnings,
            "invalid_package_scripts",
            item,
            "scripts is not an object",
            locale,
        )
        return []
    module = path.parent.relative_to(root).as_posix()
    runner, conflicts = package_runner(module, locks, payload.get("packageManager"))
    if conflicts:
        sources = ", ".join(sorted(conflicts))
        reason = text(
            locale,
            f"包管理器证据冲突：{sources}",
            f"package-manager evidence conflicts: {sources}",
        )
        warn(warnings, "package_runner_conflict", item, reason, locale)
    if runner is None and scripts:
        reason = text(
            locale,
            "同目录无 lockfile 或 packageManager",
            "no colocated lockfile or packageManager",
        )
        warn(warnings, "package_runner_unknown", item, reason, locale)
    result: list[Record] = []
    for raw_name, raw_value in sorted(scripts.items(), key=lambda pair: str(pair[0])):
        if not isinstance(raw_name, str) or not isinstance(raw_value, str):
            continue
        result.append(
            {
                "category": command_category(raw_name),
                "name": raw_name,
                "invocation": f"{runner[1]} {raw_name}" if runner else None,
                "definition": raw_value,
                "source": f"{item}#scripts.{raw_name}",
                "runner_source": runner[2] if runner else None,
                "module_root": module,
            }
        )
    return result


def taskfile_commands(path: Path, root: Path, content: str) -> list[Record]:
    item = relative(path, root)
    module = path.parent.relative_to(root).as_posix()
    in_tasks = False
    result: list[Record] = []
    for number, line in enumerate(content.splitlines(), start=1):
        if re.match(r"^tasks:\s*(?:#.*)?$", line):
            in_tasks = True
            continue
        if in_tasks and line and not line.startswith((" ", "\t", "#")):
            in_tasks = False
        match = (
            re.match(r"^  ([A-Za-z0-9_.-]+):\s*(?:#.*)?$", line) if in_tasks else None
        )
        if match:
            name = match.group(1)
            result.append(
                {
                    "category": command_category(name),
                    "name": name,
                    "invocation": f"task {name}",
                    "definition": line.strip(),
                    "source": f"{item}:{number}",
                    "runner_source": item,
                    "module_root": module,
                }
            )
    return result


def target_commands(
    path: Path, root: Path, warnings: list[WarningRecord], locale: Locale
) -> list[Record]:
    content = read_text(path, root, warnings, locale)
    if content is None:
        return []
    lowered = path.name.lower()
    if lowered in {"makefile", "gnumakefile"}:
        pattern = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.@/+\-]*):(?!=)")
        runner = "make"
    elif lowered == "justfile":
        pattern = re.compile(r"^@?([A-Za-z_][A-Za-z0-9_-]*)(?:\s+[^:=]+)?:\s*(?:#.*)?$")
        runner = "just"
    else:
        return taskfile_commands(path, root, content)
    item = relative(path, root)
    module = path.parent.relative_to(root).as_posix()
    result: list[Record] = []
    for number, line in enumerate(content.splitlines(), start=1):
        match = pattern.match(line)
        if match is None or match.group(1).startswith("."):
            continue
        name = match.group(1)
        result.append(
            {
                "category": command_category(name),
                "name": name,
                "invocation": f"{runner} {name}",
                "definition": line.strip(),
                "source": f"{item}:{number}",
                "runner_source": item,
                "module_root": module,
            }
        )
    return result


def extract_commands(
    root: Path,
    groups: dict[str, list[str]],
    warnings: list[WarningRecord],
    locale: Locale,
) -> list[Record]:
    result: list[Record] = []
    supported = {"makefile", "gnumakefile", "justfile", "taskfile.yml", "taskfile.yaml"}
    for item in groups["runners"]:
        path = root / item
        if path.name.lower() == "package.json":
            result += package_commands(
                path, root, groups["lockfiles"], warnings, locale
            )
        elif path.name.lower() in supported:
            result += target_commands(path, root, warnings, locale)
    return sorted(result, key=lambda row: (str(row["module_root"]), str(row["source"])))
