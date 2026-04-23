@echo off
setlocal

if "%~1"=="" (
  echo Uso: %~nx0 RELEASE_LABEL
  exit /b 1
)

set "RELEASE_LABEL=%~1"
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
for %%I in ("%PROJECT_ROOT%") do set "PROJECT_ROOT=%%~fI"

set "INSTALLER_SCRIPT=%SCRIPT_DIR%VideoSongInstaller.iss"
for %%I in ("%INSTALLER_SCRIPT%") do set "INSTALLER_SCRIPT=%%~fI"

set "SOURCE_EXE=%PROJECT_ROOT%\dist\VideoSong.exe"
for %%I in ("%SOURCE_EXE%") do set "SOURCE_EXE=%%~fI"

set "OUTPUT_DIR=%PROJECT_ROOT%\dist\releases"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

set "ISCC_PATH="
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC_PATH if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"

if not defined ISCC_PATH (
  where ISCC >nul 2>nul
  if not errorlevel 1 for /f "delims=" %%I in ('where ISCC') do set "ISCC_PATH=%%I"
)

if not defined ISCC_PATH (
  echo ISCC.exe nao encontrado. Instale o Inno Setup 6 antes de gerar o instalador.
  exit /b 1
)

if not exist "%INSTALLER_SCRIPT%" (
  echo Script do instalador nao encontrado em "%INSTALLER_SCRIPT%".
  exit /b 1
)

if not exist "%SOURCE_EXE%" (
  echo Executavel base nao encontrado em "%SOURCE_EXE%". Gere o build do app antes do instalador.
  exit /b 1
)

set "OUTPUT_BASENAME=VideoSong-%RELEASE_LABEL%-setup"

"%ISCC_PATH%" ^
  /DReleaseLabel=%RELEASE_LABEL% ^
  /DAppVersion=%RELEASE_LABEL% ^
  /DSourceExe=%SOURCE_EXE% ^
  /DOutputDir=%OUTPUT_DIR% ^
  /DOutputBaseFilename=%OUTPUT_BASENAME% ^
  "%INSTALLER_SCRIPT%"

if errorlevel 1 exit /b %errorlevel%

echo Instalador gerado em "%OUTPUT_DIR%\%OUTPUT_BASENAME%.exe"
endlocal
