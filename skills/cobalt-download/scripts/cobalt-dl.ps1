<#
.SYNOPSIS
    cobalt-dl: download videos/audio from 20+ platforms via cobalt API

.DESCRIPTION
    No config needed. Fetches instance list from cobalt.directory,
    tries up to 10 instances, skips auth-required ones automatically.

.EXAMPLE
    .\cobalt-dl.ps1 "<url>"                     # 1080p video
    .\cobalt-dl.ps1 "<url>" -q 2160             # 4K
    .\cobalt-dl.ps1 "<url>" --audio             # audio only MP3 320k
    .\cobalt-dl.ps1 "<url>" --audio -f opus     # audio as opus
    .\cobalt-dl.ps1 "<url>" -o ~/Downloads      # output dir
    .\cobalt-dl.ps1 "<url>" --subs en,zh        # with subtitles
#>

param()

$DIRECTORY_API = "https://cobalt.directory/api/working?type=api"

$HARDCODED_FALLBACKS = @(
    "https://cobaltapi.cjs.nz"
    "https://api.qwkuns.me"
    "https://cobaltapi.squair.xyz"
    "https://api.dl.woof.monster"
    "https://api.cobalt.liubquanti.click"
    "https://api.kektube.com"
)

function Fetch-Instances {
    try {
        $resp = Invoke-RestMethod -Uri $DIRECTORY_API `
            -TimeoutSec 10 -ErrorAction Stop
        $seen = @{}
        $result = @()
        foreach ($key in $resp.data.PSObject.Properties.Name) {
            foreach ($inst in $resp.data.$key) {
                if (-not $seen.ContainsKey($inst)) {
                    $seen[$inst] = $true
                    $result += $inst
                }
            }
        }
        if ($result.Count -gt 0) { return $result }
        return $HARDCODED_FALLBACKS
    }
    catch {
        return $HARDCODED_FALLBACKS
    }
}

function Download-File {
    param(
        [string]$Url,
        [string]$FilePath
    )
    $ProgressPreference = 'Continue'
    Invoke-WebRequest -Uri $Url -OutFile $FilePath `
        -TimeoutSec 120 -ErrorAction Stop
}

function Do-Download {
    param(
        [string]$Url,
        [string]$Quality = "1080",
        [string]$OutputDir = ".",
        [switch]$Audio,
        [switch]$Mute,
        [string]$Format = "mp3",
        [string]$Bitrate = "320",
        [string]$Subs = "",
        [string]$Codec = "",
        [switch]$TiktokAudio
    )

    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    }

    $payload = @{ url = $Url }
    if ($Audio) {
        $payload["downloadMode"] = "audio"
        $payload["audioFormat"] = $Format
        $payload["audioBitrate"] = $Bitrate
    }
    else {
        $payload["videoQuality"] = $Quality
        if ($Mute) { $payload["downloadMode"] = "mute" }
    }
    if ($Subs) { $payload["subtitleLang"] = $Subs }
    if ($Codec) { $payload["youtubeVideoCodec"] = $Codec }
    if ($TiktokAudio) { $payload["tiktokFullAudio"] = $true }

    $body = $payload | ConvertTo-Json -Compress
    $headers = @{
        "Accept"       = "application/json"
        "Content-Type" = "application/json"
    }

    $instances = Fetch-Instances
    $resp = $null
    $tried = 0

    foreach ($inst in $instances) {
        if ($tried -ge 10) { break }
        $tried++
        try {
            $resp = Invoke-RestMethod -Uri $inst -Method Post `
                -Body $body -Headers $headers `
                -TimeoutSec 30 -ErrorAction Stop
            $status = $resp.status
            if ($status -and $status -ne "error") { break }
            $errCode = ""
            if ($resp.error -and $resp.error.code) {
                $errCode = $resp.error.code
            }
            if ($errCode -match "auth") {
                Write-Host "  $inst -> auth required, next..."
                $resp = $null
                continue
            }
            break
        }
        catch {
            Write-Host "  $inst -> $($_.Exception.Message)"
            $resp = $null
        }
    }

    if (-not $resp) {
        Write-Host "All instances failed."
        exit 1
    }

    $status = if ($resp.status) { $resp.status } else { "error" }

    switch ($status) {
        { $_ -in "tunnel", "redirect" } {
            $fname = if ($resp.filename) { $resp.filename } else { "download.mp4" }
            $fpath = Join-Path $OutputDir $fname
            Write-Host "Downloading: $fname"
            Download-File -Url $resp.url -FilePath $fpath
            Write-Host "Saved: $fpath"
        }
        "picker" {
            $items = $resp.picker
            Write-Host "Found $($items.Count) items"
            if ($resp.audio -and $resp.audioFilename) {
                Write-Host "Downloading audio: $($resp.audioFilename)"
                $aPath = Join-Path $OutputDir $resp.audioFilename
                Download-File -Url $resp.audio -FilePath $aPath
            }
            for ($i = 0; $i -lt $items.Count; $i++) {
                $ext = if ($items[$i].type -eq "photo") { "jpg" } else { "mp4" }
                $fn = "item_$($i + 1).$ext"
                Write-Host "  [$($i + 1)/$($items.Count)] $fn"
                $fp = Join-Path $OutputDir $fn
                Download-File -Url $items[$i].url -FilePath $fp
            }
            Write-Host "Saved $($items.Count) items to $OutputDir"
        }
        "error" {
            $ec = if ($resp.error -and $resp.error.code) {
                $resp.error.code
            } else { "unknown" }
            Write-Host "Error: $ec"
            exit 1
        }
    }
}

# --- Argument parsing ---
$scriptArgs = $args
if ($scriptArgs.Count -eq 0 -or $scriptArgs[0] -in @("-h", "--help")) {
    Write-Host @"
cobalt-dl: download videos/audio from 20+ platforms via cobalt API

Usage:
    .\cobalt-dl.ps1 <url>                     # 1080p video
    .\cobalt-dl.ps1 <url> -q 2160             # 4K
    .\cobalt-dl.ps1 <url> --audio             # audio only MP3 320k
    .\cobalt-dl.ps1 <url> --audio -f opus     # audio as opus
    .\cobalt-dl.ps1 <url> -o ~/Downloads      # output dir
    .\cobalt-dl.ps1 <url> --subs en,zh        # with subtitles
"@
    exit 0
}

$targetUrl = $scriptArgs[0]
$dlParams = @{ Url = $targetUrl }
$i = 1
while ($i -lt $scriptArgs.Count) {
    switch ($scriptArgs[$i]) {
        { $_ -in "-q", "--quality" } {
            $dlParams["Quality"] = $scriptArgs[$i + 1]; $i += 2
        }
        { $_ -in "-o", "--output" } {
            $dlParams["OutputDir"] = $scriptArgs[$i + 1]; $i += 2
        }
        "--audio" { $dlParams["Audio"] = [switch]$true; $i++ }
        "--mute" { $dlParams["Mute"] = [switch]$true; $i++ }
        { $_ -in "-f", "--format" } {
            $dlParams["Format"] = $scriptArgs[$i + 1]; $i += 2
        }
        { $_ -in "-b", "--bitrate" } {
            $dlParams["Bitrate"] = $scriptArgs[$i + 1]; $i += 2
        }
        "--subs" {
            $dlParams["Subs"] = $scriptArgs[$i + 1]; $i += 2
        }
        "--codec" {
            $dlParams["Codec"] = $scriptArgs[$i + 1]; $i += 2
        }
        "--tiktok-full-audio" {
            $dlParams["TiktokAudio"] = [switch]$true; $i++
        }
        default { $i++ }
    }
}

Do-Download @dlParams
