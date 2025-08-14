#!/bin/bash
# Docker-based testing that simulates the GitHub Actions environment

echo "🚀 Running GitHub Actions simulation in Docker..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo "❌ .env file not found"
    exit 1
fi

# Create a temporary container to run tests
docker run --rm \
  -v "$(pwd):/workspace" \
  -w /workspace \
  -e DOCKER_USERNAME=$DOCKER_USERNAME \
  -e PROJECT=$PROJECT \
  -e APP_URL=http://localhost:80 \
  -e HEADLESS=true \
  --privileged \
  --net=host \
  ubuntu:22.04 \
  bash -c "
    # Update package list
    apt-get update
    
    # Install Docker
    apt-get install -y docker.io
    
    # Install Python
    apt-get install -y python3 python3-pip
    
    # Install Chromium
    apt-get install -y chromium-browser
    
    # Install Python packages
    pip3 install requests webdriver-manager selenium pytest
    
    # Build Docker image
    docker build --tag \$DOCKER_USERNAME/\$PROJECT:latest .
    
    # Run container
    docker run -d --name \$PROJECT -p 80:3000 \$DOCKER_USERNAME/\$PROJECT:latest
    
    # Wait for container
    sleep 10
    
    # Run tests
    pytest tests/selenium.py -v -s
    
    # Cleanup
    docker stop \$PROJECT || true
    docker rm \$PROJECT || true
  "
