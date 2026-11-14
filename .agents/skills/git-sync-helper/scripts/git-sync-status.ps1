param(
    [string]$Remote = "origin",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "== $Title =="
}

if (-not (Test-Path ".git")) {
    git rev-parse --show-toplevel | Out-Null
}

$insideWorkTree = git rev-parse --is-inside-work-tree
if ($insideWorkTree -ne "true") {
    throw "This directory is not inside a Git work tree."
}

$currentBranch = git branch --show-current
$upstream = ""
try {
    $upstream = git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null
} catch {
    $upstream = ""
}

Write-Section "Repository"
Write-Host "Path:    $(git rev-parse --show-toplevel)"
Write-Host "Branch:  $currentBranch"
if ($upstream) {
    Write-Host "Upstream: $upstream"
} else {
    Write-Host "Upstream: none"
}

Write-Section "Remote"
git remote -v

Write-Section "Fetch"
git fetch $Remote --prune
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Fetch failed. Remote comparison may be stale until GitHub credentials/network access are available."
}

Write-Section "Branch Status"
git status --short --branch

if ($upstream) {
    Write-Section "Ahead Behind"
    $counts = git rev-list --left-right --count "HEAD...$upstream"
    $parts = $counts -split "\s+"
    Write-Host "Ahead:  $($parts[0])"
    Write-Host "Behind: $($parts[1])"

    Write-Section "Incoming Commits"
    $incoming = git log --oneline "HEAD..$upstream"
    if ($incoming) {
        $incoming
    } else {
        Write-Host "none"
    }

    Write-Section "Outgoing Commits"
    $outgoing = git log --oneline "$upstream..HEAD"
    if ($outgoing) {
        $outgoing
    } else {
        Write-Host "none"
    }
} elseif ($Branch) {
    $remoteRef = "$Remote/$Branch"
    $remoteExists = $true
    try {
        git rev-parse --verify $remoteRef | Out-Null
    } catch {
        $remoteExists = $false
    }

    if ($remoteExists) {
        Write-Section "Ahead Behind"
        $counts = git rev-list --left-right --count "HEAD...$remoteRef"
        $parts = $counts -split "\s+"
        Write-Host "Compared to: $remoteRef"
        Write-Host "Ahead:       $($parts[0])"
        Write-Host "Behind:      $($parts[1])"

        Write-Section "Incoming Commits"
        $incoming = git log --oneline "HEAD..$remoteRef"
        if ($incoming) {
            $incoming
        } else {
            Write-Host "none"
        }

        Write-Section "Outgoing Commits"
        $outgoing = git log --oneline "$remoteRef..HEAD"
        if ($outgoing) {
            $outgoing
        } else {
            Write-Host "none"
        }
    }
}

Write-Section "Conflicts"
$conflicts = git diff --name-only --diff-filter=U
if ($conflicts) {
    $conflicts
} else {
    Write-Host "none"
}

Write-Section "Unstaged Diff"
git diff --stat

Write-Section "Staged Diff"
git diff --cached --stat

Write-Section "Recent Commits"
git log --oneline --decorate --max-count=8
