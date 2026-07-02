#define MyAppName "CA Office Management System"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "CA Office CMS Development Team"
#define MyAppExeName "CAOfficeCMS.exe"

[Setup]
AppId={{A7E1F5C7-77A1-4CC8-9E3A-CA0FF1CEC510}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\CA Office CMS
DefaultGroupName=CA Office CMS
DisableProgramGroupPage=yes
OutputDir=..\dist\installer
OutputBaseFilename=CAOfficeCMSSetup-1.0.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\dist\CAOfficeCMS\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
Name: "{commonappdata}\CAOfficeCMS"
Name: "{commonappdata}\CAOfficeCMS\data"
Name: "{commonappdata}\CAOfficeCMS\backups"
Name: "{commonappdata}\CAOfficeCMS\exports"
Name: "{commonappdata}\CAOfficeCMS\logs"

[Icons]
Name: "{group}\CA Office CMS"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\CA Office CMS"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
