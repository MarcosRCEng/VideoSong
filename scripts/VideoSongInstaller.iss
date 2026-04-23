#define MyAppName "VideoSong"
#ifndef ReleaseLabel
  #define ReleaseLabel "local"
#endif
#ifndef AppVersion
  #define AppVersion ReleaseLabel
#endif
#ifndef SourceExe
  #define SourceExe "..\dist\VideoSong.exe"
#endif
#ifndef OutputDir
  #define OutputDir "..\dist\releases"
#endif
#ifndef OutputBaseFilename
  #define OutputBaseFilename "VideoSong-" + ReleaseLabel + "-setup"
#endif

[Setup]
AppId={{B2FEA948-B31F-4C62-95BB-0CC4CA2D11ED}
AppName={#MyAppName}
AppVersion={#AppVersion}
AppPublisher=VideoSong
DefaultDirName={autopf}\VideoSong
DefaultGroupName=VideoSong
OutputDir={#OutputDir}
OutputBaseFilename={#OutputBaseFilename}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\VideoSong.exe

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
Source: "{#SourceExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\VideoSong"; Filename: "{app}\VideoSong.exe"
Name: "{autodesktop}\VideoSong"; Filename: "{app}\VideoSong.exe"; Tasks: desktopicon

[Run]
Filename: "{cmd}"; Parameters: "/C winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements"; Description: "Instalar Node.js LTS (necessario para downloads do YouTube)"; Flags: postinstall runascurrentuser waituntilterminated; Check: NeedNodeInstall
Filename: "{app}\VideoSong.exe"; Description: "Executar VideoSong"; Flags: nowait postinstall skipifsilent

[Code]
function IsNodeInstalled: Boolean;
begin
  Result :=
    FileExists(ExpandConstant('{pf}\nodejs\node.exe')) or
    FileExists(ExpandConstant('{localappdata}\Programs\nodejs\node.exe')) or
    FileExists(ExpandConstant('{localappdata}\Microsoft\WinGet\Links\node.exe'));
end;

function IsWingetAvailable: Boolean;
begin
  Result := FileExists(ExpandConstant('{localappdata}\Microsoft\WindowsApps\winget.exe'));
end;

function NeedNodeInstall: Boolean;
begin
  Result := (not IsNodeInstalled()) and IsWingetAvailable();
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep = ssPostInstall) and (not IsNodeInstalled()) and (not IsWingetAvailable()) then
  begin
    MsgBox(
      'Node.js LTS nao foi encontrado e o winget tambem nao esta disponivel. ' +
      'Instale manualmente o Node.js 20+ em https://nodejs.org/ antes de usar URLs do YouTube.',
      mbInformation,
      MB_OK
    );
  end;
end;
