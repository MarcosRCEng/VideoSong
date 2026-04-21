$ErrorActionPreference = "Stop"

function Get-RequiredBinaryPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BinaryName
    )

    $command = Get-Command $BinaryName -ErrorAction SilentlyContinue
    if (-not $command -or -not $command.Source) {
        throw "$BinaryName nao encontrado. Execute .\scripts\setup_windows.ps1 antes de empacotar."
    }

    try {
        $null = & $command.Source -version 2>$null
    }
    catch {
        throw "$BinaryName foi encontrado, mas nao esta utilizavel. Execute .\scripts\setup_windows.ps1 antes de empacotar."
    }

    return $command.Source
}

$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
$python = [System.IO.Path]::GetFullPath($python)
$spec = Join-Path $PSScriptRoot "..\VideoSong.spec"
$spec = [System.IO.Path]::GetFullPath($spec)
$buildPath = Join-Path $PSScriptRoot "..\build"
$buildPath = [System.IO.Path]::GetFullPath($buildPath)
$distPath = Join-Path $PSScriptRoot "..\dist"
$distPath = [System.IO.Path]::GetFullPath($distPath)

if (-not (Test-Path $python)) {
    throw "Ambiente virtual nao encontrado em .venv. Crie o ambiente e instale as dependencias antes de empacotar."
}

if (-not (Test-Path $spec)) {
    throw "Arquivo VideoSong.spec nao encontrado. Mantenha a configuracao de empacotamento versionada na raiz do projeto."
}

$nodePath = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodePath -or -not $nodePath.Source) {
    throw "Node.js nao encontrado. Execute .\scripts\setup_windows.ps1 antes de empacotar."
}

$ffmpegPath = Get-RequiredBinaryPath -BinaryName "ffmpeg"
$ffprobePath = Get-RequiredBinaryPath -BinaryName "ffprobe"

$env:VIDEOSONG_FFMPEG_PATH = $ffmpegPath
$env:VIDEOSONG_FFPROBE_PATH = $ffprobePath

if (Test-Path $buildPath) {
    Remove-Item -LiteralPath $buildPath -Recurse -Force
}

if (Test-Path $distPath) {
    Remove-Item -LiteralPath $distPath -Recurse -Force
}

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    $spec
