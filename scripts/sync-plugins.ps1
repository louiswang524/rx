# Sync local RX source into Codex plugin caches + Claude Code marketplace.
# Run after editing skills under C:\Users\louis\rx
# Usage: powershell -File C:\Users\louis\rx\scripts\sync-plugins.ps1
$ErrorActionPreference = "Stop"
$src = "C:\Users\louis\rx"
if (-not (Test-Path (Join-Path $src "skills"))) {
  throw "RX source not found at $src"
}
$exclude = @(".git", ".venv", ".pytest_cache", ".superpowers", "__pycache__", "node_modules")
$codexCacheRoot = Join-Path $env:USERPROFILE ".codex\plugins\cache\personal\rx"
$pluginsCopy = "C:\Users\louis\plugins\rx"

# Read version from plugin.json
$ver = (Get-Content (Join-Path $src ".claude-plugin\plugin.json") -Raw | ConvertFrom-Json).version
Write-Host "RX version: $ver  source: $src"

foreach ($v in @($ver, "0.1.0")) {
  $dst = Join-Path $codexCacheRoot $v
  New-Item -ItemType Directory -Force -Path $dst | Out-Null
  Write-Host "Syncing Codex cache $v ..."
  & robocopy $src $dst /MIR /XD @exclude /NFL /NDL /NJH /NJS /nc /ns /np | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "robocopy failed: $LASTEXITCODE" }
}

Write-Host "Syncing plugins\rx ..."
New-Item -ItemType Directory -Force -Path $pluginsCopy | Out-Null
& robocopy $src $pluginsCopy /MIR /XD @exclude /NFL /NDL /NJH /NJS /nc /ns /np | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy plugins\rx failed: $LASTEXITCODE" }

Write-Host "Updating Claude Code marketplace + plugin (WSL) ..."
wsl bash -lc "claude plugin marketplace update rx-dev && claude plugin update rx@rx-dev"
Write-Host "Done. Start a NEW Codex / Claude Code session to load skills."
