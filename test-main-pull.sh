#!/bin/bash
# Local test script for main_pull.yml workflow

set -e  # Exit on any error

echo "🚀 Starting local GitHub Actions simulation for main_pull.yml..."

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "❌ .env file not found. Please create it with your secrets."
    exit 1
fi

# Check required environment variables
if [ -z "$DOCKER_USERNAME" ] || [ -z "$PROJECT" ]; then
    echo "❌ Missing required environment variables: DOCKER_USERNAME or PROJECT"
    exit 1
fi

echo "📋 Using DOCKER_USERNAME: $DOCKER_USERNAME"
echo "📋 Using PROJECT: $PROJECT"

# Cleanup function
cleanup() {
    echo "🧹 Cleaning up..."
    docker stop $PROJECT 2>/dev/null || true
    docker rm $PROJECT 2>/dev/null || true
    echo "✅ Cleanup completed!"
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Step 1: Checkout (already done since we're running locally)
echo "✅ Step 1: Checkout - Already in local repository"

# Step 2: Build Docker image
echo "📦 Step 2: Building Docker image..."
docker build --tag $DOCKER_USERNAME/$PROJECT:latest .
if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Step 3: Run Docker container
echo "🏃 Step 3: Running Docker container..."
docker run -d --name $PROJECT -p 80:3000 $DOCKER_USERNAME/$PROJECT:latest
if [ $? -eq 0 ]; then
    echo "✅ Docker container started successfully"
else
    echo "❌ Docker container failed to start"
    exit 1
fi

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 10

# Check if container is running
if docker ps | grep -q $PROJECT; then
    echo "✅ Container '$PROJECT' is running on http://localhost:80"
else
    echo "❌ Container failed to start properly"
    docker logs $PROJECT
    exit 1
fi

# Step 4: Set up Python (simulate)
echo "🐍 Step 4: Setting up Python environment..."
python3 --version
if [ $? -eq 0 ]; then
    echo "✅ Python is available"
else
    echo "❌ Python is not available"
    exit 1
fi

# Step 5: Install Chromium browser (Linux only)
echo "🌐 Step 5: Installing Chromium browser..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update && sudo apt-get install -y chromium-browser
    echo "✅ Chromium browser installed"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "ℹ️  On macOS, please ensure Chrome is installed"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "ℹ️  On Windows, please ensure Chrome is installed"
fi

# Step 6: Install Python packages
echo "📦 Step 6: Installing Python packages..."
pip install requests webdriver-manager selenium pytest
if [ $? -eq 0 ]; then
    echo "✅ Python packages installed successfully"
else
    echo "❌ Failed to install Python packages"
    exit 1
fi

# Step 7: Run the Pytest script
echo "🧪 Step 7: Running Selenium tests..."
export APP_URL="http://localhost:80"
export HEADLESS="false"  # Set to true for headless mode
pytest tests/selenium.py -v -s
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed"
    exit 1
fi

echo "🎉 All workflow steps completed successfully!"
