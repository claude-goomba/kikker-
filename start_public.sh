#!/bin/bash

echo "🌐 KIKKER BAND - PUBLIC WEBSITE STARTER 🌐"
echo "============================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "🐸 Starting Kikker Band website publicly..."
echo ""

# Kill any existing processes on these ports
echo "Cleaning up existing processes..."
pkill -f "python3 server.py" 2>/dev/null || true
pkill -f "python3 app_simple.py" 2>/dev/null || true
pkill -f "./ngrok" 2>/dev/null || true

echo "Starting backend server..."
cd backend
python3 app_simple.py &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 2

echo "Starting website server..."
python3 server.py &
WEBSITE_PID=$!

# Wait a bit for website to start
sleep 2

echo "Starting ngrok tunnel..."
./ngrok http 8000 --log=stdout &
NGROK_PID=$!

echo ""
echo "🎉 KIKKER WEBSITE IS NOW PUBLIC! 🎉"
echo "====================================="
echo ""
echo "⏳ Getting public URL... (wait ~10 seconds)"
echo ""

# Wait for ngrok to fully start
sleep 10

# Get the public URL
echo "🔗 YOUR PUBLIC LINKS:"
echo "====================="

# Try to get ngrok URL via API
PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'tunnels' in data and len(data['tunnels']) > 0:
        print(data['tunnels'][0]['public_url'])
    else:
        print('Please check ngrok manually at http://127.0.0.1:4040')
except:
    print('Please check ngrok manually at http://127.0.0.1:4040')
" 2>/dev/null)

if [[ $PUBLIC_URL == http* ]]; then
    echo "🌐 Main Website: $PUBLIC_URL"
    echo "🛠️  Admin Panel: $PUBLIC_URL/admin.html"
    echo ""
    echo "📋 Share these links with anyone!"
    echo "🎫 They can buy tickets directly from the website"
    echo "📊 Use admin panel to manage events and view orders"
else
    echo "🌐 Check your public URL at: http://127.0.0.1:4040"
    echo "📋 The website should be accessible via the ngrok URL"
fi

echo ""
echo "📊 Monitoring Dashboard: http://127.0.0.1:4040"
echo ""
echo "💡 TIPS:"
echo "- Backend API: http://localhost:5000"
echo "- Local website: http://localhost:8000"
echo "- Ngrok dashboard: http://127.0.0.1:4040"
echo ""
echo "⚠️  IMPORTANT:"
echo "- Keep this terminal open to maintain the public link"
echo "- The ngrok URL changes each time you restart"
echo "- For permanent URL, sign up for ngrok account"
echo ""
echo "Press Ctrl+C to stop all servers and close public access"
echo "==========================================================="

# Function to cleanup when script exits
cleanup() {
    echo ""
    echo "🛑 Stopping all servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $WEBSITE_PID 2>/dev/null || true
    kill $NGROK_PID 2>/dev/null || true
    pkill -f "python3 server.py" 2>/dev/null || true
    pkill -f "python3 app_simple.py" 2>/dev/null || true
    pkill -f "./ngrok" 2>/dev/null || true
    echo "🐸 Kikker website stopped. Goodbye!"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Wait indefinitely
while true; do
    sleep 1
done