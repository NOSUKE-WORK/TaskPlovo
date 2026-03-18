@echo off
chcp 65001 > nul

echo [TaskPlovo Build]
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    pause & exit /b 1
)

echo [1/4] Installing packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    pause & exit /b 1
)

echo [2/4] Generating icon...
if not exist "assets" mkdir assets
python generate_icon.py
if %errorlevel% neq 0 (
    echo [ERROR] Icon generation failed.
    pause & exit /b 1
)

echo [3/4] Cleaning old build cache...
if exist "dist\TaskPlovo.exe" del /f /q "dist\TaskPlovo.exe"
if exist "build" rmdir /s /q "build"
if exist "TaskPlovo.spec" del /f /q "TaskPlovo.spec"

echo [4/4] Building EXE...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name "TaskPlovo" ^
  --icon "%cd%\assets\icon.ico" ^
  --add-data "%cd%\assets;assets" ^
  --hidden-import "pystray._win32" ^
  --hidden-import "PIL._tkinter_finder" ^
  --hidden-import "ttkbootstrap" ^
  --hidden-import "openpyxl" ^
  --collect-all ttkbootstrap ^
  --version-file "version_info.txt" ^
  main.py

if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    pause & exit /b 1
)

if not exist "dist\TaskPlovo.exe" (
    echo [ERROR] dist\TaskPlovo.exe not found.
    pause & exit /b 1
)

echo.
echo Build complete!
echo   dist\TaskPlovo.exe  --  Share this file directly. No installer needed.
echo.
pause
