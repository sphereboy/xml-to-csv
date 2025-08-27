#!/bin/bash

# Framer Blog XML to CSV Converter - Web Application Starter
# This script starts the web interface for the converter

echo "🚀 Starting Framer Blog XML to CSV Converter..."
echo "📱 Web interface will be available at: http://localhost:5000"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "run_web.py" ]; then
    echo "❌ Please run this script from the framer_blog_converter directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Check if requirements are installed
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "⚠️  No virtual environment detected"
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Start the web application
echo "✅ Starting web server..."
python3 run_web.py
