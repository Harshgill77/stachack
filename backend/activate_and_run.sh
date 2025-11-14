#!/bin/bash

# Activate virtual environment and run the application
# This ensures dependencies are always available

echo ""
echo "========================================"
echo "🌾 CROP RECOMMENDATION SYSTEM"
echo "========================================"
echo ""

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
    echo ""
fi

# Check if dependencies are installed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 Installing missing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Check if Node is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install Node.js"
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "../frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd ../frontend
    npm install
    cd ../backend
    echo "✅ Frontend dependencies installed"
    echo ""
fi

# Start Flask backend
echo "📡 Starting Flask API server..."
python3 app/main.py &
BACKEND_PID=$!
sleep 3

# Start React frontend
echo "🎨 Starting React frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
cd ../backend

echo ""
echo "========================================"
echo "✅ SERVERS STARTED SUCCESSFULLY!"
echo "========================================"
echo ""
echo "📱 Frontend:    http://localhost:5173"
echo "🔌 Backend API: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for frontend
wait $FRONTEND_PID
cleanup
