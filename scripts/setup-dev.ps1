<#
setup-dev.ps1

Creates a workspace virtualenv (.venv), upgrades pip, installs requirements,
and optionally installs `skopeo` inside WSL for Dockerfile analysis.

Usage:
  # create venv and install requirements
  .\scripts\setup-dev.ps1

  # also install skopeo in WSL (requires WSL and sudo privileges in distro)
  .\scripts\setup-dev.ps1 -InstallSkopeo
#>

param(
    [switch]$InstallSkopeo
)

Set-StrictMode -Version Latest

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-ErrorAndExit($msg) { Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }

Write-Info "Setting up development environment in: $(Get-Location)"

# 1) Ensure python is available
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-ErrorAndExit "Python not found on PATH. Install Python 3.11+ and re-run this script."
}

# 2) Create venv if missing
$venvPath = Join-Path (Get-Location) '.venv'
if (-not (Test-Path $venvPath)) {
    Write-Info "Creating virtual environment at $venvPath"
    & python -m venv .venv
} else {
    Write-Info "Virtual environment already exists at $venvPath"
}

# 3) Use the venv python to upgrade pip and install requirements
$venvPython = Join-Path $venvPath 'Scripts\python.exe'
if (-not (Test-Path $venvPython)) {
    Write-ErrorAndExit "Virtualenv python not found at $venvPython"
}

Write-Info "Upgrading pip, setuptools, wheel in the virtualenv"
& $venvPython -m pip install --upgrade pip setuptools wheel

$reqFile = Join-Path (Join-Path (Get-Location) 'Eyes-of-an-Addict') 'requirements.txt'
if (-not (Test-Path $reqFile)) {
    Write-Warn "requirements.txt not found at $reqFile; skipping dependency install"
} else {
    Write-Info "Installing requirements from $reqFile"
    & $venvPython -m pip install -r $reqFile
}

# 4) Install small runtime extras commonly used for local dev
Write-Info "Installing optional runtime tools (gunicorn, rq, redis) into venv"
& $venvPython -m pip install --upgrade gunicorn rq redis | Out-Null

Write-Info "Done. To activate the virtualenv in this shell run:"
Write-Host "    .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Green
Write-Host "Then you can run the app (dev):" -ForegroundColor Green
Write-Host "    $env:DATABASE_URL='sqlite:///dev.db' ; python .\\Eyes-of-an-Addict\\main.py" -ForegroundColor Green

if ($InstallSkopeo) {
    # 5) Try to install skopeo in WSL (best-effort)
    $wsl = Get-Command wsl -ErrorAction SilentlyContinue
    if (-not $wsl) {
        Write-Warn "WSL not found on this machine. Cannot install skopeo in WSL."
    } else {
        Write-Info "Installing skopeo inside WSL (requires sudo). You may be prompted for your password."
        try {
            wsl sudo apt-get update -y
            wsl sudo apt-get install -y skopeo
            Write-Info "skopeo install attempted in WSL. Verify with: wsl skopeo --version"
        } catch {
            Write-Warn "Failed to install skopeo in WSL: $_"
        }
    }
}

Write-Info "Setup complete. If you use VS Code, select the interpreter: .venv\\Scripts\\python.exe"
