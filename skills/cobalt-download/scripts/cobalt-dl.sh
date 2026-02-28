#!/usr/bin/env bash
# cobalt-dl: download videos/audio from 20+ platforms via cobalt API
# Requires: curl, jq
#
# Usage:
#   cobalt-dl <url>                        # 1080p video
#   cobalt-dl <url> -q 2160               # 4K
#   cobalt-dl <url> --audio               # audio only MP3 320k
#   cobalt-dl <url> -o ~/Downloads        # output dir
#   cobalt-dl <url> --subs en,zh          # with subtitles
#
# No config needed. Fetches instance list from cobalt.directory,
# tries up to 10 instances, skips auth-required ones automatically.

set -euo pipefail

DIRECTORY_API="https://cobalt.directory/api/working?type=api"

HARDCODED_FALLBACKS=(
  "https://cobaltapi.cjs.nz"
  "https://api.qwkuns.me"
  "https://cobaltapi.squair.xyz"
  "https://api.dl.woof.monster"
  "https://api.cobalt.liubquanti.click"
  "https://api.kektube.com"
)

fetch_instances() {
  local result
  result=$(curl -s --max-time 10 "$DIRECTORY_API" 2>/dev/null \
    | jq -r '[.data | to_entries[] | .value[]] | unique[]' \
    2>/dev/null) || true

  if [ -n "$result" ]; then
    echo "$result"
  else
    printf '%s\n' "${HARDCODED_FALLBACKS[@]}"
  fi
}

do_download() {
  local url="$1"; shift
  local quality="1080" output_dir="." audio=false mute=false
  local audio_fmt="mp3" audio_br="320" subs="" codec=""
  local tiktok_audio=false

  while [ $# -gt 0 ]; do
    case "$1" in
      -q|--quality) quality="$2"; shift 2 ;;
      -o|--output)  output_dir="$2"; shift 2 ;;
      --audio) audio=true; shift ;;
      --mute)  mute=true; shift ;;
      -f|--format)  audio_fmt="$2"; shift 2 ;;
      -b|--bitrate) audio_br="$2"; shift 2 ;;
      --subs)  subs="$2"; shift 2 ;;
      --codec) codec="$2"; shift 2 ;;
      --tiktok-full-audio) tiktok_audio=true; shift ;;
      *) shift ;;
    esac
  done

  mkdir -p "$output_dir"

  local payload
  payload=$(jq -n --arg u "$url" '{url:$u}')
  if $audio; then
    payload=$(echo "$payload" | jq \
      --arg f "$audio_fmt" --arg b "$audio_br" \
      '. + {downloadMode:"audio",audioFormat:$f,audioBitrate:$b}')
  else
    payload=$(echo "$payload" | jq \
      --arg q "$quality" '. + {videoQuality:$q}')
    $mute && payload=$(echo "$payload" | jq \
      '. + {downloadMode:"mute"}')
  fi
  [ -n "$subs" ] && payload=$(echo "$payload" | jq \
    --arg s "$subs" '. + {subtitleLang:$s}')
  [ -n "$codec" ] && payload=$(echo "$payload" | jq \
    --arg c "$codec" '. + {youtubeVideoCodec:$c}')
  $tiktok_audio && payload=$(echo "$payload" | jq \
    '. + {tiktokFullAudio:true}')

  local instances
  instances=$(fetch_instances)

  local resp="" status="" tried=0
  while IFS= read -r inst; do
    [ -z "$inst" ] && continue
    tried=$((tried + 1))
    [ "$tried" -gt 10 ] && break

    resp=$(curl -s --max-time 30 -X POST "$inst" \
      -H "Accept: application/json" \
      -H "Content-Type: application/json" \
      -d "$payload" 2>/dev/null) || resp='{"status":"error"}'

    status=$(echo "$resp" | jq -r '.status // "error"')
    if [ "$status" != "error" ]; then
      break
    fi

    local ec
    ec=$(echo "$resp" | jq -r '.error.code // ""')
    if [[ "$ec" == *"auth"* ]]; then
      echo "  $inst -> auth required, next..." >&2
      continue
    fi
    break
  done <<< "$instances"

  case "$status" in
    tunnel|redirect)
      local dl_url fname fpath
      dl_url=$(echo "$resp" | jq -r '.url')
      fname=$(echo "$resp" | jq -r '.filename // "download.mp4"')
      fpath="$output_dir/$fname"
      echo "Downloading: $fname"
      curl -L --progress-bar -o "$fpath" "$dl_url"
      echo "Saved: $fpath"
      ;;
    picker)
      local cnt
      cnt=$(echo "$resp" | jq '.picker | length')
      echo "Found $cnt items"
      local a_url a_name
      a_url=$(echo "$resp" | jq -r '.audio // empty')
      a_name=$(echo "$resp" | jq -r '.audioFilename // empty')
      if [ -n "$a_url" ] && [ -n "$a_name" ]; then
        echo "Downloading audio: $a_name"
        curl -sL -o "$output_dir/$a_name" "$a_url"
      fi
      for i in $(seq 0 $((cnt - 1))); do
        local iu it ext fn
        iu=$(echo "$resp" | jq -r ".picker[$i].url")
        it=$(echo "$resp" | jq -r ".picker[$i].type // \"video\"")
        ext="mp4"; [ "$it" = "photo" ] && ext="jpg"
        fn="item_$((i+1)).$ext"
        echo "  [$((i+1))/$cnt] $fn"
        curl -sL -o "$output_dir/$fn" "$iu"
      done
      echo "Saved $cnt items to $output_dir"
      ;;
    error)
      echo "Error: $(echo "$resp" | jq -r '.error.code // "unknown"')"
      exit 1
      ;;
    *)
      echo "All instances failed."
      exit 1
      ;;
  esac
}

case "${1:-}" in
  -h|--help|"")
    cat << 'EOF'
cobalt-dl: download videos/audio from 20+ platforms via cobalt API

Usage:
    cobalt-dl <url>                     # 1080p video
    cobalt-dl <url> -q 2160             # 4K
    cobalt-dl <url> --audio             # audio only MP3 320k
    cobalt-dl <url> --audio -f opus     # audio as opus
    cobalt-dl <url> -o ~/Downloads      # output dir
    cobalt-dl <url> --subs en,zh        # with subtitles
EOF
    ;;
  *) do_download "$@" ;;
esac
