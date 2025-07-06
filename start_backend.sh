#!/bin/bash

echo "Starting Kikker Band Backend..."
echo "================================"

cd "$(dirname "$0")/backend"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""
echo "Starting server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the simplified backend (no external dependencies needed)
python3 app_simple.py