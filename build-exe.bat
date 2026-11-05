@echo off
setlocal enabledelayedexpansion

title Build Project-Review.exe with Native .NET 10 Shell

echo ======================================================================
echo   DONG GOI PROJECT-REVIEW.EXE VOI NATIVE .NET 10 SHELL
echo   Universal Project Starter Kit - Standalone Binary Builder
echo ======================================================================
echo.

:: 0. Kill any running Project-Review instance
taskkill /F /IM Project-Review.exe >nul 2>&1

:: 1. Check dotnet
dotnet --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay .NET SDK tren he thong de build!
    echo Vui long cai dat .NET 10 SDK: https://dotnet.microsoft.com/download
    echo.
    pause
    exit /b 1
)

:: 2. Check icon file
if not exist "%~dp0assets\app-icon.ico" (
    echo [INFO] Dang tao file icon assets\app-icon.ico...
    python "%~dp0scripts\generate_icon.py"
)

:: 3. Build Standalone Exe with .NET 10 (Native Windows GUI, No Console)
echo [INFO] Dang bien dich Project-Review.exe bang .NET 10 Native WebView2...
echo.

dotnet publish "%~dp0tools\ProjectReviewer\ProjectReviewer.csproj" -c Release -r win-x64 --self-contained false -o "%~dp0tools\ProjectReviewer\dist"

if errorlevel 1 (
    echo.
    echo [ERROR] Bien dich that bai! Vui long kiem tra log o tren.
    pause
    exit /b 1
)

:: 4. Move executable to root directory and cleanup temporary files
if exist "%~dp0tools\ProjectReviewer\dist\Project-Review.exe" (
    echo [INFO] Di chuyen Project-Review.exe ra thu muc goc...
    taskkill /F /IM Project-Review.exe >nul 2>&1
    copy /Y "%~dp0tools\ProjectReviewer\dist\Project-Review.exe" "%~dp0Project-Review.exe" >nul
)

echo [INFO] Don dep thu muc build tam thoi...
if exist "%~dp0tools\ProjectReviewer\dist" rmdir /S /Q "%~dp0tools\ProjectReviewer\dist"

echo.
echo ======================================================================
echo   [THANH CONG] Da tao Project-Review.exe .NET 10 Native thanh cong!
echo   - 100%% Chuan Windows 11 Fluent: Dark Slate Title Bar, khong bi mau Teal.
echo   - Nhan dien 100%% App Icon tai Taskbar, khong bi icon qua dia cau Edge.
echo   - Khong co popup dich thuat, khong bi thanh trinh duyet lam phien.
echo ======================================================================
echo.
if "%~1"=="" pause
