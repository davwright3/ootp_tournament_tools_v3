; --- installer/installer.iss ---

[Setup]
AppName=AU Tournament Tool v3
AppVersion=0.0.1
AppPublisher=AngeredUnicorn
DefaultDirName={pf}\AU_Tournament_Tool_v3
DefaultGroupName=AU Tournament Tool v3
OutputDir=Output
OutputBaseFilename=AU_Tournament_Tool_v3_Setup
ArchitecturesInstallIn64BitMode=x64
Compression=lzma
SolidCompression=yes

[Files]
; Handle ONEFILE: dist\main.exe
Source: "..\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AU Tournament Utilities v2"; Filename: "{app}\main.exe"
Name: "{commondesktop}\AU Tournament Utilities v2"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\main.exe"; Description: "Launch AU Tournament Utilities v2"; Flags: nowait postinstall skipifsilent; Check: FileExists(ExpandConstant('{app}\main.exe'))