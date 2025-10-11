@echo off
echo Building FTL Save Manager executable...
echo.

REM Create the executable with PyInstaller
pyinstaller --onefile --windowed --name "FTL Save Manager" --distpath "dist" main.py

echo.
echo Build complete! Executable can be found in the 'dist' folder.
echo File: FTL Save Manager.exe
pause
