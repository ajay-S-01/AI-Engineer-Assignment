#!/bin/bash

# Development startup script

echo "🚀 Starting AI Engineer Assignment in development mode..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from env.example..."
    cp env.example .env
    echo "📝 Please edit .env file with your API keys before continuing."
    echo "Press Enter when ready..."
    read
fi

# Start backend
echo "🔧 Starting FastAPI backend..."
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend
echo "🎨 Starting React frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Development servers started!"
echo "📊 Backend API: http://localhost:8000"
echo "📊 Backend Docs: http://localhost:8000/docs"
echo "🎨 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user to stop
wait

# Cleanup
echo "🛑 Stopping servers..."
kill $BACKEND_PID $FRONTEND_PID
echo "✅ All servers stopped"
