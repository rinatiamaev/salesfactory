#!/bin/bash
# Run script for the AI Catalog Service

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create it from .env.example"
    echo "cp .env.example .env"
    exit 1
fi

# Run the application
echo "Starting AI Catalog Service..."
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
