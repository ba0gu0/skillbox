#!/usr/bin/env python3
"""jina-web: read web pages and search the internet via Jina AI APIs.

Usage:
    jina-web read <url>                          # markdown
    jina-web read <url> --format text            # plain text
    jina-web read <url> --target "article"       # CSS selector
    jina-web read <url> --no-images --json       # JSON, no images
    jina-web search "query"                      # web search
    jina-web search "query" --type news --json   # news search, JSON

Env: JINA_API_KEY (optional, for higher rate limits)
"""

import json
import os
import subprocess
import sys
import urllib.parse

READ_BASE = "https://r.jina.ai"
SEARCH_BASE = "https://s.jina.ai"

HAS_REQUESTS = False
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    pass


def http_get(url, headers, timeout=30):
    if HAS_REQUESTS:
        r = requests.get(url, headers=headers, timeout=timeout)
        return r.text
    h_args = []
    for k, v in headers.items():
        h_args += ["-H", f"{k}: {v}"]
    r = subprocess.run(
        ["curl", "-sS", "--max-time", str(timeout)] + h_args + [url],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"Error: curl failed: {r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r.stdout


def build_headers(json_output, fmt, no_cache, proxy,
                  target, wait_for, remove,
                  no_images, no_links,
                  with_links_summary, with_images_summary):
    headers = {}
    api_key = os.environ.get("JINA_API_KEY", "")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    headers["Accept"] = "application/json" if json_output else "text/plain"

    fmt_map = {
        "markdown": "markdown", "text": "text", "html": "html",
        "screenshot": "screenshot", "pageshot": "pageshot",
    }
    if fmt in fmt_map:
        headers["X-Respond-With"] = fmt_map[fmt]

    if no_cache:
        headers["X-No-Cache"] = "true"
    if proxy:
        headers["X-Proxy-Url"] = proxy
    if target:
        headers["X-Target-Selector"] = target
    if wait_for:
        headers["X-Wait-For-Selector"] = wait_for
    if remove:
        headers["X-Remove-Selector"] = remove
    if no_images:
        headers["X-Retain-Images"] = "none"
    if no_links:
        headers["X-Retain-Links"] = "none"
    if with_links_summary:
        headers["X-With-Links-Summary"] = "true"
    if with_images_summary:
        headers["X-With-Images-Summary"] = "true"

    return headers


def do_read(url, **kwargs):
    timeout = kwargs.pop("timeout", 30)
    headers = build_headers(**kwargs)
    full_url = f"{READ_BASE}/{url}"
    print(f"[jina] Reading: {url}", file=sys.stderr)
    result = http_get(full_url, headers, timeout)
    print(result)


def do_search(query, engine="", search_type="", budget="", **kwargs):
    timeout = kwargs.pop("timeout", 30)
    headers = build_headers(**kwargs)
    params = {"q": query}
    if engine:
        params["engine"] = engine
    if search_type:
        params["type"] = search_type
    if budget:
        params["tokenBudget"] = budget
    qs = urllib.parse.urlencode(params)
    full_url = f"{SEARCH_BASE}/search?{qs}"
    print(f"[jina] Searching: {query}", file=sys.stderr)
    result = http_get(full_url, headers, timeout)
    print(result)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    mode = args[0]
    if mode not in ("read", "search"):
        print(f"Error: unknown command '{mode}'. Use 'read' or 'search'.")
        sys.exit(1)

    if len(args) < 2:
        print(f"Error: missing argument for '{mode}'.")
        sys.exit(1)

    input_val = args[1]
    opts = {
        "json_output": False, "fmt": "markdown", "no_cache": False,
        "proxy": "", "target": "", "wait_for": "", "remove": "",
        "no_images": False, "no_links": False,
        "with_links_summary": False, "with_images_summary": False,
        "timeout": 30,
    }
    search_opts = {"engine": "", "search_type": "", "budget": ""}

    i = 2
    while i < len(args):
        a = args[i]
        if a == "--json":
            opts["json_output"] = True; i += 1
        elif a == "--no-cache":
            opts["no_cache"] = True; i += 1
        elif a == "--proxy" and i + 1 < len(args):
            opts["proxy"] = args[i + 1]; i += 2
        elif a == "--format" and i + 1 < len(args):
            opts["fmt"] = args[i + 1]; i += 2
        elif a == "--timeout" and i + 1 < len(args):
            opts["timeout"] = int(args[i + 1]); i += 2
        elif a == "--target" and i + 1 < len(args):
            opts["target"] = args[i + 1]; i += 2
        elif a == "--wait-for" and i + 1 < len(args):
            opts["wait_for"] = args[i + 1]; i += 2
        elif a == "--remove" and i + 1 < len(args):
            opts["remove"] = args[i + 1]; i += 2
        elif a == "--no-images":
            opts["no_images"] = True; i += 1
        elif a == "--no-links":
            opts["no_links"] = True; i += 1
        elif a == "--with-links-summary":
            opts["with_links_summary"] = True; i += 1
        elif a == "--with-images-summary":
            opts["with_images_summary"] = True; i += 1
        elif a == "--budget" and i + 1 < len(args):
            search_opts["budget"] = args[i + 1]; i += 2
        elif a == "--engine" and i + 1 < len(args):
            search_opts["engine"] = args[i + 1]; i += 2
        elif a == "--type" and i + 1 < len(args):
            search_opts["search_type"] = args[i + 1]; i += 2
        else:
            i += 1

    if mode == "read":
        do_read(input_val, **opts)
    elif mode == "search":
        do_search(input_val, **search_opts, **opts)


if __name__ == "__main__":
    main()
