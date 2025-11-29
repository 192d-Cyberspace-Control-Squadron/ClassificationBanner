# Install-ClassificationBannerADMX.ps1
# Installs Classification Banner ADMX/ADML files to Group Policy Central Store

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('CentralStore','Local')]
    [string]$InstallLocation = 'CentralStore',
    
    [Parameter(Mandatory=$false)]
    [string]$Domain = $env:USERDNSDOMAIN
)

# Require administrative privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script requires administrative privileges. Please run as Administrator."
    exit 1
}

Write-Host "Classification Banner ADMX Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Determine installation paths
if ($InstallLocation -eq 'CentralStore') {
    if ([string]::IsNullOrEmpty($Domain)) {
        Write-Error "Cannot determine domain name. Either join the computer to a domain or use -InstallLocation Local"
        exit 1
    }
    
    $admxPath = "\\$Domain\SYSVOL\$Domain\Policies\PolicyDefinitions"
    $admlPath = "$admxPath\en-US"
    
    Write-Host "Installing to Central Store (Domain: $Domain)" -ForegroundColor Green
} else {
    $admxPath = "$env:SystemRoot\PolicyDefinitions"
    $admlPath = "$admxPath\en-US"
    
    Write-Host "Installing to Local Computer" -ForegroundColor Green
}

Write-Host "ADMX Path: $admxPath" -ForegroundColor Gray
Write-Host "ADML Path: $admlPath" -ForegroundColor Gray
Write-Host ""

# Check if Central Store exists (create if needed)
if ($InstallLocation -eq 'CentralStore') {
    if (-not (Test-Path $admxPath)) {
        Write-Host "Central Store does not exist. Creating..." -ForegroundColor Yellow
        try {
            New-Item -Path $admxPath -ItemType Directory -Force | Out-Null
            New-Item -Path $admlPath -ItemType Directory -Force | Out-Null
            Write-Host "Central Store created successfully." -ForegroundColor Green
        } catch {
            Write-Error "Failed to create Central Store: $_"
            exit 1
        }
    }
}

# Verify paths exist
if (-not (Test-Path $admxPath)) {
    Write-Error "Path does not exist: $admxPath"
    exit 1
}

if (-not (Test-Path $admlPath)) {
    Write-Host "Creating en-US directory..." -ForegroundColor Yellow
    New-Item -Path $admlPath -ItemType Directory -Force | Out-Null
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$admxFile = Join-Path $scriptDir "ClassificationBanner.admx"
$admlFile = Join-Path $scriptDir "en-US\ClassificationBanner.adml"

# Verify source files exist
if (-not (Test-Path $admxFile)) {
    Write-Error "ADMX file not found: $admxFile"
    Write-Host "Please ensure ClassificationBanner.admx is in the same directory as this script."
    exit 1
}

if (-not (Test-Path $admlFile)) {
    Write-Error "ADML file not found: $admlFile"
    Write-Host "Please ensure ClassificationBanner.adml is in the en-US subdirectory."
    exit 1
}

# Backup existing files if they exist
$admxDest = Join-Path $admxPath "ClassificationBanner.admx"
$admlDest = Join-Path $admlPath "ClassificationBanner.adml"

if (Test-Path $admxDest) {
    Write-Host "Backing up existing ADMX file..." -ForegroundColor Yellow
    Copy-Item $admxDest "$admxDest.backup" -Force
}

if (Test-Path $admlDest) {
    Write-Host "Backing up existing ADML file..." -ForegroundColor Yellow
    Copy-Item $admlDest "$admlDest.backup" -Force
}

# Copy files
try {
    Write-Host "Copying ClassificationBanner.admx..." -ForegroundColor Cyan
    Copy-Item $admxFile $admxDest -Force
    Write-Host "  ✓ ADMX file copied successfully" -ForegroundColor Green
    
    Write-Host "Copying ClassificationBanner.adml..." -ForegroundColor Cyan
    Copy-Item $admlFile $admlDest -Force
    Write-Host "  ✓ ADML file copied successfully" -ForegroundColor Green
    
} catch {
    Write-Error "Failed to copy files: $_"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($InstallLocation -eq 'CentralStore') {
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Open Group Policy Management Console (gpmc.msc)" -ForegroundColor White
    Write-Host "2. Edit a Group Policy Object" -ForegroundColor White
    Write-Host "3. Navigate to: Computer Configuration → Administrative Templates" -ForegroundColor White
    Write-Host "4. Look for 'Classification Banner' category" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: If you don't see the category, close and reopen GPMC." -ForegroundColor Gray
    Write-Host ""
    Write-Host "The policies will be available on all domain controllers within a few minutes." -ForegroundColor Cyan
} else {
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Open Local Group Policy Editor (gpedit.msc)" -ForegroundColor White
    Write-Host "2. Navigate to: Computer Configuration → Administrative Templates" -ForegroundColor White
    Write-Host "3. Look for 'Classification Banner' category" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: If you don't see the category, close and reopen gpedit.msc." -ForegroundColor Gray
}

Write-Host ""
Write-Host "For detailed configuration guidance, see ADMX_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
