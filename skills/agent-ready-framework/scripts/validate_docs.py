#!/usr/bin/env python3
"""Validate generated Agent-Ready Markdown documents without changing the project."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Literal
from urllib.parse import unquote, urlsplit

from _validation_support import (
    PLACEHOLDER_PATTERNS,
    REQUIRED_CAPABILITIES,
    LinkTarget,
    Locale,
    extract_links,
    is_angle_placeholder,
    linked_relative_paths,
    mask_markdown_code,
    translate,
)
from _validation_capabilities import capability_findings
from _validation_cli import parse_args

type Severity = Literal["error", "warning"]
type Location = tuple[str | None, int | None, int | None]


@dataclass(frozen=True)
class Issue:
    severity: Severity
    code: str
    message: str
    file: str | None = None
    line: int | None = None
    column: int | None = None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }
        if self.file is not None:
            result["file"] = self.file
        if self.line is not None:
            result["line"] = self.line
        if self.column is not None:
            result["column"] = self.column
        return result


@dataclass(frozen=True)
class Document:
    path: Path
    relative_path: str
    content: str


def line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    previous_newline = text.rfind("\n", 0, offset)
    return line, offset - previous_newline


class Validator:
    def __init__(self, root: Path, locale: Locale) -> None:
        self.root = root
        self.locale = locale
        self.issues: list[Issue] = []

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    def add(
        self,
        severity: Severity,
        code: str,
        message_key: str,
        location: Location = (None, None, None),
        **values: object,
    ) -> None:
        file, line, column = location
        issue = Issue(
            severity,
            code,
            translate(self.locale, message_key, **values),
            file,
            line,
            column,
        )
        self.issues.append(issue)

    def validate_root(self) -> None:
        if not self.root.is_dir():
            location = (str(self.root), None, None)
            self.add(
                "error",
                "root_not_directory",
                "root_not_directory",
                location,
                path=self.root,
            )

    def resolve_repo_path(self, raw_path: str, kind_key: str) -> Path | None:
        value = raw_path.strip()
        kind = translate(self.locale, kind_key)
        if not value:
            self.add(
                "error", "empty_path", "empty_path", (raw_path, None, None), kind=kind
            )
            return None
        candidate = Path(value)
        if candidate.is_absolute() or PureWindowsPath(value).is_absolute():
            location = (value, None, None)
            self.add(
                "error",
                "absolute_path",
                "absolute_path",
                location,
                kind=kind,
                path=value,
            )
            return None
        try:
            resolved = (self.root / candidate).resolve(strict=False)
        except (OSError, RuntimeError, ValueError) as error:
            location = (value, None, None)
            self.add(
                "error",
                "path_resolution_failed",
                "path_resolution_failed",
                location,
                kind=kind,
                path=value,
                reason=error,
            )
            return None
        if not resolved.is_relative_to(self.root):
            location = (value, None, None)
            self.add(
                "error",
                "path_outside_root",
                "outside_root",
                location,
                kind=kind,
                path=value,
            )
            return None
        return resolved

    def load_documents(self, raw_files: tuple[str, ...]) -> list[Document]:
        if not raw_files:
            self.add("error", "empty_file_set", "empty_file_set")
            return []
        documents: list[Document] = []
        seen: set[Path] = set()
        for raw_path in raw_files:
            path = self.resolve_repo_path(raw_path, "file_kind")
            if path is None:
                continue
            relative = path.relative_to(self.root).as_posix()
            location = (relative, None, None)
            if path in seen:
                self.add(
                    "warning",
                    "duplicate_file",
                    "duplicate_file",
                    location,
                    path=relative,
                )
                continue
            seen.add(path)
            if not path.exists():
                self.add(
                    "error", "file_not_found", "file_not_found", location, path=relative
                )
                continue
            if not path.is_file():
                self.add("error", "not_file", "not_file", location, path=relative)
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                self.add(
                    "error",
                    "read_failed",
                    "read_failed",
                    location,
                    path=relative,
                    reason=error,
                )
                continue
            documents.append(Document(path, relative, content))
        return documents

    def load_linked_documents(self, documents: list[Document]) -> None:
        text_suffixes = {".md", ".mdx", ".markdown", ".rst", ".txt", ""}
        loaded = {document.relative_path for document in documents}
        pending = list(documents)
        while pending and len(loaded) < 256:
            document = pending.pop()
            targets = {
                target
                for target in linked_relative_paths(
                    document.path, document.content, self.root
                )
                if Path(target).suffix.lower() in text_suffixes and target not in loaded
            }
            if not targets:
                continue
            additions = self.load_documents(tuple(sorted(targets)))
            documents.extend(additions)
            loaded.update(document.relative_path for document in additions)
            pending.extend(additions)

    def parse_requirements(self, raw_values: tuple[str, ...]) -> dict[str, str]:
        mappings: dict[str, str] = {}
        for raw_value in raw_values:
            capability, separator, raw_path = raw_value.partition("=")
            capability = capability.strip()
            raw_path = raw_path.strip()
            if not separator:
                self.add(
                    "error",
                    "invalid_requirement",
                    "invalid_requirement",
                    value=raw_value,
                )
                continue
            if not capability:
                self.add(
                    "error", "empty_capability", "empty_capability", value=raw_value
                )
                continue
            if capability in mappings:
                self.add(
                    "error",
                    "duplicate_capability",
                    "duplicate_capability",
                    capability=capability,
                )
                continue
            mappings[capability] = raw_path
        for capability in REQUIRED_CAPABILITIES:
            if capability not in mappings:
                self.add(
                    "error",
                    "missing_capability",
                    "missing_capability",
                    capability=capability,
                )
        return mappings

    def validate_requirements(self, mappings: dict[str, str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for capability, raw_path in mappings.items():
            path = self.resolve_repo_path(raw_path, "capability_kind")
            if path is None:
                continue
            relative = path.relative_to(self.root).as_posix()
            normalized[capability] = relative
            location = (relative, None, None)
            if not path.exists():
                self.add(
                    "error",
                    "capability_file_not_found",
                    "capability_file_missing",
                    location,
                    capability=capability,
                    path=relative,
                )
            elif not path.is_file():
                self.add(
                    "error",
                    "capability_not_file",
                    "capability_not_file",
                    location,
                    capability=capability,
                    path=relative,
                )
        return normalized

    def scan_document(self, document: Document) -> None:
        prose = mask_markdown_code(document.content)
        for code, pattern in PLACEHOLDER_PATTERNS:
            scan_text = document.content if code == "brace_placeholder" else prose
            for match in pattern.finditer(scan_text):
                value = match.group(0)
                if code == "angle_placeholder" and not is_angle_placeholder(value):
                    continue
                if (
                    code == "brace_placeholder"
                    and value[1].islower()
                    and prose[match.start()] == " "
                ):
                    continue
                line, column = line_column(document.content, match.start())
                location = (document.relative_path, line, column)
                self.add("error", code, code, location, value=value)
        for link in extract_links(prose):
            self.validate_link(document, link)

    def validate_capabilities(
        self, mappings: dict[str, str], documents: list[Document]
    ) -> None:
        document_map = {
            document.relative_path: (document.path, document.content)
            for document in documents
        }
        for finding in capability_findings(mappings, document_map, self.root):
            path = finding["path"]
            location = (
                (path, 1, 1)
                if finding["code"] != "capability_unreachable"
                else (path, None, None)
            )
            values = {key: value for key, value in finding.items() if key != "code"}
            self.add(
                "error",
                finding["code"],
                finding["code"],
                location,
                **values,
            )

    def validate_link(self, document: Document, link: LinkTarget) -> None:
        line, column = line_column(document.content, link.offset)
        location = (document.relative_path, line, column)
        decoded = unquote(link.target)
        if "*" in decoded:
            self.add(
                "error", "wildcard_link", "wildcard_link", location, target=link.target
            )
            return
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", decoded):
            return
        if decoded.startswith(("//", "/")):
            return
        try:
            path_text = urlsplit(decoded).path
            candidate = (
                document.path if not path_text else document.path.parent / path_text
            )
            resolved = candidate.resolve(strict=False)
        except (OSError, RuntimeError, ValueError) as error:
            self.add(
                "error",
                "invalid_link",
                "invalid_link",
                location,
                target=link.target,
                reason=error,
            )
            return
        if not resolved.is_relative_to(self.root):
            self.add(
                "error",
                "link_outside_root",
                "link_outside_root",
                location,
                target=link.target,
            )
        elif not resolved.exists():
            self.add(
                "error", "broken_link", "broken_link", location, target=link.target
            )


def build_payload(
    validator: Validator,
    documents: list[Document],
    requirements: dict[str, str],
) -> dict[str, object]:
    errors = validator.errors
    warnings = validator.warnings
    return {
        "valid": not errors,
        "root": str(validator.root),
        "files": [document.relative_path for document in documents],
        "requirements": requirements,
        "errors": [issue.to_dict() for issue in errors],
        "warnings": [issue.to_dict() for issue in warnings],
        "summary": {
            "files": len(documents),
            "errors": len(errors),
            "warnings": len(warnings),
        },
    }


def render_text(validator: Validator, documents: list[Document]) -> str:
    errors = validator.errors
    warnings = validator.warnings
    title_key = "invalid" if errors else "valid"
    lines = [translate(validator.locale, title_key)]
    for issue in (*errors, *warnings):
        label_key = "error_label" if issue.severity == "error" else "warning_label"
        location = issue.file or "-"
        if issue.line is not None:
            location += f":{issue.line}"
            if issue.column is not None:
                location += f":{issue.column}"
        label = translate(validator.locale, label_key)
        lines.append(f"[{label}] {issue.code} {location}: {issue.message}")
    summary = translate(
        validator.locale,
        "summary",
        files=len(documents),
        errors=len(errors),
        warnings=len(warnings),
    )
    lines.append(summary)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    options = parse_args(argv)
    root = options.root.expanduser().resolve(strict=False)
    validator = Validator(root, options.locale)
    validator.validate_root()
    mappings = validator.parse_requirements(options.requirements)
    requirements = validator.validate_requirements(mappings)
    documents = validator.load_documents(options.files)
    loaded_paths = {document.relative_path for document in documents}
    mapped_files = tuple(
        path
        for path in dict.fromkeys(requirements.values())
        if path not in loaded_paths
    )
    if mapped_files:
        documents.extend(validator.load_documents(mapped_files))
    validator.load_linked_documents(documents)
    for document in documents:
        validator.scan_document(document)
    validator.validate_capabilities(requirements, documents)
    payload = build_payload(validator, documents, requirements)
    if options.output_format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(validator, documents))
    return 1 if validator.errors else 0


if __name__ == "__main__":
    sys.exit(main())
