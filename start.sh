#!/bin/bash

# Start script for the Chainlit application

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in the PATH"
    exit 1
fi

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install or update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit the .env file to configure the application"
fi

# Test the n8n connection
echo "Testing n8n connection..."
python test_n8n_connection.py

# Start the Chainlit application
echo "Starting Chainlit application..."
chainlit run app.py -w

# Deactivate the virtual environment when the application exits
deactivate 