#!/usr/bin/env python3
"""cobalt-dl: download videos/audio from 20+ platforms via cobalt API.

Usage:
    cobalt-dl <url>                     # 1080p video
    cobalt-dl <url> -q 2160             # 4K
    cobalt-dl <url> --audio             # audio only MP3 320k
    cobalt-dl <url> --audio -f opus     # audio as opus
    cobalt-dl <url> -o ~/Downloads      # output dir
    cobalt-dl <url> --subs en,zh        # with subtitles

No config needed. Fetches instance list from cobalt.directory,
tries up to 10 instances, skips auth-required ones automatically.
"""

import json
import subprocess
import sys
from pathlib import Path

DIRECTORY_API = "https://cobalt.directory/api/working?type=api"

HARDCODED_FALLBACKS = [
    "https://cobaltapi.cjs.nz",
    "https://api.qwkuns.me",
    "https://cobaltapi.squair.xyz",
    "https://api.dl.woof.monster",
    "https://api.cobalt.liubquanti.click",
    "https://api.kektube.com",
]

HAS_REQUESTS = False
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    pass


def http_get(url, timeout=10):
    if HAS_REQUESTS:
        return requests.get(url, timeout=timeout).json()
    r = subprocess.run(
        ["curl", "-s", "--max-time", str(timeout), url],
        capture_output=True, text=True,
    )
    return json.loads(r.stdout)


def http_post(url, payload, timeout=30):
    if HAS_REQUESTS:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        return requests.post(
            url, json=payload, headers=headers, timeout=timeout
        ).json()
    r = subprocess.run(
        ["curl", "-s", "--max-time", str(timeout),
         "-X", "POST", url,
         "-H", "Accept: application/json",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload)],
        capture_output=True, text=True,
    )
    return json.loads(r.stdout)


def download_file(url, filepath):
    if HAS_REQUESTS:
        with requests.get(url, stream=True, timeout=120) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            done = 0
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        pct = done * 100 // total
                        bar = "#" * (pct // 2) + "-" * (50 - pct // 2)
                        print(f"\r  [{bar}] {pct}%", end="", flush=True)
            if total:
                print()
    else:
        subprocess.run(
            ["curl", "-L", "--progress-bar", "-o", str(filepath), url],
            check=True,
        )


def fetch_instances():
    """Fetch from cobalt.directory, return unique URL list."""
    try:
        data = http_get(DIRECTORY_API, timeout=10)
        services_map = data.get("data", {})
        seen = set()
        result = []
        for instances in services_map.values():
            for inst in instances:
                if inst not in seen:
                    seen.add(inst)
                    result.append(inst)
        return result if result else HARDCODED_FALLBACKS
    except Exception:
        return HARDCODED_FALLBACKS


def do_download(url, quality=None, output=None, audio=False,
                mute=False, fmt=None, bitrate=None, subs=None,
                codec=None, tiktok_audio=False):
    out_dir = Path(output) if output else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {"url": url}
    if audio:
        payload["downloadMode"] = "audio"
        payload["audioFormat"] = fmt or "mp3"
        payload["audioBitrate"] = bitrate or "320"
    else:
        payload["videoQuality"] = quality or "1080"
        if mute:
            payload["downloadMode"] = "mute"
    if subs:
        payload["subtitleLang"] = subs
    if codec:
        payload["youtubeVideoCodec"] = codec
    if tiktok_audio:
        payload["tiktokFullAudio"] = True

    instances = fetch_instances()
    resp = None
    for i, inst in enumerate(instances):
        if i >= 10:
            break
        try:
            resp = http_post(inst, payload, timeout=30)
            status = resp.get("status", "error")
            if status != "error":
                break
            err_code = resp.get("error", {}).get("code", "")
            if "auth" in err_code:
                print(f"  {inst} -> auth required, next...")
                resp = None
                continue
            break
        except Exception as e:
            print(f"  {inst} -> {e}")
            resp = None

    if resp is None:
        print("All instances failed.")
        sys.exit(1)

    status = resp.get("status", "error")

    if status in ("tunnel", "redirect"):
        fname = resp.get("filename", "download.mp4")
        fpath = out_dir / fname
        print(f"Downloading: {fname}")
        download_file(resp["url"], fpath)
        print(f"Saved: {fpath}")

    elif status == "picker":
        items = resp.get("picker", [])
        print(f"Found {len(items)} items")
        a_url, a_name = resp.get("audio"), resp.get("audioFilename")
        if a_url and a_name:
            print(f"Downloading audio: {a_name}")
            download_file(a_url, out_dir / a_name)
        for i, item in enumerate(items, 1):
            ext = "jpg" if item.get("type") == "photo" else "mp4"
            fname = f"item_{i}.{ext}"
            print(f"  [{i}/{len(items)}] {fname}")
            download_file(item["url"], out_dir / fname)
        print(f"Saved {len(items)} items to {out_dir}")

    elif status == "error":
        err = resp.get("error", {})
        print(f"Error: {err.get('code', 'unknown')}")
        sys.exit(1)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    url = args[0]
    kwargs = {}
    i = 1
    while i < len(args):
        a = args[i]
        if a in ("-q", "--quality") and i + 1 < len(args):
            kwargs["quality"] = args[i + 1]; i += 2
        elif a in ("-o", "--output") and i + 1 < len(args):
            kwargs["output"] = args[i + 1]; i += 2
        elif a == "--audio":
            kwargs["audio"] = True; i += 1
        elif a == "--mute":
            kwargs["mute"] = True; i += 1
        elif a in ("-f", "--format") and i + 1 < len(args):
            kwargs["fmt"] = args[i + 1]; i += 2
        elif a in ("-b", "--bitrate") and i + 1 < len(args):
            kwargs["bitrate"] = args[i + 1]; i += 2
        elif a == "--subs" and i + 1 < len(args):
            kwargs["subs"] = args[i + 1]; i += 2
        elif a == "--codec" and i + 1 < len(args):
            kwargs["codec"] = args[i + 1]; i += 2
        elif a == "--tiktok-full-audio":
            kwargs["tiktok_audio"] = True; i += 1
        else:
            i += 1

    do_download(url, **kwargs)


if __name__ == "__main__":
    main()
