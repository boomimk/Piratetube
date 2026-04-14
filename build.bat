@echo off
echo.
echo  ========================================
echo    PirateTube - EXE Builder
echo  ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install it from python.org
    pause
    exit /b
)

:: Install dependencies
echo  [1/3] Installing dependencies...
pip install pyinstaller yt-dlp --quiet

:: Build exe
echo  [2/3] Building PirateTube.exe...
pyinstaller --onefile --name PirateTube --clean Piratetube-Docker.py

:: Done
echo.
echo  [3/3] Done!
echo.
echo  Your EXE is at:  dist\PirateTube.exe
echo.
pause
