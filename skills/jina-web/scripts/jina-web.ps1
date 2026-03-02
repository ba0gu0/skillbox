<#
.SYNOPSIS
    jina-web: read web pages and search the internet via Jina AI APIs

.DESCRIPTION
    Two modes: read (fetch URL → markdown) and search (web search → markdown).
    Env: JINA_API_KEY (optional, for higher rate limits)

.EXAMPLE
    .\jina-web.ps1 read "https://example.com"
    .\jina-web.ps1 read "https://example.com" --format text --target "article"
    .\jina-web.ps1 search "Claude AI" --json
    .\jina-web.ps1 search "AI news" --type news --budget 5000
#>

param()

$READ_BASE = "https://r.jina.ai"
$SEARCH_BASE = "https://s.jina.ai"

function Show-Usage {
    Write-Host @"
jina-web: read web pages and search the internet via Jina AI APIs

Usage:
    .\jina-web.ps1 read <url>                          # markdown
    .\jina-web.ps1 read <url> --format text            # plain text
    .\jina-web.ps1 read <url> --target "article"       # CSS selector
    .\jina-web.ps1 read <url> --no-images --json       # JSON, no images
    .\jina-web.ps1 search "query"                      # web search
    .\jina-web.ps1 search "query" --type news --json   # news, JSON
"@
    exit 0
}

function Do-Request {
    param(
        [string]$Mode,
        [string]$InputUrl,
        [bool]$JsonOutput = $false,
        [string]$Format = "markdown",
        [bool]$NoCache = $false,
        [string]$Proxy = "",
        [int]$Timeout = 30,
        [string]$Target = "",
        [string]$WaitFor = "",
        [string]$Remove = "",
        [bool]$NoImages = $false,
        [bool]$NoLinks = $false,
        [bool]$WithLinksSummary = $false,
        [bool]$WithImagesSummary = $false,
        [string]$Budget = "",
        [string]$Engine = "",
        [string]$SearchType = ""
    )

    $headers = @{}

    $apiKey = $env:JINA_API_KEY
    if ($apiKey) {
        $headers["Authorization"] = "Bearer $apiKey"
    }

    if ($JsonOutput) {
        $headers["Accept"] = "application/json"
    } else {
        $headers["Accept"] = "text/plain"
    }

    $headers["X-Respond-With"] = $Format

    if ($NoCache) { $headers["X-No-Cache"] = "true" }
    if ($Proxy) { $headers["X-Proxy-Url"] = $Proxy }

    if ($Mode -eq "read") {
        if ($Target) { $headers["X-Target-Selector"] = $Target }
        if ($WaitFor) { $headers["X-Wait-For-Selector"] = $WaitFor }
        if ($Remove) { $headers["X-Remove-Selector"] = $Remove }
        if ($NoImages) { $headers["X-Retain-Images"] = "none" }
        if ($NoLinks) { $headers["X-Retain-Links"] = "none" }
        if ($WithLinksSummary) { $headers["X-With-Links-Summary"] = "true" }
        if ($WithImagesSummary) { $headers["X-With-Images-Summary"] = "true" }
    }

    if ($Mode -eq "read") {
        $url = "$READ_BASE/$InputUrl"
        Write-Host "[jina] Reading: $InputUrl" -ForegroundColor Cyan
    }
    elseif ($Mode -eq "search") {
        $encoded = [System.Uri]::EscapeDataString($InputUrl)
        $url = "$SEARCH_BASE/search?q=$encoded"
        if ($Engine) { $url += "&engine=$Engine" }
        if ($SearchType) { $url += "&type=$SearchType" }
        if ($Budget) { $url += "&tokenBudget=$Budget" }
        Write-Host "[jina] Searching: $InputUrl" -ForegroundColor Cyan
    }

    try {
        $resp = Invoke-WebRequest -Uri $url -Headers $headers `
            -TimeoutSec $Timeout -ErrorAction Stop
        Write-Output $resp.Content
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# --- Argument parsing ---
$scriptArgs = $args
if ($scriptArgs.Count -eq 0 -or $scriptArgs[0] -in @("-h", "--help", "help")) {
    Show-Usage
}

$mode = $scriptArgs[0]
if ($mode -notin @("read", "search")) {
    Write-Host "Error: Unknown command '$mode'. Use 'read' or 'search'."
    exit 1
}

if ($scriptArgs.Count -lt 2) {
    Write-Host "Error: Missing argument for '$mode'."
    exit 1
}

$inputVal = $scriptArgs[1]
$reqParams = @{
    Mode = $mode
    InputUrl = $inputVal
}

$i = 2
while ($i -lt $scriptArgs.Count) {
    switch ($scriptArgs[$i]) {
        "--json" { $reqParams["JsonOutput"] = $true; $i++ }
        "--no-cache" { $reqParams["NoCache"] = $true; $i++ }
        "--proxy" { $reqParams["Proxy"] = $scriptArgs[$i + 1]; $i += 2 }
        "--format" { $reqParams["Format"] = $scriptArgs[$i + 1]; $i += 2 }
        "--timeout" { $reqParams["Timeout"] = [int]$scriptArgs[$i + 1]; $i += 2 }
        "--target" { $reqParams["Target"] = $scriptArgs[$i + 1]; $i += 2 }
        "--wait-for" { $reqParams["WaitFor"] = $scriptArgs[$i + 1]; $i += 2 }
        "--remove" { $reqParams["Remove"] = $scriptArgs[$i + 1]; $i += 2 }
        "--no-images" { $reqParams["NoImages"] = $true; $i++ }
        "--no-links" { $reqParams["NoLinks"] = $true; $i++ }
        "--with-links-summary" { $reqParams["WithLinksSummary"] = $true; $i++ }
        "--with-images-summary" { $reqParams["WithImagesSummary"] = $true; $i++ }
        "--budget" { $reqParams["Budget"] = $scriptArgs[$i + 1]; $i += 2 }
        "--engine" { $reqParams["Engine"] = $scriptArgs[$i + 1]; $i += 2 }
        "--type" { $reqParams["SearchType"] = $scriptArgs[$i + 1]; $i += 2 }
        default { $i++ }
    }
}

Do-Request @reqParams
