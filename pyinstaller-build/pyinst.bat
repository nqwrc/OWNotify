SET Name=OWNotify
SET Settings=config.ini
SET Dest=dist\%Name%

REM pyinstaller gui.py -n %Name% -w --onedir --clean -y --upx-dir=PATH_TO_UPX_FOLDER\upx-3.96-win64
REM pyinstaller OWN_1File.spec --clean -y --upx-dir=PATH_TO_UPX_FOLDER\upx-3.96-win64
pyinstaller OWN_1Dir.spec --clean -y --upx-dir=PATH_TO_UPX_FOLDER\upx-3.96-win64

mkdir %Dest%\icons
copy icons\own.ico dist\%Name%\icons
copy %Settings% %Dest%

REM Deletes whole directory
rd /s /q ^
    __pycache__ ^
    .vscode

REM Deletes file
cd %Dest%
del /f /q ^
    %Name%.exe.manifest ^
    mfc140u.dll ^