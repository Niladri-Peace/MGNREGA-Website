@echo off
REM MGNREGA Dashboard - Quick Start Script for Windows

echo ========================================
echo MGNREGA Dashboard - Quick Start
echo ========================================
echo.

REM Check Docker
echo Checking prerequisites...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo [OK] Docker is installed

REM Check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed.
    echo Please install Docker Compose
    pause
    exit /b 1
)
echo [OK] Docker Compose is installed
echo.

REM Setup environment
echo ========================================
echo Setting Up Environment
echo ========================================
if not exist .env (
    echo [WARNING] .env file not found. Creating from example...
    copy .env.example .env
    echo [OK] Created .env file
    echo.
    echo Please edit .env file with your configuration:
    echo   - Set DATA_GOV_API_KEY
    echo   - Set strong passwords
    echo.
    pause
) else (
    echo [OK] .env file exists
)
echo.

REM Build containers
echo ========================================
echo Building Docker Containers
echo ========================================
echo This may take a few minutes...
docker-compose build
if errorlevel 1 (
    echo [ERROR] Failed to build containers
    pause
    exit /b 1
)
echo [OK] Containers built successfully
echo.

REM Start services
echo ========================================
echo Starting Services
echo ========================================
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)
echo [OK] Services started
echo.
echo Waiting for services to be ready...
timeout /t 15 /nobreak >nul
echo.

REM Initialize database
echo ========================================
echo Initializing Database
echo ========================================
echo Seeding sample data...
docker-compose exec -T backend python scripts/seed_data.py
echo [OK] Database initialized
echo.

REM Show access info
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Your MGNREGA Dashboard is now running!
echo.
echo Frontend:     http://localhost:3000
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/api/docs
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop services:
echo   docker-compose down
echo.
echo Visit http://localhost:3000 to get started!
echo.
pause
