# install.ps1 - Windows installation script
# Run as Administrator in PowerShell

param(
    [switch]$NoPrompt,
    [string]$InstallPath = "C:\LETS-SPOOF-PORT-53"
)

# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Colors for output
$Red = "`e[31m"
$Green = "`e[32m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$NC = "`e[0m"

Write-Host "$Blue"
@"
╔══════════════════════════════════════════════════════════════════════════════╗
║                   LETS-SPOOF-PORT-53 - Windows Installation                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"@
Write-Host "$NC"

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "$Red`❌ Please run as Administrator$NC"
    exit 1
}

# Check PowerShell version
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Host "$Red`❌ PowerShell 5.0 or higher required$NC"
    exit 1
}

# Install Chocolatey
function Install-Chocolatey {
    Write-Host "$Yellow`📦 Installing Chocolatey...$NC"
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Install Python
function Install-Python {
    Write-Host "$Yellow`🐍 Installing Python...$NC"
    choco install python --version=3.9.10 -y
    refreshenv
}

# Install system tools
function Install-SystemTools {
    Write-Host "$Yellow`🔧 Installing system tools...$NC"
    
    $tools = @(
        "nmap",
        "wireshark",
        "git",
        "curl",
        "vscode",
        "chromium",
        "python3"
    )
    
    foreach ($tool in $tools) {
        choco install $tool -y
    }
    
    # Install npcap for packet capture
    choco install npcap -y
}

# Create installation directory
function Create-InstallDirectory {
    Write-Host "$Yellow`📁 Creating installation directory...$NC"
    
    if (Test-Path $InstallPath) {
        Remove-Item -Path $InstallPath -Recurse -Force
    }
    
    New-Item -ItemType Directory -Path $InstallPath -Force
    New-Item -ItemType Directory -Path "$InstallPath\.lets-spoof-port-53" -Force
    New-Item -ItemType Directory -Path "$InstallPath\reports" -Force
    New-Item -ItemType Directory -Path "$InstallPath\logs" -Force
}

# Clone repository
function Clone-Repository {
    Write-Host "$Yellow`📥 Cloning repository...$NC"
    
    Set-Location $InstallPath
    git clone https://gitlab.com/your-repo/lets-spoof-port-53.git .
}

# Setup Python virtual environment
function Setup-VirtualEnv {
    Write-Host "$Yellow`🐍 Setting up Python virtual environment...$NC"
    
    Set-Location $InstallPath
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    
    # Upgrade pip
    python -m pip install --upgrade pip setuptools wheel
}

# Install Python requirements
function Install-PythonRequirements {
    Write-Host "$Yellow`📚 Installing Python packages...$NC"
    
    Set-Location $InstallPath
    
    $packages = @(
        "scapy",
        "colorama",
        "requests",
        "psutil",
        "paramiko",
        "flask",
        "flask-socketio",
        "python-telegram-bot",
        "discord.py",
        "slack-sdk",
        "twilio",
        "python-whois",
        "qrcode",
        "pyshorteners",
        "shodan",
        "python-hunter",
        "phonenumbers",
        "selenium",
        "pandas",
        "matplotlib",
        "seaborn",
        "numpy",
        "reportlab",
        "aiohttp",
        "websockets",
        "cryptography",
        "pywin32"
    )
    
    foreach ($package in $packages) {
        Write-Host "$Yellow  Installing $package...$NC"
        python -m pip install $package
    }
}

# Create start menu shortcut
function Create-Shortcut {
    Write-Host "$Yellow`🔗 Creating start menu shortcut...$NC"
    
    $shortcutPath = [Environment]::GetFolderPath("Programs") + "\LETS-SPOOF-PORT-53.lnk"
    $targetPath = "$InstallPath\venv\Scripts\python.exe"
    $arguments = "$InstallPath\lets_spoof_port_53.py"
    
    $WScriptShell = New-Object -ComObject WScript.Shell
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $targetPath
    $shortcut.Arguments = $arguments
    $shortcut.WorkingDirectory = $InstallPath
    $shortcut.Save()
}

# Create desktop shortcut
function Create-DesktopShortcut {
    Write-Host "$Yellow`🖥️  Creating desktop shortcut...$NC"
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = "$desktopPath\LETS-SPOOF-PORT-53.lnk"
    $targetPath = "$InstallPath\venv\Scripts\python.exe"
    $arguments = "$InstallPath\lets_spoof_port_53.py"
    
    $WScriptShell = New-Object -ComObject WScript.Shell
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $targetPath
    $shortcut.Arguments = $arguments
    $shortcut.WorkingDirectory = $InstallPath
    $shortcut.Save()
}

# Create batch file for easy launch
function Create-BatchFile {
    Write-Host "$Yellow`📝 Creating batch file...$NC"
    
    $batchContent = @"
@echo off
echo Starting LETS-SPOOF-PORT-53...
cd /d $InstallPath
call venv\Scripts\activate.bat
python lets_spoof_port_53.py
pause
"@
    
    $batchContent | Out-File -FilePath "$InstallPath\launch.bat" -Encoding ASCII
    $batchContent | Out-File -FilePath "$desktopPath\LETS-SPOOF-PORT-53.bat" -Encoding ASCII
}

# Add to PATH
function Add-ToPath {
    Write-Host "$Yellow`🔧 Adding to PATH...$NC"
    
    $path = [Environment]::GetEnvironmentVariable("Path", "User")
    $newPath = "$InstallPath\venv\Scripts;$path"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
}

# Create Windows service (optional)
function Create-WindowsService {
    Write-Host "$Yellow`⚙️  Creating Windows service...$NC"
    
    # Install NSSM (Non-Sucking Service Manager)
    choco install nssm -y
    
    # Create service
    nssm install LETS-SPOOF-PORT-53 "$InstallPath\venv\Scripts\python.exe"
    nssm set LETS-SPOOF-PORT-53 AppParameters "$InstallPath\lets_spoof_port_53.py"
    nssm set LETS-SPOOF-PORT-53 AppDirectory $InstallPath
    nssm set LETS-SPOOF-PORT-53 Start SERVICE_AUTO_START
    
    Write-Host "$Green`✅ Service created$NC"
    Write-Host "$Yellow  Use 'services.msc' to manage the service$NC"
}

# Main installation
function Main {
    if (-not $NoPrompt) {
        $confirm = Read-Host "This will install LETS-SPOOF-PORT-53. Continue? (Y/N)"
        if ($confirm -ne 'Y') {
            Write-Host "$Yellow`Installation cancelled$NC"
            exit 0
        }
    }
    
    # Check if Chocolatey is installed
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Install-Chocolatey
    }
    
    Install-Python
    Install-SystemTools
    Create-InstallDirectory
    Clone-Repository
    Setup-VirtualEnv
    Install-PythonRequirements
    Create-Shortcut
    Create-DesktopShortcut
    Create-BatchFile
    Add-ToPath
    
    # Optional: Create Windows service
    $createService = Read-Host "Create Windows service? (Y/N)"
    if ($createService -eq 'Y') {
        Create-WindowsService
    }
    
    Write-Host "$Green"
    Write-Host "╔════════════════════════════════════════════════════════════════╗"
    Write-Host "║                    Installation Complete!                       ║"
    Write-Host "╚════════════════════════════════════════════════════════════════╝"
    Write-Host "$NC"
    Write-Host "$Green`✅ LETS-SPOOF-PORT-53 has been installed successfully!$NC"
    Write-Host ""
    Write-Host "$Yellow`To start the tool:$NC"
    Write-Host "  Double-click the desktop shortcut or run: launch.bat"
    Write-Host ""
    Write-Host "$Yellow`Configuration files:$NC"
    Write-Host "  $InstallPath\.lets-spoof-port-53\"
    Write-Host ""
    Write-Host "$Blue`🔮 Happy Spoofing!$NC"
}

# Run main installation
Main