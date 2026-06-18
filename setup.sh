#!/bin/bash

echo "========================================"
echo "Signature Detection System - Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org"
    exit 1
fi

echo "✓ Python found:"
python3 --version
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "✗ Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org"
    exit 1
fi

echo "✓ Node.js found:"
node --version
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "✗ Failed to install Python dependencies"
    exit 1
fi
echo "✓ Python dependencies installed"
echo ""

# Install Frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "✗ Failed to install frontend dependencies"
    cd ..
    exit 1
fi
echo "✓ Frontend dependencies installed"
cd ..
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo ""
echo "1. Open Terminal 1 and run:"
echo "   python3 api.py"
echo ""
echo "2. Open Terminal 2 and run:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser: http://localhost:3000"
echo ""
