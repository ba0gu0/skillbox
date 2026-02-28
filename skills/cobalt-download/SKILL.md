---
name: cobalt-download
description: >
  Download videos and audio from 20+ platforms (YouTube, TikTok, Instagram,
  Twitter/X, Reddit, Bilibili, Pinterest, SoundCloud, Vimeo, etc.) using
  the cobalt API. Auto-detects python/curl+jq/powershell backend.
  Use when: user wants to download a video, extract audio from a video,
  save a clip, or rip media from a social platform URL.
  Triggers: "download video", "下载视频", "save video", "rip audio",
  "extract audio", "download from youtube", "download from tiktok",
  "download from twitter", "下载", "保存视频", "提取音频".
---

# Cobalt Download Skill

Download videos and audio from 20+ platforms via [cobalt](https://cobalt.tools) API.
Zero-config — each run fetches the latest instance list from
[cobalt.directory](https://cobalt.directory/), tries up to 10 instances,
skips auth-required ones automatically.

## Scripts

- Python: `scripts/cobalt-dl.py`
- Shell:  `scripts/cobalt-dl.sh` (curl + jq)
- PowerShell: `scripts/cobalt-dl.ps1` (Windows)

## Quick Reference

```bash
# Download video (default 1080p)
python3 scripts/cobalt-dl.py "<url>"

# 4K video
python3 scripts/cobalt-dl.py "<url>" -q 2160

# Audio only (MP3 320kbps)
python3 scripts/cobalt-dl.py "<url>" --audio

# Audio as opus
python3 scripts/cobalt-dl.py "<url>" --audio -f opus

# Output directory
python3 scripts/cobalt-dl.py "<url>" -o ~/Downloads

# With subtitles
python3 scripts/cobalt-dl.py "<url>" --subs en,zh
```

Shell version (identical interface):
```bash
scripts/cobalt-dl.sh "<url>"
scripts/cobalt-dl.sh "<url>" --audio
```

PowerShell version (Windows):
```powershell
pwsh scripts/cobalt-dl.ps1 "<url>"
pwsh scripts/cobalt-dl.ps1 "<url>" --audio
pwsh scripts/cobalt-dl.ps1 "<url>" -q 2160 -o C:\Downloads
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-q`, `--quality` | Video quality (144-4320) | 1080 |
| `-o`, `--output` | Output directory | current dir |
| `--audio` | Audio only mode | off |
| `-f`, `--format` | Audio format (mp3/opus/ogg/wav) | mp3 |
| `-b`, `--bitrate` | Audio bitrate (64-320) | 320 |
| `--mute` | Video without audio | off |
| `--subs` | Subtitle languages (ISO 639-1) | none |
| `--codec` | YouTube codec (h264/av1/vp9) | h264 |
| `--tiktok-full-audio` | TikTok original sound | off |

## Supported Platforms (22)

bilibili, bluesky, dailymotion, facebook, instagram, loom, ok,
pinterest, newgrounds, reddit, rutube, snapchat, soundcloud,
streamable, tiktok, tumblr, twitch clips, twitter/X, vimeo, vk,
xiaohongshu, youtube

## How It Works

1. Fetch instance list from `cobalt.directory/api/working?type=api`
2. If API unreachable, fall back to hardcoded instance list
3. POST the URL to the first instance
4. If auth required → skip to next instance (up to 10 tries)
5. On success: download via requests (Python) / curl (Shell) / Invoke-WebRequest (PowerShell)

## Response Types

- `tunnel` / `redirect` → single file, download via `url` + `filename`
- `picker` → multiple items (e.g., Instagram carousel), iterate `picker[]`
- `error` → check `error.code` for reason
