#!/bin/bash

echo ""
echo "========================================"
echo "🌾 CROP RECOMMENDATION SYSTEM"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+"
    exit 1
fi

# Check if Node is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install Node.js"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "../frontend/node_modules" ]; then
    echo "⚠️  Frontend dependencies not found."
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
echo "📝 Note: Location errors are normal and non-critical"
echo "   The app uses a fallback location if needed."
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

# Wait for frontend (it usually exits first)
wait $FRONTEND_PID
cleanup
