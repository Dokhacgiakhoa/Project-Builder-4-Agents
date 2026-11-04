@echo off
title Lam moi bo nho dem Icon Windows Explorer
echo ======================================================================
echo   DANG LAM MOI ICON CACHE CUA WINDOWS EXPLORER...
echo ======================================================================
echo.
echo Dang dong tien trinh explorer.exe...
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 1 /nobreak >nul
echo Dang xoa cache cu...
del /f /q "%localappdata%\IconCache.db" >nul 2>&1
del /f /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*" >nul 2>&1
echo Dang khoi dong lai Windows Explorer...
start explorer.exe
echo.
echo ======================================================================
echo   [HOAN TAT] Explorer da duoc khoi dong lai voi Icon Cache moi!
echo ======================================================================
pause
