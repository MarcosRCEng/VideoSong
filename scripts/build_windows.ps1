param(
    [Parameter(Mandatory = $true)]
    [string]$ReleaseLabel
)

$ErrorActionPreference = "Stop"

function Get-RequiredBinaryPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BinaryName
    )

    $candidates = @()
    $command = Get-Command $BinaryName -ErrorAction SilentlyContinue
    if ($command -and $command.Source) {
        $candidates += $command.Source
    }

    if ($env:ProgramFiles) {
        $candidates += Join-Path $env:ProgramFiles "ffmpeg\bin\$BinaryName.exe"
        $candidates += Join-Path $env:ProgramFiles "ffmpeg\$BinaryName.exe"
    }

    if ($env:LOCALAPPDATA) {
        $candidates += Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Links\$BinaryName.exe"
    }

    if ($env:ChocolateyInstall) {
        $candidates += Join-Path $env:ChocolateyInstall "bin\$BinaryName.exe"
    }

    foreach ($candidate in ($candidates | Where-Object { $_ } | Select-Object -Unique)) {
        if (-not (Test-Path $candidate)) {
            continue
        }

        try {
            $null = & $candidate -version 2>$null
            return $candidate
        }
        catch {
            continue
        }
    }

    throw "$BinaryName nao encontrado. Execute .\scripts\setup_windows.ps1 antes de empacotar."
}

$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
$python = [System.IO.Path]::GetFullPath($python)
$spec = Join-Path $PSScriptRoot "..\VideoSong.spec"
$spec = [System.IO.Path]::GetFullPath($spec)
$distPath = Join-Path $PSScriptRoot "..\dist"
$distPath = [System.IO.Path]::GetFullPath($distPath)
$tmpPath = Join-Path ([System.IO.Path]::GetTempPath()) "VideoSong-Build"
$buildRunId = "{0}-{1}" -f (Get-Date -Format "yyyyMMdd-HHmmss"), $PID
$stagingRootPath = Join-Path $tmpPath "pyinstaller\$buildRunId"
$stagingBuildPath = Join-Path $stagingRootPath "build"
$stagingDistPath = Join-Path $stagingRootPath "dist"
$releasePath = Join-Path $distPath "releases"
$releaseFileName = "VideoSong-$ReleaseLabel.exe"
$releaseFilePath = Join-Path $releasePath $releaseFileName
$builtExePath = Join-Path $distPath "VideoSong.exe"
$stagedExePath = Join-Path $stagingDistPath "VideoSong.exe"

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

New-Item -ItemType Directory -Path $stagingRootPath -Force | Out-Null
New-Item -ItemType Directory -Path $stagingBuildPath -Force | Out-Null
New-Item -ItemType Directory -Path $stagingDistPath -Force | Out-Null
New-Item -ItemType Directory -Path $distPath -Force | Out-Null

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --distpath $stagingDistPath `
    --workpath $stagingBuildPath `
    $spec

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller falhou com codigo $LASTEXITCODE. O executavel nao sera publicado em dist\\."
}

if (-not (Test-Path $stagedExePath)) {
    throw "Build concluido sem gerar o executavel em staging. Revise a configuracao do PyInstaller."
}

New-Item -ItemType Directory -Path $releasePath -Force | Out-Null
Copy-Item -LiteralPath $stagedExePath -Destination $builtExePath -Force
Copy-Item -LiteralPath $stagedExePath -Destination $releaseFilePath -Force

Write-Host "Artefato principal: $builtExePath"
Write-Host "Artefato versionado: $releaseFilePath"
