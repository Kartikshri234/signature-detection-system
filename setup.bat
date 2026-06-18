@echo off
echo ========================================
echo Signature Detection System - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python found: 
python --version
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo ✓ Node.js found: 
node --version
echo.

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✓ Python dependencies installed
echo.

REM Install Frontend dependencies
echo Installing frontend dependencies...
cd frontend
npm install
if errorlevel 1 (
    echo ✗ Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)
echo ✓ Frontend dependencies installed
cd ..
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo.
echo 1. Open Terminal 1 and run:
echo    python api.py
echo.
echo 2. Open Terminal 2 and run:
echo    cd frontend
echo    npm start
echo.
echo 3. Open your browser: http://localhost:3000
echo.
pause
