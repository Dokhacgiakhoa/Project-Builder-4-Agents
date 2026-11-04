@echo off
setlocal enabledelayedexpansion

title Project Review - Architecture and System Design Auditor

echo ======================================================================
echo   UNIVERSAL PROJECT STARTER KIT - ARCHITECTURE AUDITOR
echo   Thanh Tra Kien Truc va Doi Chieu Chuan Muc [Zero-Token, Offline]
echo ======================================================================
echo.

:: 1. Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python tren he thong!
    echo Vui long cai dat Python 3.8 tro len de chay bo thanh tra kien truc.
    echo.
    if "%~1"=="" pause
    exit /b 1
)

:: 2. Execute Auditor Engine
echo [INFO] Dang khoi chay bo thanh tra kien truc scripts\project_auditor.py...
echo.

python "%~dp0scripts\project_auditor.py" "%~dp0."

set AUDIT_EXIT_CODE=%ERRORLEVEL%

echo.
if %AUDIT_EXIT_CODE% equ 0 (
    echo [THANH CONG] Du an dat tieu chuan kien truc san sang cho Production!
) else (
    echo [CHU Y] Du an con mot so diem can hoan thien theo bao cao.
)

echo.
echo ======================================================================
echo   [HUONG DAN SU DUNG CHO AI AGENT]
echo   1. Mo tep: PROJECT_REVIEW_REPORT.md vua duoc tao.
echo   2. Cuon xuong Muc 7, sao chep doan Prompt san co.
echo   3. Dan vao Claude Code, Cursor, hoac Antigravity de AI tu sua code!
echo ======================================================================
echo.

:: Pause only if executed by double-click from Explorer (no arguments)
if "%~1"=="" (
    pause
)

exit /b %AUDIT_EXIT_CODE%
