#!/bin/bash
# VPS Start & Auto-Restart Script

echo "========================================="
echo "   Starting Premium Userbot on VPS"
echo "========================================="

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found! Installing..."
    sudo apt update && sudo apt install -y python3 python3-pip ffmpeg git
fi

# Install requirements
echo "Installing requirements..."
pip3 install -r requirements.txt

# Run userbot
echo "Starting Userbot..."
python3 main.py
