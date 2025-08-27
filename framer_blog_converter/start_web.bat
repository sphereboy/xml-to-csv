@echo off
REM Framer Blog XML to CSV Converter - Web Application Starter
REM This script starts the web interface for the converter

echo 🚀 Starting Framer Blog XML to CSV Converter...
echo 📱 Web interface will be available at: http://localhost:5000
echo 🔄 Press Ctrl+C to stop the server
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "run_web.py" (
    echo ❌ Please run this script from the framer_blog_converter directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if requirements are installed
if not exist "venv" if not exist ".venv" (
    echo ⚠️  No virtual environment detected
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the web application
echo ✅ Starting web server...
python run_web.py

pause
