SET Name=OWNotify

REM pyinstaller gui.py -n %Name% --icon=own.ico --onedir --clean -y
REM pyinstaller OWN_1File.spec --clean -y --upx-dir=PATH_TO_UPX_FOLDER
pyinstaller OWN_1Dir.spec --clean -y --upx-dir=%PATH_TO_UPX_FOLDER%

REM Deletes whole directory
rd /s /q ^
    __pycache__ ^
    .vscode

REM Deletes file
cd dist\%Name%
del /f /q ^
    %Name%.exe.manifest ^
    mfc140u.dll ^