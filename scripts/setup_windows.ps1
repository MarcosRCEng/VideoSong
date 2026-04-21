$ErrorActionPreference = "Stop"

function Get-NodeCandidatePaths {
    $paths = @()

    $command = Get-Command node -ErrorAction SilentlyContinue
    if ($command -and $command.Source) {
        $paths += $command.Source
    }

    $paths += @(
        (Join-Path $env:ProgramFiles "nodejs\node.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\nodejs\node.exe")
    )

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
Write-Host "Proximo passo:"
Write-Host "1. Ative o ambiente virtual"
Write-Host "2. Instale os pacotes Python com python -m pip install -r requirements.txt"
Write-Host "3. Execute python main.py"
