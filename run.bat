@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title GameMaster

where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python launcher was not found. Install Python 3.11+ and enable PATH.
  pause
  exit /b 1
)

if not exist "tools\official-scrcpy\scrcpy.exe" (
  echo [ERROR] Missing tools\official-scrcpy\scrcpy.exe
  echo Add the official matching Scrcpy client before running.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creating local virtual environment...
  py -3 -m venv .venv
  if errorlevel 1 goto :failed
)

call ".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
if errorlevel 1 goto :failed

set PYTHONPATH=%CD%\app;%CD%\src
python app\main.py
if errorlevel 1 goto :failed
exit /b 0

:failed
echo.
echo [ERROR] GameMaster did not start. Review the message above.
pause
exit /b 1
