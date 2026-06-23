#!/bin/bash
echo "Installing dependencies..."
python -m pip install -r requirements.txt

echo ""
echo "Starting Pascal Kitchens Quote Studio..."
python app.py
