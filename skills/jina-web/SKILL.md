---
name: jina-web
description: >
  Read web pages and search the internet using Jina AI Reader & Search APIs.
  Two modes: (1) READ - fetch any URL and convert to clean markdown/text,
  (2) SEARCH - web search with results returned as markdown.
  Supports proxy, CSS selectors, screenshots, caching control, and more.
  Auto-detects python/curl+jq/powershell backend.
  Use when: user wants to read a webpage, fetch URL content, scrape a site,
  search the web, or get clean text from a URL.
  Triggers: "read this page", "fetch URL", "scrape website", "search the web",
  "jina search", "jina read", "读取网页", "抓取页面", "搜索网页",
  "网页内容", "获取链接内容".
---

# Jina Web Skill

Read web pages and search the internet via [Jina AI](https://jina.ai) Reader & Search APIs.

## Scripts

- Python: `scripts/jina-web.py`
- Shell:  `scripts/jina-web.sh` (curl)
- PowerShell: `scripts/jina-web.ps1` (Windows)

## Authentication

Set `JINA_API_KEY` env var for higher rate limits (optional, ~20 req/min without).

## Quick Reference

```bash
# Read a web page → markdown
python3 scripts/jina-web.py read "https://example.com"

# Read as plain text
python3 scripts/jina-web.py read "https://example.com" --format text

# Read with CSS selector, no images
python3 scripts/jina-web.py read "https://example.com" --target "article" --no-images

# Remove nav/footer, wait for JS content
python3 scripts/jina-web.py read "https://example.com" --remove "nav,footer" --wait-for ".content"

# Read as JSON (includes title, url, publishedTime, token usage)
python3 scripts/jina-web.py read "https://example.com" --json

# Take screenshot
python3 scripts/jina-web.py read "https://example.com" --format screenshot

# Search the web
python3 scripts/jina-web.py search "Claude AI latest features"

# Search with JSON output
python3 scripts/jina-web.py search "AI news 2026" --json

# News search with token budget
python3 scripts/jina-web.py search "AI regulation" --type news --budget 5000

# Image search
python3 scripts/jina-web.py search "cute cats" --type images

# Use Bing engine
python3 scripts/jina-web.py search "rust tutorial" --engine bing
```

Shell version (identical interface):
```bash
scripts/jina-web.sh read "https://example.com"
scripts/jina-web.sh search "Claude AI" --json
```

PowerShell version (Windows):
```powershell
pwsh scripts/jina-web.ps1 read "https://example.com"
pwsh scripts/jina-web.ps1 search "Claude AI" --json
```

## Options

### Common Options

| Flag | Description | Default |
|------|-------------|---------|
| `--json` | Return structured JSON with metadata | off |
| `--no-cache` | Skip cache, fetch fresh | off |
| `--proxy URL` | Use HTTP proxy | none |
| `--format FMT` | markdown/text/html/screenshot/pageshot | markdown |
| `--timeout SEC` | Request timeout (max 180) | 30 |

### Read Options

| Flag | Description | Default |
|------|-------------|---------|
| `--target SEL` | Target CSS selector(s), comma-separated | none |
| `--wait-for SEL` | Wait for CSS selector(s) before extraction | none |
| `--remove SEL` | Remove elements matching selector(s) | none |
| `--no-images` | Strip all images from output | off |
| `--no-links` | Strip all links from output | off |
| `--with-links-summary` | Append link summary at end | off |
| `--with-images-summary` | Append image summary at end | off |

### Search Options

| Flag | Description | Default |
|------|-------------|---------|
| `--budget N` | Token budget for results | none |
| `--engine ENG` | google/bing/reader | google |
| `--type TYPE` | web/images/news | web |

## How It Works

1. **Read** (`r.jina.ai`): Renders page (including JS), extracts content → clean markdown
2. **Search** (`s.jina.ai`): Searches web, fetches top results → markdown with content

## Response Format

**Plain text** (default): clean markdown directly.

**JSON** (`--json`): structured response with metadata.
- Read: `{"code":200,"data":{"text":"...","title":"...","url":"...","publishedTime":"...","usage":{"tokens":N}}}`
- Search: `{"code":200,"data":[{"title":"...","url":"...","description":"...","content":"..."},...]}`

## Rate Limits

- Without API key: ~20 req/min
- With key: higher limits based on plan
- Free key: https://jina.ai/reader
