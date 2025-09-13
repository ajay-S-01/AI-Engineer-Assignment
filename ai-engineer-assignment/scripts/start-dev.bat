@echo off
REM Development startup script for Windows

echo 🚀 Starting AI Engineer Assignment in development mode...

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found. Copying from env.example...
    copy env.example .env
    echo 📝 Please edit .env file with your API keys before continuing.
    echo Press Enter when ready...
    pause
)

REM Start backend
echo 🔧 Starting FastAPI backend...
cd backend
start "Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

REM Start frontend
echo 🎨 Starting React frontend...
cd ..\frontend
start "Frontend" cmd /k "npm start"

echo ✅ Development servers started!
echo 📊 Backend API: http://localhost:8000
echo 📊 Backend Docs: http://localhost:8000/docs
echo 🎨 Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
