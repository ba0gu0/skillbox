"""Command-line parsing and localized options for validate_docs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

from _validation_support import REQUIRED_CAPABILITIES, Locale, translate

type OutputFormat = Literal["text", "json"]


@dataclass(frozen=True)
class Options:
    root: Path
    files: tuple[str, ...]
    requirements: tuple[str, ...]
    output_format: OutputFormat
    locale: Locale


def parse_args(argv: list[str] | None = None) -> Options:
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--locale", choices=("zh-CN", "en"), default="zh-CN")
    known, _ = pre_parser.parse_known_args(argv)
    locale = cast(Locale, known.locale)
    capabilities = ", ".join(REQUIRED_CAPABILITIES)
    parser = argparse.ArgumentParser(
        description=translate(locale, "cli_description"),
        epilog=translate(locale, "cli_epilog", capabilities=capabilities),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--root", type=Path, default=Path.cwd(), help=translate(locale, "root_help")
    )
    parser.add_argument(
        "--file",
        dest="files",
        action="append",
        default=[],
        metavar="PATH",
        help=translate(locale, "file_help"),
    )
    parser.add_argument(
        "--require",
        dest="requirements",
        action="append",
        default=[],
        metavar="CAPABILITY=PATH",
        help=translate(locale, "require_help"),
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help=translate(locale, "format_help"),
    )
    parser.add_argument(
        "--locale",
        choices=("zh-CN", "en"),
        default="zh-CN",
        help=translate(locale, "locale_help"),
    )
    namespace = parser.parse_args(argv)
    return Options(
        root=namespace.root,
        files=tuple(namespace.files),
        requirements=tuple(namespace.requirements),
        output_format=cast(OutputFormat, namespace.format),
        locale=cast(Locale, namespace.locale),
    )
