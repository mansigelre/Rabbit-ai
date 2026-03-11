@echo off
REM Quick setup script for Windows

cls
echo.
echo 🚀 Sales Insight Automator - Quick Setup
echo ==========================================
echo.

REM Check Docker
echo Checking prerequisites...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)
echo ✓ Docker found

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Docker Compose not found. Please install Docker Compose.
    pause
    exit /b 1
)
echo ✓ Docker Compose found

REM Create environment files
echo.
echo 📝 Creating environment files...

if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo ✓ Created backend\.env
) else (
    echo ⚠ backend\.env already exists, skipping
)

if not exist frontend\.env (
    copy frontend\.env.example frontend\.env
    echo ✓ Created frontend\.env
) else (
    echo ⚠ frontend\.env already exists, skipping
)

REM Instructions
echo.
echo ⚠️  Configuration Required
echo ==========================================
echo Edit these files with your API keys:
echo 1. backend\.env
echo    - GEMINI_API_KEY
echo    - SMTP_EMAIL ^& SMTP_PASSWORD
echo.
echo 2. frontend\.env
echo    - VITE_API_URL (if deploying)
echo.

REM Start services
echo.
echo 🐳 Building and starting services...
docker-compose build
docker-compose up -d

REM Wait for services
echo.
echo ⏳ Waiting for services to be ready...
timeout /t 5 /nobreak

echo.
echo ✓ Setup Complete!
echo ==========================================
echo.
echo 📱 Access the application:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo 📝 Next steps:
echo   1. Upload sales_q1_2026.csv in the frontend
echo   2. Enter your email address
echo   3. Check your inbox for the summary
echo.
echo 🛑 To stop services: docker-compose down
echo.
pause
