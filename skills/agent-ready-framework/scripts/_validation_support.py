"""Static rules, translations, and Markdown link extraction for validate_docs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from urllib.parse import unquote, urlsplit

type Locale = Literal["zh-CN", "en"]

REQUIRED_CAPABILITIES: tuple[str, ...] = (
    "project_identity",
    "current_state",
    "next_actions",
    "acceptance",
    "red_lines",
)
ANGLE_PATTERN = re.compile(
    r"<[A-Za-z\u3400-\u9fff][^<>\s]*>"
    r"|\uff1c[^\uff1c\uff1e\s]+\uff1e|\u3008[^\u3008\u3009\s]+\u3009"
)
PLACEHOLDER_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("template_comment", re.compile(r"<!--\s*TEMPLATE\b", re.IGNORECASE)),
    (
        "brace_placeholder",
        re.compile(r"(?<![$\\])\{(?:[A-Z][A-Z0-9_-]*|[a-z][a-z0-9]*(?:_[a-z0-9]+)+)\}"),
    ),
    ("chinese_brace_placeholder", re.compile(r"\{[^{}\n]*[\u3400-\u9fff][^{}\n]*\}")),
    ("fill_placeholder", re.compile(r"\[\u5f85\u586b\u5145[^\]\n]*\]?")),
    ("xxx_placeholder", re.compile(r"(?<![\w])xxx(?![\w])", re.IGNORECASE)),
    ("angle_placeholder", ANGLE_PATTERN),
)
REFERENCE_LINK_PATTERN = re.compile(
    r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*(?:<([^>\n]+)>|(\S+))"
)

HTML_TAGS = frozenset(
    """
    a abbr address article aside audio b blockquote body br button canvas caption code
    col colgroup data datalist dd del details dialog div dl dt em embed fieldset figcaption
    figure footer form h1 h2 h3 h4 h5 h6 head header hr html i iframe img input ins kbd
    label legend li link main map mark menu meta meter nav noscript object ol optgroup option
    output p picture pre progress q rp rt ruby s samp script search section select slot small
    source span strong style sub summary sup table tbody td template textarea tfoot th thead
    time title tr track u ul var video wbr
    """.split()
)
CAPABILITY_CONTENT_PATTERNS: dict[str, re.Pattern[str]] = {
    "project_identity": re.compile(
        r"\b(project|purpose|overview|identity|scope|stack)\b|"
        r"项目|定位|用途|边界|技术栈",
        re.IGNORECASE,
    ),
    "current_state": re.compile(
        r"\b(current|status|phase|progress|state)\b|当前|状态|阶段|进展", re.IGNORECASE
    ),
    "next_actions": re.compile(
        r"\b(next|task|todo|backlog|action|priority)\b|下一步|任务|行动|待办|优先级",
        re.IGNORECASE,
    ),
    "acceptance": re.compile(
        r"\b(acceptance|verification|verify|test|build|done|command)\b|"
        r"验收|验证|测试|构建|完成|命令",
        re.IGNORECASE,
    ),
    "red_lines": re.compile(
        r"\b(red lines?|non-negotiable|rules?|forbid|never|must|security|constraint)\b|"
        r"红线|规则|禁止|不得|必须|安全|约束",
        re.IGNORECASE,
    ),
}

MESSAGES: dict[Locale, dict[str, str]] = {
    "zh-CN": {
        "cli_description": "验证 Agent-Ready 最终文档（只读、离线）。",
        "cli_epilog": (
            "核心能力：{capabilities}\n示例：--require project_identity=AGENTS.md"
        ),
        "root_help": "仓库根目录",
        "file_help": "待验证的仓库相对文件路径；可重复",
        "require_help": "能力到仓库相对文件路径的映射；可重复",
        "format_help": "输出格式",
        "locale_help": "输出语言",
        "valid": "文档验证通过",
        "invalid": "文档验证失败",
        "summary": "汇总：{files} 个文件，{errors} 个错误，{warnings} 个警告",
        "error_label": "错误",
        "warning_label": "警告",
        "empty_file_set": "验证文件集为空；至少提供一个 --file。",
        "root_not_directory": "仓库根目录不存在或不是目录：{path}",
        "empty_path": "{kind}路径为空。",
        "absolute_path": "{kind}必须使用仓库根目录相对路径：{path}",
        "outside_root": "{kind}越出仓库根目录：{path}",
        "path_resolution_failed": "无法解析{kind}路径 {path}：{reason}",
        "file_not_found": "验证文件不存在：{path}",
        "not_file": "验证目标不是普通文件：{path}",
        "read_failed": "无法以 UTF-8 读取文件 {path}：{reason}",
        "duplicate_file": "验证文件重复，已忽略后一次：{path}",
        "invalid_requirement": "能力映射必须使用 capability=path：{value}",
        "empty_capability": "能力映射的 capability 不能为空：{value}",
        "duplicate_capability": "能力映射重复：{capability}",
        "missing_capability": "缺少核心能力映射：{capability}",
        "capability_file_missing": "能力 {capability} 映射的文件不存在：{path}",
        "capability_not_file": "能力 {capability} 映射的目标不是文件：{path}",
        "capability_empty": "能力 {capability} 映射的文件没有有效内容：{path}",
        "capability_content_missing": (
            "能力 {capability} 在映射文件中没有可识别内容：{path}"
        ),
        "capability_unreachable": (
            "能力 {capability} 无法从项目入口 {entry} 到达：{path}"
        ),
        "template_comment": "残留 HTML 或模板注释。",
        "brace_placeholder": "残留英文花括号占位符：{value}",
        "chinese_brace_placeholder": "残留中文花括号占位符：{value}",
        "fill_placeholder": "残留待填充占位符：{value}",
        "xxx_placeholder": "残留 xxx 占位符：{value}",
        "angle_placeholder": "残留尖括号占位符：{value}",
        "wildcard_link": "Markdown 链接目标禁止使用通配符：{target}",
        "invalid_link": "无法解析 Markdown 链接目标 {target}：{reason}",
        "link_outside_root": "Markdown 相对链接越出仓库根目录：{target}",
        "broken_link": "Markdown 相对链接目标不存在：{target}",
        "file_kind": "验证文件",
        "capability_kind": "能力映射文件",
    },
    "en": {
        "cli_description": "Validate final Agent-Ready documents (read-only and offline).",
        "cli_epilog": (
            "Core capabilities: {capabilities}\n"
            "Example: --require project_identity=AGENTS.md"
        ),
        "root_help": "repository root",
        "file_help": "repository-relative document to validate; repeatable",
        "require_help": "capability-to-path mapping; repeatable",
        "format_help": "output format",
        "locale_help": "output locale",
        "valid": "Document validation passed",
        "invalid": "Document validation failed",
        "summary": "Summary: {files} files, {errors} errors, {warnings} warnings",
        "error_label": "ERROR",
        "warning_label": "WARNING",
        "empty_file_set": "The validation file set is empty; provide at least one --file.",
        "root_not_directory": "Repository root does not exist or is not a directory: {path}",
        "empty_path": "The {kind} path is empty.",
        "absolute_path": "The {kind} must be relative to the repository root: {path}",
        "outside_root": "The {kind} escapes the repository root: {path}",
        "path_resolution_failed": "Cannot resolve {kind} path {path}: {reason}",
        "file_not_found": "Validation file does not exist: {path}",
        "not_file": "Validation target is not a regular file: {path}",
        "read_failed": "Cannot read {path} as UTF-8: {reason}",
        "duplicate_file": "Duplicate validation file ignored: {path}",
        "invalid_requirement": "Capability mapping must use capability=path: {value}",
        "empty_capability": "Capability cannot be empty in mapping: {value}",
        "duplicate_capability": "Duplicate capability mapping: {capability}",
        "missing_capability": "Missing core capability mapping: {capability}",
        "capability_file_missing": "Mapped file for {capability} does not exist: {path}",
        "capability_not_file": "Mapped target for {capability} is not a file: {path}",
        "capability_empty": "Mapped file for {capability} has no meaningful content: {path}",
        "capability_content_missing": (
            "Mapped file has no recognizable {capability} content: {path}"
        ),
        "capability_unreachable": (
            "Capability {capability} is not reachable from entry {entry}: {path}"
        ),
        "template_comment": "An HTML or template comment remains.",
        "brace_placeholder": "An English brace placeholder remains: {value}",
        "chinese_brace_placeholder": "A Chinese brace placeholder remains: {value}",
        "fill_placeholder": "A fill-in placeholder remains: {value}",
        "xxx_placeholder": "An xxx placeholder remains: {value}",
        "angle_placeholder": "An angle-bracket placeholder remains: {value}",
        "wildcard_link": "Markdown link targets cannot contain wildcards: {target}",
        "invalid_link": "Cannot parse Markdown link target {target}: {reason}",
        "link_outside_root": "Relative Markdown link escapes repository root: {target}",
        "broken_link": "Relative Markdown link target does not exist: {target}",
        "file_kind": "validation file",
        "capability_kind": "capability mapping file",
    },
}


@dataclass(frozen=True)
class LinkTarget:
    target: str
    offset: int


def translate(locale: Locale, key: str, **values: object) -> str:
    return MESSAGES[locale][key].format(**values)


def mask_markdown_code(text: str) -> str:
    masked = list(text)
    fenced = re.compile(r"(?ms)^(?P<fence>`{3,}|~{3,})[^\n]*\n.*?^(?P=fence)[ \t]*$")
    inline = re.compile(r"(?<!`)`+[^`\n]*`+(?!`)")
    for pattern in (fenced, inline):
        for match in pattern.finditer(text):
            for index in range(match.start(), match.end()):
                if masked[index] != "\n":
                    masked[index] = " "
    return "".join(masked)


def is_angle_placeholder(value: str) -> bool:
    inner = value[1:-1].strip()
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", inner):
        return False
    if re.fullmatch(r"[^\s@<>]+@[^\s@<>]+", inner):
        return False
    tag_name = inner.lstrip("/").split(maxsplit=1)[0].rstrip("/").lower()
    return tag_name not in HTML_TAGS


def capability_content_matches(capability: str, content: str) -> bool:
    pattern = CAPABILITY_CONTENT_PATTERNS.get(capability)
    return bool(pattern and pattern.search(mask_markdown_code(content)))


def linked_relative_paths(document: Path, content: str, root: Path) -> set[str]:
    result: set[str] = set()
    for link in extract_links(mask_markdown_code(content)):
        decoded = unquote(link.target)
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", decoded):
            continue
        if decoded.startswith(("//", "/")):
            continue
        path_text = urlsplit(decoded).path
        candidate = document if not path_text else document.parent / path_text
        try:
            resolved = candidate.resolve(strict=False)
        except (OSError, RuntimeError, ValueError):
            continue
        if resolved.is_relative_to(root) and resolved.is_file():
            result.add(resolved.relative_to(root).as_posix())
    return result


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def parse_destination(segment: str) -> tuple[str, int]:
    leading = len(segment) - len(segment.lstrip())
    value = segment.lstrip()
    if not value:
        return "", leading
    if value.startswith("<") and ">" in value[1:]:
        end = value.find(">", 1)
        return value[1:end], leading + 1
    escaped = False
    end = len(value)
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if character.isspace():
            end = index
            break
    target = re.sub(r"\\([\\`*{}\[\]()#+.!<>_-])", r"\1", value[:end])
    return target, leading


def extract_inline_links(text: str) -> list[LinkTarget]:
    links: list[LinkTarget] = []
    cursor = 0
    while True:
        marker = text.find("](", cursor)
        if marker < 0:
            break
        label_start = text.rfind("[", 0, marker)
        if label_start < 0 or is_escaped(text, marker):
            cursor = marker + 2
            continue
        start = marker + 2
        depth = 1
        end = start
        while end < len(text) and depth:
            if not is_escaped(text, end):
                if text[end] == "(":
                    depth += 1
                elif text[end] == ")":
                    depth -= 1
            end += 1
        if depth:
            cursor = marker + 2
            continue
        segment = text[start : end - 1]
        target, relative_offset = parse_destination(segment)
        links.append(LinkTarget(target=target, offset=start + relative_offset))
        cursor = end
    return links


def extract_links(text: str) -> list[LinkTarget]:
    links = extract_inline_links(text)
    for match in REFERENCE_LINK_PATTERN.finditer(text):
        group = 1 if match.group(1) is not None else 2
        target = match.group(group) or ""
        links.append(LinkTarget(target=target, offset=match.start(group)))
    unique = {(link.offset, link.target): link for link in links}
    return sorted(unique.values(), key=lambda link: link.offset)
