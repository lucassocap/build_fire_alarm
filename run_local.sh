#!/bin/bash
set -e

echo "🔥 Cicuma Fire: Starting Local Development Environment"

# 1. Check for Docker
echo "[1/3] Checking Docker Daemon..."
if ! docker info > /dev/null 2>&1; then
    echo " -> Docker is NOT running. Attempting to start Docker Desktop..."
    open -a Docker
    
    echo " -> Waiting for Docker to initialize (this may take a minute)..."
    # Loop until Docker is ready
    while ! docker info > /dev/null 2>&1; do
        printf "."
        sleep 2
    done
    echo ""
    echo " -> Docker is Active!"
else
    echo " -> Docker is already running."
fi

# 2. Build and Start
echo "[2/3] Building Containers..."
docker-compose build

# 3. Run
echo "[3/3] Starting Services..."
echo " -> Web: http://localhost:3000"
echo " -> Cortex: http://localhost:8001"
echo " -> Cell: http://localhost:8002"
docker-compose up
