$ErrorActionPreference = "Stop"

function Get-NodeCandidatePaths {
    $paths = @()

    $command = Get-Command node -ErrorAction SilentlyContinue
    if ($command -and $command.Source) {
        $paths += $command.Source
    }

    if ($env:ProgramFiles) {
        $paths += Join-Path $env:ProgramFiles "nodejs\node.exe"
    }

    if ($env:LOCALAPPDATA) {
        $paths += Join-Path $env:LOCALAPPDATA "Programs\nodejs\node.exe"
    }

    return $paths | Where-Object { $_ } | Select-Object -Unique
}

function Get-WorkingNodePath {
    foreach ($candidate in Get-NodeCandidatePaths) {
        if (-not (Test-Path $candidate)) {
            continue
        }

        try {
            $versionOutput = & $candidate --version 2>$null
            if (-not $versionOutput) {
                continue
            }

            $cleanVersion = $versionOutput.Trim()
            if (-not $cleanVersion.StartsWith("v")) {
                continue
            }

            $version = [Version]($cleanVersion.TrimStart("v"))
            if ($version.Major -ge 20) {
                return $candidate
            }
        }
        catch {
            continue
        }
    }

    return $null
}

function Get-FfmpegCandidatePaths {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BinaryName
    )

    $paths = @()
    $command = Get-Command $BinaryName -ErrorAction SilentlyContinue
    if ($command -and $command.Source) {
        $paths += $command.Source
    }

    if ($env:ProgramFiles) {
        $paths += Join-Path $env:ProgramFiles "ffmpeg\bin\$BinaryName.exe"
        $paths += Join-Path $env:ProgramFiles "ffmpeg\$BinaryName.exe"
    }

    if ($env:LOCALAPPDATA) {
        $paths += Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Links\$BinaryName.exe"
    }

    if ($env:ChocolateyInstall) {
        $paths += Join-Path $env:ChocolateyInstall "bin\$BinaryName.exe"
    }

    return $paths | Where-Object { $_ } | Select-Object -Unique
}

function Get-WorkingFfmpegPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BinaryName
    )

    foreach ($candidate in Get-FfmpegCandidatePaths -BinaryName $BinaryName) {
        if (-not (Test-Path $candidate)) {
            continue
        }

        try {
            $versionOutput = & $candidate -version 2>$null
            if (-not $versionOutput) {
                continue
            }

            $firstLine = $versionOutput | Select-Object -First 1
            if ($firstLine -and $firstLine.ToLowerInvariant().Contains("$BinaryName version")) {
                return $candidate
            }
        }
        catch {
            continue
        }
    }

    return $null
}

$projectRoot = Join-Path $PSScriptRoot ".."
$projectRoot = [System.IO.Path]::GetFullPath($projectRoot)

Write-Host "Verificando runtime JavaScript para o VideoSong..."
$nodePath = Get-WorkingNodePath

if (-not $nodePath) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw "winget nao encontrado. Instale manualmente o Node.js LTS 20+ em https://nodejs.org/ e confirme que node esta no PATH."
    }

    Write-Host "Node.js 20+ nao encontrado. Instalando Node.js LTS via winget..."
    & $winget.Source install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements

    $nodePath = Get-WorkingNodePath
    if (-not $nodePath) {
        throw "A instalacao terminou, mas nenhum node utilizavel foi encontrado ainda. Feche e reabra o terminal e valide com node --version."
    }
}

Write-Host "Node.js utilizavel encontrado em: $nodePath"
Write-Host "Versao detectada: $(& $nodePath --version)"

Write-Host ""
Write-Host "Verificando ffmpeg e ffprobe para o VideoSong..."
$ffmpegPath = Get-WorkingFfmpegPath -BinaryName "ffmpeg"
$ffprobePath = Get-WorkingFfmpegPath -BinaryName "ffprobe"

if (-not $ffmpegPath -or -not $ffprobePath) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw "winget nao encontrado. Instale manualmente o pacote completo do FFmpeg e confirme que ffmpeg e ffprobe estao no PATH."
    }

    Write-Host "FFmpeg completo nao encontrado. Instalando via winget..."
    & $winget.Source install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements

    $ffmpegPath = Get-WorkingFfmpegPath -BinaryName "ffmpeg"
    $ffprobePath = Get-WorkingFfmpegPath -BinaryName "ffprobe"
    if (-not $ffmpegPath -or -not $ffprobePath) {
        throw "A instalacao terminou, mas ffmpeg/ffprobe ainda nao foram encontrados. Feche e reabra o terminal e valide com ffmpeg -version e ffprobe -version."
    }
}

Write-Host "ffmpeg utilizavel encontrado em: $ffmpegPath"
Write-Host "ffprobe utilizavel encontrado em: $ffprobePath"
Write-Host ""
Write-Host "Proximo passo:"
Write-Host "1. Ative o ambiente virtual"
Write-Host "2. Instale os pacotes Python com python -m pip install -r requirements.txt"
Write-Host "3. Execute .\scripts\build_windows.ps1 -ReleaseLabel sprint-2 para gerar um pacote com ffmpeg/ffprobe inclusos"
Write-Host "4. Ou execute python main.py para rodar localmente"
