# Local test script for main_pull.yml workflow (Windows PowerShell)

Write-Host "🚀 Starting local GitHub Actions simulation for main_pull.yml..." -ForegroundColor Green

# Load environment variables from .env file
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
    Write-Host "✅ Environment variables loaded from .env" -ForegroundColor Green
} else {
    Write-Host "❌ .env file not found. Please create it with your secrets." -ForegroundColor Red
    exit 1
}

# Check required environment variables
if (-not $env:DOCKER_USERNAME -or -not $env:PROJECT) {
    Write-Host "❌ Missing required environment variables: DOCKER_USERNAME or PROJECT" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Using DOCKER_USERNAME: $env:DOCKER_USERNAME" -ForegroundColor Yellow
Write-Host "📋 Using PROJECT: $env:PROJECT" -ForegroundColor Yellow

# Cleanup function
function Cleanup {
    Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
    docker stop $env:PROJECT 2>$null
    docker rm $env:PROJECT 2>$null
    Write-Host "✅ Cleanup completed!" -ForegroundColor Green
}

try {
    # Step 1: Checkout (already done since we're running locally)
    Write-Host "✅ Step 1: Checkout - Already in local repository" -ForegroundColor Green

    # Step 2: Build Docker image
    Write-Host "📦 Step 2: Building Docker image..." -ForegroundColor Yellow
    docker build --tag "$env:DOCKER_USERNAME/$env:PROJECT`:latest" .
    if ($LASTEXITCODE -ne 0) { throw "Docker build failed" }
    Write-Host "✅ Docker image built successfully" -ForegroundColor Green

    # Step 3: Run Docker container
    Write-Host "🏃 Step 3: Running Docker container..." -ForegroundColor Yellow
    docker run -d --name $env:PROJECT -p 80:3000 "$env:DOCKER_USERNAME/$env:PROJECT`:latest"
    if ($LASTEXITCODE -ne 0) { throw "Docker container failed to start" }
    Write-Host "✅ Docker container started successfully" -ForegroundColor Green

    # Wait for container to be ready
    Write-Host "⏳ Waiting for container to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

    # Check if container is running
    $containerStatus = docker ps --filter "name=$env:PROJECT" --format "{{.Names}}"
    if ($containerStatus -match $env:PROJECT) {
        Write-Host "✅ Container '$env:PROJECT' is running on http://localhost:80" -ForegroundColor Green
    } else {
        Write-Host "❌ Container failed to start properly" -ForegroundColor Red
        docker logs $env:PROJECT
        throw "Container startup failed"
    }

    # Step 4: Set up Python (simulate)
    Write-Host "🐍 Step 4: Setting up Python environment..." -ForegroundColor Yellow
    python --version
    if ($LASTEXITCODE -ne 0) { 
        Write-Host "❌ Python is not available" -ForegroundColor Red
        throw "Python not found"
    }
    Write-Host "✅ Python is available" -ForegroundColor Green

    # Step 5: Install Chromium browser (Windows note)
    Write-Host "🌐 Step 5: Browser check..." -ForegroundColor Yellow
    Write-Host "ℹ️  On Windows, please ensure Chrome is installed" -ForegroundColor Cyan

    # Step 6: Install Python packages
    Write-Host "📦 Step 6: Installing Python packages..." -ForegroundColor Yellow
    pip install requests webdriver-manager selenium pytest
    if ($LASTEXITCODE -ne 0) { throw "Failed to install Python packages" }
    Write-Host "✅ Python packages installed successfully" -ForegroundColor Green

    # Step 7: Run the Pytest script
    Write-Host "🧪 Step 7: Running Selenium tests..." -ForegroundColor Yellow
    $env:APP_URL = "http://localhost:80"
    $env:HEADLESS = "false"  # Set to true for headless mode
    pytest tests/selenium.py -v -s
    if ($LASTEXITCODE -ne 0) { throw "Tests failed" }
    Write-Host "✅ All tests passed!" -ForegroundColor Green

    Write-Host "🎉 All workflow steps completed successfully!" -ForegroundColor Green

} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Host "📋 Container logs:" -ForegroundColor Yellow
    docker logs $env:PROJECT 2>$null
    exit 1
} finally {
    Cleanup
}
