#!/usr/bin/env bash
# jina-web: read web pages and search the internet via Jina AI APIs
# Requires: curl
#
# Usage:
#   jina-web read <url>                          # markdown
#   jina-web read <url> --format text            # plain text
#   jina-web read <url> --target "article"       # CSS selector
#   jina-web search "query"                      # web search
#   jina-web search "query" --type news --json   # news, JSON
#
# Env: JINA_API_KEY (optional, for higher rate limits)

set -euo pipefail

READ_BASE="https://r.jina.ai"
SEARCH_BASE="https://s.jina.ai"

usage() {
  cat << 'EOF'
jina-web: read web pages and search the internet via Jina AI APIs

Usage:
    jina-web read <url>                          # markdown
    jina-web read <url> --format text            # plain text
    jina-web read <url> --target "article"       # CSS selector
    jina-web read <url> --no-images --json       # JSON, no images
    jina-web search "query"                      # web search
    jina-web search "query" --type news --json   # news search, JSON
EOF
  exit 0
}

die() { echo "Error: $*" >&2; exit 1; }
info() { echo "[jina] $*" >&2; }

command -v curl >/dev/null 2>&1 || die "curl is required"

[[ $# -lt 1 ]] && usage

MODE="$1"; shift
case "$MODE" in
  read|search) ;;
  -h|--help|help) usage ;;
  *) die "Unknown command: $MODE. Use 'read' or 'search'." ;;
esac

[[ $# -lt 1 ]] && die "Missing argument for '$MODE'."
INPUT="$1"; shift

JSON_OUTPUT=false NO_CACHE=false PROXY="" FORMAT="markdown" TIMEOUT=30
TARGET="" WAIT_FOR="" REMOVE=""
NO_IMAGES=false NO_LINKS=false
WITH_LINKS_SUMMARY=false WITH_IMAGES_SUMMARY=false
TOKEN_BUDGET="" ENGINE="" SEARCH_TYPE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_OUTPUT=true ;;
    --no-cache) NO_CACHE=true ;;
    --proxy) PROXY="$2"; shift ;;
    --format) FORMAT="$2"; shift ;;
    --timeout) TIMEOUT="$2"; shift ;;
    --target) TARGET="$2"; shift ;;
    --wait-for) WAIT_FOR="$2"; shift ;;
    --remove) REMOVE="$2"; shift ;;
    --no-images) NO_IMAGES=true ;;
    --no-links) NO_LINKS=true ;;
    --with-links-summary) WITH_LINKS_SUMMARY=true ;;
    --with-images-summary) WITH_IMAGES_SUMMARY=true ;;
    --budget) TOKEN_BUDGET="$2"; shift ;;
    --engine) ENGINE="$2"; shift ;;
    --type) SEARCH_TYPE="$2"; shift ;;
    -h|--help) usage ;;
    *) ;;
  esac
  shift
done

HEADERS=()

[[ -n "${JINA_API_KEY:-}" ]] && HEADERS+=(-H "Authorization: Bearer $JINA_API_KEY")

if [[ "$JSON_OUTPUT" == "true" ]]; then
  HEADERS+=(-H "Accept: application/json")
else
  HEADERS+=(-H "Accept: text/plain")
fi

case "$FORMAT" in
  markdown|text|html|screenshot|pageshot)
    HEADERS+=(-H "X-Respond-With: $FORMAT") ;;
  *) die "Unknown format: $FORMAT" ;;
esac

[[ "$NO_CACHE" == "true" ]] && HEADERS+=(-H "X-No-Cache: true")
[[ -n "$PROXY" ]] && HEADERS+=(-H "X-Proxy-Url: $PROXY")

if [[ "$MODE" == "read" ]]; then
  [[ -n "$TARGET" ]] && HEADERS+=(-H "X-Target-Selector: $TARGET")
  [[ -n "$WAIT_FOR" ]] && HEADERS+=(-H "X-Wait-For-Selector: $WAIT_FOR")
  [[ -n "$REMOVE" ]] && HEADERS+=(-H "X-Remove-Selector: $REMOVE")
  [[ "$NO_IMAGES" == "true" ]] && HEADERS+=(-H "X-Retain-Images: none")
  [[ "$NO_LINKS" == "true" ]] && HEADERS+=(-H "X-Retain-Links: none")
  [[ "$WITH_LINKS_SUMMARY" == "true" ]] && HEADERS+=(-H "X-With-Links-Summary: true")
  [[ "$WITH_IMAGES_SUMMARY" == "true" ]] && HEADERS+=(-H "X-With-Images-Summary: true")
fi

if [[ "$MODE" == "read" ]]; then
  URL="${READ_BASE}/${INPUT}"
  info "Reading: $INPUT"
elif [[ "$MODE" == "search" ]]; then
  ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$INPUT'))" 2>/dev/null \
    || printf '%s' "$INPUT" | sed 's/ /+/g')
  URL="${SEARCH_BASE}/search?q=${ENCODED}"
  [[ -n "$ENGINE" ]] && URL="${URL}&engine=${ENGINE}"
  [[ -n "$SEARCH_TYPE" ]] && URL="${URL}&type=${SEARCH_TYPE}"
  [[ -n "$TOKEN_BUDGET" ]] && URL="${URL}&tokenBudget=${TOKEN_BUDGET}"
  info "Searching: $INPUT"
fi

RESPONSE=$(curl -sS --max-time "$TIMEOUT" "${HEADERS[@]}" "$URL" 2>&1) \
  || die "Request failed. Check network connection."

[[ -z "$RESPONSE" ]] && die "Empty response received"

echo "$RESPONSE"
