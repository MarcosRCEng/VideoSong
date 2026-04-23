param(
    [Parameter(Mandatory = $true)]
    [string]$ReleaseLabel
)

$ErrorActionPreference = "Stop"

function Get-IsccPath {
    $candidates = @()

    $command = Get-Command ISCC -ErrorAction SilentlyContinue
    if ($command -and $command.Source) {
        $candidates += $command.Source
    }

    if ($env:ProgramFiles) {
        $candidates += Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe"
    }

    if ($env:ProgramFiles -and ${env:ProgramFiles(x86)}) {
        $candidates += Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"
    }

    foreach ($candidate in ($candidates | Where-Object { $_ } | Select-Object -Unique)) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    throw "ISCC.exe nao encontrado. Instale o Inno Setup 6 antes de gerar o instalador."
}

$projectRoot = Join-Path $PSScriptRoot ".."
$projectRoot = [System.IO.Path]::GetFullPath($projectRoot)
$installerScript = Join-Path $PSScriptRoot "VideoSongInstaller.iss"
$installerScript = [System.IO.Path]::GetFullPath($installerScript)
$sourceExe = Join-Path $projectRoot "dist\VideoSong.exe"
$sourceExe = [System.IO.Path]::GetFullPath($sourceExe)
$outputDir = Join-Path $projectRoot "dist\releases"
$outputDir = [System.IO.Path]::GetFullPath($outputDir)
$outputBaseFilename = "VideoSong-$ReleaseLabel-setup"
$iscc = Get-IsccPath

if (-not (Test-Path $installerScript)) {
    throw "Script do instalador nao encontrado em scripts\VideoSongInstaller.iss."
}

if (-not (Test-Path $sourceExe)) {
    throw "Executavel base nao encontrado em dist\VideoSong.exe. Gere o build do app antes do instalador."
}

New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

& $iscc `
    "/DReleaseLabel=$ReleaseLabel" `
    "/DAppVersion=$ReleaseLabel" `
    "/DSourceExe=$sourceExe" `
    "/DOutputDir=$outputDir" `
    "/DOutputBaseFilename=$outputBaseFilename" `
    $installerScript

if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup falhou com codigo $LASTEXITCODE."
}

$installerPath = Join-Path $outputDir "$outputBaseFilename.exe"
if (-not (Test-Path $installerPath)) {
    throw "A compilacao terminou, mas o instalador nao foi encontrado em $installerPath."
}

Write-Host "Instalador gerado em: $installerPath"
