$ErrorActionPreference = "Stop"

$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
$python = [System.IO.Path]::GetFullPath($python)
$spec = Join-Path $PSScriptRoot "..\VideoSong.spec"
$spec = [System.IO.Path]::GetFullPath($spec)

if (-not (Test-Path $python)) {
    throw "Ambiente virtual nao encontrado em .venv. Crie o ambiente e instale as dependencias antes de empacotar."
}

if (-not (Test-Path $spec)) {
    throw "Arquivo VideoSong.spec nao encontrado. Mantenha a configuracao de empacotamento versionada na raiz do projeto."
}

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    $spec
