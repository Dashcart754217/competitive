@echo off
title Competitive Exam Quiz Bot Runner
color 0A

echo ========================================================
echo   COMPETITIVE EXAM QUIZ TELEGRAM BOT
echo   (UPSC, SSC, OPSC, OSSSC, NEET, JEE, OJEE, 10th/12th)
echo ========================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b
)

:: Install dependencies if needed
echo [1/3] Checking dependencies...
pip install -r requirements.txt --quiet

:: Seed database and initialize
echo [2/3] Initializing Question Bank and SQLite Database...
python -c "import database, seed_data; database.init_db(); seed_data.seed_database_if_empty()"

:: Prompt for BOT_TOKEN if not set in environment or config
if "%BOT_TOKEN%"=="" (
    echo.
    echo Tip: You can set BOT_TOKEN permanently in Windows or in config.py.
    set /p BOT_TOKEN="Enter your Telegram BOT_TOKEN: "
)

echo [3/3] Starting Bot Polling...
echo ========================================================
python bot.py
pause

