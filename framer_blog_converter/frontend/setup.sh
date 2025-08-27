#!/bin/bash

echo "🚀 Setting up Framer Blog Converter Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    echo "   Please update Node.js from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Build the project
echo "🔨 Building the project..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully"
    echo ""
    echo "🎉 Frontend is ready for deployment!"
    echo ""
    echo "Next steps:"
    echo "1. Deploy your Python backend (api_app.py) to Render/Railway/Heroku"
    echo "2. Update the API URLs in pages/index.tsx with your backend URL"
    echo "3. Deploy to Netlify using the netlify.toml configuration"
    echo ""
    echo "📁 Build output is in: framer_blog_converter/frontend/out/"
else
    echo "❌ Build failed"
    exit 1
fi
