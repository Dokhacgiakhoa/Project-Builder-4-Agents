@echo off
setlocal enabledelayedexpansion

title Build Project-Review.exe with Custom Icon

echo ======================================================================
echo   DONG GOI PROJECT-REVIEW.EXE VOI CUSTOM APP ICON
echo   Universal Project Starter Kit - Standalone Binary Builder
echo ======================================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python tren he thong de build file .exe!
    echo.
    pause
    exit /b 1
)

:: 2. Check icon file
if not exist "%~dp0assets\app-icon.ico" (
    echo [INFO] Dang tao file icon assets\app-icon.ico...
    python "%~dp0scripts\generate_icon.py"
)

:: 3. Check or install PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Dang cai dat PyInstaller...
    pip install pyinstaller
)

:: 4. Build Standalone Exe with PyInstaller
echo [INFO] Dang bien dich Project-Review.exe voi Icon doc quyen...
echo.

pyinstaller --noconfirm --clean --onefile --console --icon="%~dp0assets\app-icon.ico" --name="Project-Review" "%~dp0scripts\project_auditor.py"

if errorlevel 1 (
    echo.
    echo [ERROR] Bien dich that bai! Vui long kiem tra log o tren.
    pause
    exit /b 1
)

:: 5. Move executable to root directory and cleanup temporary files
if exist "%~dp0dist\Project-Review.exe" (
    echo [INFO] Di chuyen Project-Review.exe ra thu muc goc...
    move /Y "%~dp0dist\Project-Review.exe" "%~dp0Project-Review.exe" >nul
)

echo [INFO] Don dep thu muc build tam thoi...
if exist "%~dp0build" rmdir /S /Q "%~dp0build"
if exist "%~dp0dist" rmdir /S /Q "%~dp0dist"
if exist "%~dp0Project-Review.spec" del /Q "%~dp0Project-Review.spec"

echo.
echo ======================================================================
echo   [THANH CONG] Da tao Project-Review.exe thanh cong!
echo   Icon: assets\app-icon.ico da duoc nhung truc tiep vao file .exe.
echo   Ban co the nhap dup Project-Review.exe tren Windows Explorer de chay!
echo ======================================================================
echo.

if "%~1"=="" pause
exit /b 0
