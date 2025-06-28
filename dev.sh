#!/bin/bash

# Simple development script for Medical Bot
# Quick start without extensive checks

echo "🚀 Starting Medical Bot Development Environment..."

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping services..."
    jobs -p | xargs -r kill
    echo "✅ Cleanup completed!"
}

# Setup trap for cleanup
trap cleanup EXIT INT TERM

# Start backend
echo "🔧 Starting backend on port 8000..."
cd backend
source ../venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found, using system Python"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
cd ..

# Start frontend
echo "📱 Starting frontend on port 3000..."
cd frontend
npm run dev &
cd ..

echo ""
echo "🎉 Services are starting..."
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait
