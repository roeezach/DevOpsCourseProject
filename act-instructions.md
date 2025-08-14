# Instructions for using Act to run GitHub Actions locally

## Install Act

# Windows (using Chocolatey)

choco install act-cli

# macOS (using Homebrew)

brew install act

# Linux (using curl)

curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

## Create secrets file for Act

# Create .secrets file with your environment variables

echo "DOCKER_USERNAME=your-username" > .secrets
echo "PROJECT=your-project" >> .secrets

## Run the workflow

act pull_request -s .secrets

## Or run specific job

act -j test -s .secrets

## Run with verbose output

act pull_request -s .secrets -v
