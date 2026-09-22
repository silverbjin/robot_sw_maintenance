#Requires -RunAsAdministrator
$ErrorActionPreference = "Stop"
Write-Host "[1/3] Updating WSL..." -ForegroundColor Cyan
wsl --update

$distros = (wsl --list --quiet) -join "`n"
if ($distros -notmatch "Ubuntu-22.04") {
    Write-Host "[2/3] Installing Ubuntu-22.04..." -ForegroundColor Cyan
    wsl --install -d Ubuntu-22.04
    Write-Host "Ubuntu installation was requested. Reboot Windows if prompted, then launch Ubuntu-22.04 once and create your Linux user." -ForegroundColor Yellow
} else {
    Write-Host "[2/3] Ubuntu-22.04 already installed." -ForegroundColor Green
}

Write-Host "[3/3] Current WSL distributions:" -ForegroundColor Cyan
wsl --list --verbose
Write-Host "After Ubuntu user setup, continue with scripts/01_install_linux.sh inside WSL2." -ForegroundColor Green
