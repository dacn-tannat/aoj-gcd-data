#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual environment created and dependencies installed."
else
    source venv/bin/activate
fi

# Run the main Python script
python src/main.py

# Deactivate the virtual environment
deactivate
