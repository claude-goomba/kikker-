#!/bin/bash

echo "🐸 KIKKER BAND WEBSITE STARTER 🐸"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Make the script executable
chmod +x server.py

echo "Starting Kikker Band website..."
echo ""
echo "This will:"
echo "1. Start the website on http://localhost:8000"
echo "2. Automatically open your browser"
echo "3. Show admin panel at http://localhost:8000/admin.html"
echo ""
echo "⚠️  IMPORTANT: You also need to start the backend!"
echo "   In another terminal, run: ./start_backend.sh"
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Start the website server
python3 server.py