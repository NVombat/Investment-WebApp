#!/bin/bash
echo "[STARTING-SERVER] [PORT] 8000"

echo "Running application..."

#STARTING APPLICATION
python3 back.py &

echo "Running Flask Server [8000]"