"""Static catalog and classifiers used by the read-only project inventory."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Literal, Sequence, cast


type Locale = Literal["zh-CN", "en"]
type OutputFormat = Literal["json", "markdown"]


MAX_FILES = 50_000
MAX_READ_BYTES = 1_000_000
SKIP_DIRS = frozenset(
    """
    .git .hg .svn .cache .mypy_cache .next .pytest_cache .ruff_cache .tox .venv
    __pycache__ build coverage dist node_modules target vendor venv
    """.split()
)
AGENT_NAMES = frozenset(
    ".cursorrules agents.md claude.md cline.md copilot-instructions.md gemini.md".split()
)
DOC_DIRS = frozenset("doc docs documentation spec specs wiki".split())
DOC_PREFIXES = ("readme", "changelog", "contributing", "roadmap", "todo")
DOC_NAMES = frozenset("security.md code_of_conduct.md governance.md".split())
MANIFEST_NAMES = frozenset(
    """
    build.gradle build.gradle.kts build.zig cmakelists.txt composer.json cargo.toml
    deno.json deno.jsonc gemfile go.mod go.work mix.exs package.json package.swift
    pom.xml pubspec.yaml pyproject.toml requirements.txt setup.cfg setup.py
    """.split()
)
LOCK_NAMES = frozenset(
    """
    bun.lock bun.lockb cargo.lock composer.lock gemfile.lock go.sum gradle.lockfile
    mix.lock package-lock.json package.resolved pipfile.lock pnpm-lock.yaml poetry.lock
    pubspec.lock uv.lock yarn.lock
    """.split()
)
RUNNER_NAMES = frozenset(
    """
    gnumakefile justfile makefile noxfile.py package.json rakefile taskfile.yaml
    taskfile.yml tox.ini
    """.split()
)
LANGUAGE_EXTENSIONS = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cs": "C#",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".go": "Go",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".lua": "Lua",
    ".mjs": "JavaScript",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".sh": "Shell",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".zig": "Zig",
}
ECOSYSTEMS = {
    "cargo.toml": "Rust",
    "composer.json": "PHP",
    "gemfile": "Ruby",
    "go.mod": "Go",
    "go.work": "Go",
    "mix.exs": "Elixir",
    "package.swift": "Swift",
    "pom.xml": "JVM",
    "pubspec.yaml": "Dart",
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "setup.cfg": "Python",
    "setup.py": "Python",
    "package.json": "JavaScript/TypeScript",
    "deno.json": "JavaScript/TypeScript",
    "deno.jsonc": "JavaScript/TypeScript",
}


def is_agent(relative_path: str) -> bool:
    lowered = relative_path.lower()
    return (
        Path(lowered).name in AGENT_NAMES
        or lowered == ".github/copilot-instructions.md"
        or lowered.startswith(".github/instructions/")
        or lowered.startswith(".cursor/rules/")
    )


def is_document(relative_path: str) -> bool:
    path = Path(relative_path.lower())
    return (
        path.name.startswith(DOC_PREFIXES)
        or path.name in DOC_NAMES
        or any(part in DOC_DIRS for part in path.parts[:-1])
    )


def is_ci(relative_path: str) -> bool:
    lowered = relative_path.lower()
    exact = {
        ".circleci/config.yml",
        ".gitlab-ci.yml",
        "azure-pipelines.yml",
        "bitbucket-pipelines.yml",
        "jenkinsfile",
    }
    return (
        lowered.startswith(".github/workflows/")
        or lowered.startswith(".buildkite/")
        or lowered in exact
    )


def ecosystem(name: str) -> str:
    lowered = name.lower()
    if lowered.endswith((".csproj", ".sln")):
        return ".NET"
    if lowered.startswith("build.gradle"):
        return "JVM"
    return ECOSYSTEMS.get(lowered, "Other")


def command_category(name: str) -> str:
    rules = (
        (r"(^|[-_:])(test|spec|e2e|check)([-_:]|$)", "test"),
        (r"(^|[-_:])(lint|fmt|format|vet|typecheck)([-_:]|$)", "quality"),
        (r"(^|[-_:])(build|compile|bundle)([-_:]|$)", "build"),
        (r"(^|[-_:])(dev|serve|start|watch|run)([-_:]|$)", "development"),
        (r"(^|[-_:])(install|setup|bootstrap)([-_:]|$)", "install"),
    )
    return next(
        (category for pattern, category in rules if re.search(pattern, name.lower())),
        "other",
    )


def parse_options(argv: Sequence[str] | None) -> tuple[Path, OutputFormat, Locale]:
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--locale", choices=("zh-CN", "en"), default="zh-CN")
    known, _ = pre_parser.parse_known_args(argv)
    locale = cast(Locale, known.locale)
    is_chinese = locale == "zh-CN"
    parser = argparse.ArgumentParser(
        description="只读盘点 Agent-Ready 项目"
        if is_chinese
        else "Read-only project inventory"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="项目根目录（默认当前目录）"
        if is_chinese
        else "project root (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="输出格式" if is_chinese else "output format",
    )
    parser.add_argument(
        "--locale",
        choices=("zh-CN", "en"),
        default="zh-CN",
        help="输出语言" if is_chinese else "output locale",
    )
    options = parser.parse_args(argv)
    return (
        Path(options.root),
        cast(OutputFormat, options.format),
        cast(Locale, options.locale),
    )
