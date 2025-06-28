@echo off
REM Medical Bot Application Startup Script for Windows
REM This script runs both frontend and backend services

setlocal enabledelayedexpansion

echo [INFO] Starting Medical Bot Application...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is required but not installed.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is required but not installed.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is required but not installed.
    pause
    exit /b 1
)

echo [INFO] Setting up backend...

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "..\venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv ..\venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call ..\venv\Scripts\activate.bat

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    if exist ".env.example" (
        echo [WARNING] No .env file found. Copying from .env.example...
        copy .env.example .env
        echo [WARNING] Please edit .env file with your API keys before running the application.
    ) else (
        echo [ERROR] No .env or .env.example file found!
        pause
        exit /b 1
    )
)

cd ..
echo [SUCCESS] Backend setup completed!

echo [INFO] Setting up frontend...

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing Node.js dependencies...
    npm install
)

cd ..
echo [SUCCESS] Frontend setup completed!

echo [INFO] Starting backend server...

REM Start backend in a new window
start "Medical Bot Backend" cmd /k "cd backend && ..\venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

echo [INFO] Starting frontend server...

REM Start frontend in a new window
start "Medical Bot Frontend" cmd /k "cd frontend && npm run dev"

echo [SUCCESS] Medical Bot Application is starting!
echo [SUCCESS] Frontend: http://localhost:3000
echo [SUCCESS] Backend API: http://localhost:8000
echo.
echo [INFO] Both services are starting in separate windows.
echo [INFO] Close the command windows to stop the services.
echo.
pause
