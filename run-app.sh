#!/bin/bash

# Medical Bot Application Startup Script
# This script runs both frontend and backend services

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to kill process on port
kill_port() {
    local port=$1
    print_status "Killing process on port $port..."
    lsof -ti :$port | xargs kill -9 2>/dev/null || true
}

# Function to setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "../venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv ../venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source ../venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            print_warning "No .env file found. Copying from .env.example..."
            cp .env.example .env
            print_warning "Please edit .env file with your API keys before running the application."
        else
            print_error "No .env or .env.example file found!"
            return 1
        fi
    fi
    
    cd ..
    print_success "Backend setup completed!"
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
    fi
    
    cd ..
    print_success "Frontend setup completed!"
}

# Function to start backend
start_backend() {
    print_status "Starting backend server..."
    
    cd backend
    
    # Check if port 8000 is in use
    if port_in_use 8000; then
        print_warning "Port 8000 is already in use. Killing existing process..."
        kill_port 8000
        sleep 2
    fi
    
    # Activate virtual environment and start server
    source ../venv/bin/activate
    
    print_status "Backend server starting on http://localhost:8000"
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait for backend to start
    print_status "Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health >/dev/null 2>&1; then
            print_success "Backend server is running!"
            return 0
        fi
        sleep 1
    done
    
    print_error "Backend failed to start within 30 seconds"
    return 1
}

# Function to start frontend
start_frontend() {
    print_status "Starting frontend server..."
    
    cd frontend
    
    # Check if port 3000 is in use
    if port_in_use 3000; then
        print_warning "Port 3000 is already in use. Killing existing process..."
        kill_port 3000
        sleep 2
    fi
    
    print_status "Frontend server starting on http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!
    
    cd ..
    
    # Wait for frontend to start
    print_status "Waiting for frontend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 >/dev/null 2>&1; then
            print_success "Frontend server is running!"
            return 0
        fi
        sleep 1
    done
    
    print_error "Frontend failed to start within 30 seconds"
    return 1
}

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down servers..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Kill any remaining processes on our ports
    kill_port 8000
    kill_port 3000
    
    print_success "Cleanup completed!"
}

# Main function
main() {
    print_status "Starting Medical Bot Application..."
    
    # Check prerequisites
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed."
        exit 1
    fi
    
    if ! command_exists node; then
        print_error "Node.js is required but not installed."
        exit 1
    fi
    
    if ! command_exists npm; then
        print_error "npm is required but not installed."
        exit 1
    fi
    
    # Setup trap for cleanup
    trap cleanup EXIT INT TERM
    
    # Setup services
    setup_backend || exit 1
    setup_frontend || exit 1
    
    # Start services
    start_backend || exit 1
    start_frontend || exit 1
    
    print_success "🎉 Medical Bot Application is running!"
    print_success "📱 Frontend: http://localhost:3000"
    print_success "🔧 Backend API: http://localhost:8000"
    print_success "📚 API Documentation: http://localhost:8000/docs"
    print_success ""
    print_status "Press Ctrl+C to stop all services"
    
    # Wait for user to stop
    wait
}

# Run main function
main "$@"
