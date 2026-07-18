"""Capability content and route checks for validate_docs."""

from __future__ import annotations

from pathlib import Path

from _validation_support import (
    CAPABILITY_CONTENT_PATTERNS,
    REQUIRED_CAPABILITIES,
    capability_content_matches,
    linked_relative_paths,
)

type DocumentMap = dict[str, tuple[Path, str]]
type Finding = dict[str, str]


def capability_findings(
    mappings: dict[str, str], documents: DocumentMap, root: Path
) -> list[Finding]:
    findings: list[Finding] = []
    for capability in REQUIRED_CAPABILITIES:
        relative = mappings.get(capability)
        document = documents.get(relative or "")
        if document is None:
            continue
        _, content = document
        if not content.strip():
            findings.append(
                {"code": "capability_empty", "capability": capability, "path": relative}
            )
        elif (
            capability not in CAPABILITY_CONTENT_PATTERNS
            or not capability_content_matches(capability, content)
        ):
            findings.append(
                {
                    "code": "capability_content_missing",
                    "capability": capability,
                    "path": relative,
                }
            )
    entry = mappings.get("project_identity")
    if entry not in documents:
        return findings
    graph = {
        relative: linked_relative_paths(path, content, root)
        for relative, (path, content) in documents.items()
    }
    visited: set[str] = set()
    pending = [entry]
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        pending.extend(graph.get(current, set()) - visited)
    for capability in REQUIRED_CAPABILITIES:
        relative = mappings.get(capability)
        if relative is not None and relative not in visited:
            findings.append(
                {
                    "code": "capability_unreachable",
                    "capability": capability,
                    "entry": entry,
                    "path": relative,
                }
            )
    return findings
