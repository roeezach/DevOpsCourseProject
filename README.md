# DevOps Final Project - CI/CD Pipeline Implementation

## 📋 Project Overview

This project demonstrates a complete DevOps CI/CD pipeline implementation for a web application using modern DevOps practices and tools. The project includes automated testing, containerization, and deployment workflows using GitHub Actions and Docker.

**Course**: DevOps Course - Colman College  
**Project Type**: Final Project  
**Application**: Currency Converter Web App

## Architecture

```
DevOpsCourseProject/
├── app/                    # Application source code
│   ├── index.js           # Node.js server
│   └── public/            # Static files
│       ├── index.html     # Frontend
│       └── style.css      # Styling
├── tests/                 # Test suite
│   └── selenium.py        # Selenium automated tests
├── .github/workflows/     # CI/CD pipelines
│   ├── main_pull.yml      # Testing workflow (PR)
│   └── workflow.yml       # Build & Deploy workflow
├── docker-compose.yaml    # Container orchestration
├── Dockerfile            # Container configuration
└── package.json          # Dependencies
```

## 🚀 Features

### Application Features

- **Currency Converter**: Convert Israeli Shekels to USD, EUR, and GBP
- **Real-time Conversion**: Live currency conversion with current rates
- **Responsive Design**: Works on desktop and mobile devices
- **User-friendly Interface**: Clean and intuitive UI

### DevOps Features

- **Automated Testing**: Selenium-based end-to-end tests
- **Containerization**: Docker containers for consistent environments
- **CI/CD Pipeline**: GitHub Actions workflows for automation
- **Pull Request Testing**: Automated testing on every PR
- **Deployment Automation**: Automated deployment to production

## 🛠️ Technology Stack

### Frontend & Backend

- **Node.js**: Server-side JavaScript runtime
- **Express.js**: Web framework
- **HTML/CSS**: Frontend technologies
- **JavaScript**: Client-side scripting

### DevOps & Testing

- **Docker**: Containerization platform
- **GitHub Actions**: CI/CD automation
- **Selenium**: Web automation testing
- **Python**: Test automation scripting
- **pytest**: Testing framework

### Deployment

- **Docker Hub**: Container registry
- **SSH**: Secure deployment
- **Docker Compose**: Multi-container orchestration

## 📊 CI/CD Pipeline

### Testing Pipeline (`main_pull.yml`)

**Triggers**: Pull requests to main branch

```yaml
1. Build Docker image
2. Run container on port 80
3. Set up Python environment
4. Install test dependencies
5. Run Selenium tests
6. Generate test reports
7. Clean up containers
```

### Deployment Pipeline (`workflow.yml`)

**Triggers**: Push to main branch

```yaml
1. Build Docker image
2. Push to Docker Hub
3. Deploy to production server
4. Health checks
5. Rollback if needed
```

## 🔧 Local Development

### Prerequisites

- Node.js 14+ installed
- Docker and Docker Compose
- Python 3.9+ (for tests)
- Git

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/roeezach/DevOpsCourseProject.git
cd DevOpsCourseProject
```

2. **Install dependencies**

```bash
npm install
```

3. **Run locally**

```bash
npm start
# or
node app/index.js
```

4. **Run with Docker**

```bash
docker-compose up -d
```

5. **Run tests**

```bash
# Install test dependencies
pip install selenium pytest webdriver-manager

# Run tests
pytest tests/selenium.py -v
```

## 🔐 Environment Variables

### Required Secrets (GitHub)

```
DOCKER_USERNAME    # Docker Hub username
DOCKER_PASSWORD    # Docker Hub password/token
PROJECT           # Project name
HOST              # Production server IP
USER              # Server username
SSH_KEY           # SSH private key
PORT              # SSH port (default: 22)
```

**Live Application**: [Currency Converter](http://your-production-url.com)  
**Docker Image**: [rif7/currency-converter](https://hub.docker.com/r/rif7/currency-converter)
