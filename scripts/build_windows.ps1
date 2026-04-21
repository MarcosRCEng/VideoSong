$ErrorActionPreference = "Stop"

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
