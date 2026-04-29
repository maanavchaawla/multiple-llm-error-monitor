@echo off
REM Force the terminal to stay in the exact folder where this .bat file lives
cd /d "%~dp0"

echo ==================================================
echo  Starting Enterprise LLM Error Monitor...
echo ==================================================
echo.

echo [1/2] Activating Virtual Environment...
IF EXIST "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) ELSE (
    echo [ERROR] Virtual environment 'venv' not found! Make sure this .bat file is in your project folder.
    pause
    exit /b
)

echo [2/2] Launching Python Daemon...
python monitor_daemon.py

echo.
echo ==================================================
echo Monitor has stopped or crashed. Press any key to close.
pause