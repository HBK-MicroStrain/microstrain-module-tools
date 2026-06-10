param (
    [switch]$python,
    [switch]$csharp
)

$root = Split-Path $PSScriptRoot -Parent
$workspace = "$env:USERPROFILE\opendaq-notebooks"

Set-Location $root

if (-not $python -and -not $csharp) {
    Write-Error "Specify at least one of --python or --csharp."
    exit 1
}

if (Test-Path ".venv") {
    Write-Host "Removing existing virtual environment."
    Remove-Item -Recurse -Force .venv
}

Write-Host "Setting up virtual environment."
python -m venv .venv

Write-Host "Activating virtual environment."
& .venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies."
pip install -r requirements.txt

if (-not (Test-Path $workspace)) {
    New-Item -ItemType Directory $workspace | Out-Null
}

if ($python) {
    $dest = "$workspace\python_starter.ipynb"
    if (-not (Test-Path $dest)) {
        Copy-Item "$root\templates\python\python_template.ipynb" $dest
        Write-Host "Copied Python starter notebook."
    }
}

if ($csharp) {
    $dotnetJupyterDir = "$env:USERPROFILE\.dotnet-jupyter"

    if (-not (Test-Path $dotnetJupyterDir)) {
        Write-Host "Setting up dedicated .NET environment for Jupyter."
        $env:DOTNET_INSTALL_DIR = $dotnetJupyterDir
        & ([scriptblock]::Create((Invoke-RestMethod https://dot.net/v1/dotnet-install.ps1))) -Channel 8.0 -InstallDir $dotnetJupyterDir

        Write-Host "Installing C# Jupyter kernel."
        & "$dotnetJupyterDir\dotnet.exe" tool install Microsoft.dotnet-interactive --tool-path "$dotnetJupyterDir\tools"
        & "$dotnetJupyterDir\tools\dotnet-interactive" jupyter install
    } else {
        Write-Host "Dedicated .NET environment for Jupyter already exists, skipping."
    }

    $dest = "$workspace\csharp_starter.ipynb"
    if (-not (Test-Path $dest)) {
        Copy-Item "$root\templates\csharp\csharp_template.ipynb" $dest
        Write-Host "Copied C# starter notebook."
    }
}

Write-Host "Setup complete. Run scripts/start.bat to begin a session."
