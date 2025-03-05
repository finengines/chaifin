@echo off
REM Start script for the Chainlit application on Windows

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in the PATH
    exit /b 1
)

REM Check if the virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install or update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please edit the .env file to configure the application
)

REM Test the n8n connection
echo Testing n8n connection...
python test_n8n_connection.py

REM Start the Chainlit application
echo Starting Chainlit application...
chainlit run app.py -w

REM Deactivate the virtual environment when the application exits
call venv\Scripts\deactivate.bat 