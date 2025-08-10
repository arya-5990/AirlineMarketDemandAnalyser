@echo off
setlocal enabledelayedexpansion

REM Airline Market Demand Analyzer - Windows Deployment Script
REM This script provides deployment options for Windows users

set "APP_NAME=airline-analyzer"
set "PORT=8501"
set "DOCKER_IMAGE=airline-analyzer:latest"

REM Function to print colored output
:print_status
echo [INFO] %~1
goto :eof

:print_success
echo [SUCCESS] %~1
goto :eof

:print_warning
echo [WARNING] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

REM Function to check if Docker is installed
:check_docker
docker --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not installed. Please install Docker Desktop first."
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker Compose is not installed. Please install Docker Desktop first."
    exit /b 1
)

call :print_success "Docker and Docker Compose are available"
goto :eof

REM Function to check if port is available
:check_port
netstat -an | find ":%PORT%" >nul
if not errorlevel 1 (
    call :print_warning "Port %PORT% is already in use. Please stop the service using that port first."
    exit /b 1
)
goto :eof

REM Function to build Docker image
:build_image
call :print_status "Building Docker image..."
docker build -t %DOCKER_IMAGE% .
if errorlevel 1 (
    call :print_error "Failed to build Docker image"
    exit /b 1
)
call :print_success "Docker image built successfully"
goto :eof

REM Function to deploy with Docker Compose
:deploy_docker_compose
call :print_status "Deploying with Docker Compose..."

if not exist ".env" (
    call :print_warning "No .env file found. Creating sample .env file..."
    copy env.example .env >nul
    call :print_warning "Please update the .env file with your API keys before running the application."
)

docker-compose up -d
if errorlevel 1 (
    call :print_error "Failed to deploy with Docker Compose"
    exit /b 1
)

call :print_success "Application deployed successfully with Docker Compose"
call :print_status "Access the application at: http://localhost:%PORT%"
goto :eof

REM Function to deploy with Docker run
:deploy_docker_run
call :print_status "Deploying with Docker run..."

if not exist ".env" (
    call :print_warning "No .env file found. Creating sample .env file..."
    copy env.example .env >nul
    call :print_warning "Please update the .env file with your API keys before running the application."
)

docker run -d --name %APP_NAME% -p %PORT%:8501 --env-file .env --restart unless-stopped %DOCKER_IMAGE%
if errorlevel 1 (
    call :print_error "Failed to deploy with Docker run"
    exit /b 1
)

call :print_success "Application deployed successfully with Docker run"
call :print_status "Access the application at: http://localhost:%PORT%"
goto :eof

REM Function to deploy locally with Streamlit
:deploy_local
call :print_status "Deploying locally with Streamlit..."

if not exist ".env" (
    call :print_warning "No .env file found. Creating sample .env file..."
    copy env.example .env >nul
    call :print_warning "Please update the .env file with your API keys before running the application."
)

REM Check if virtual environment exists
if not exist "venv" (
    call :print_status "Creating virtual environment..."
    python -m venv venv
    if errorlevel 1 (
        call :print_error "Failed to create virtual environment"
        exit /b 1
    )
)

REM Activate virtual environment
call :print_status "Activating virtual environment..."
call venv\Scripts\activate.bat

REM Install dependencies
call :print_status "Installing dependencies..."
pip install -r requirements.txt
if errorlevel 1 (
    call :print_error "Failed to install dependencies"
    exit /b 1
)

REM Run the application
call :print_status "Starting Streamlit application..."
call :print_success "Application deployed successfully locally"
call :print_status "Access the application at: http://localhost:%PORT%"

streamlit run main.py --server.port=%PORT%
goto :eof

REM Function to stop the application
:stop_app
call :print_status "Stopping application..."

REM Try Docker Compose first
docker-compose ps | find "%APP_NAME%" >nul
if not errorlevel 1 (
    docker-compose down
    call :print_success "Application stopped (Docker Compose)"
    goto :eof
)

REM Try Docker run
docker ps | find "%APP_NAME%" >nul
if not errorlevel 1 (
    docker stop %APP_NAME%
    docker rm %APP_NAME%
    call :print_success "Application stopped (Docker run)"
    goto :eof
)

call :print_warning "No running application found"
goto :eof

REM Function to show logs
:show_logs
call :print_status "Showing application logs..."

REM Try Docker Compose first
docker-compose ps | find "%APP_NAME%" >nul
if not errorlevel 1 (
    docker-compose logs -f
    goto :eof
)

REM Try Docker run
docker ps | find "%APP_NAME%" >nul
if not errorlevel 1 (
    docker logs -f %APP_NAME%
    goto :eof
)

call :print_warning "No running application found"
goto :eof

REM Function to show status
:show_status
call :print_status "Application status:"

REM Check Docker Compose
docker-compose ps | find "%APP_NAME%" >nul
if not errorlevel 1 (
    call :print_success "Application is running with Docker Compose"
    docker-compose ps
    goto :eof
)

REM Check Docker run
docker ps | find "%APP_NAME%" >nul
if not errorlevel 1 (
    call :print_success "Application is running with Docker run"
    docker ps | find "%APP_NAME%"
    goto :eof
)

call :print_warning "Application is not running"
goto :eof

REM Function to clean up
:cleanup
call :print_status "Cleaning up..."

REM Stop and remove containers
docker-compose down >nul 2>&1
docker stop %APP_NAME% >nul 2>&1
docker rm %APP_NAME% >nul 2>&1

REM Remove images
docker rmi %DOCKER_IMAGE% >nul 2>&1

REM Remove volumes
docker volume prune -f >nul 2>&1

call :print_success "Cleanup completed"
goto :eof

REM Function to show help
:show_help
echo Airline Market Demand Analyzer - Windows Deployment Script
echo.
echo Usage: %0 [OPTION]
echo.
echo Options:
echo   docker-compose    Deploy using Docker Compose (recommended)
echo   docker-run        Deploy using Docker run
echo   local             Deploy locally with Streamlit
echo   stop              Stop the running application
echo   logs              Show application logs
echo   status            Show application status
echo   cleanup           Clean up Docker resources
echo   help              Show this help message
echo.
echo Examples:
echo   %0 docker-compose    # Deploy with Docker Compose
echo   %0 local             # Deploy locally
echo   %0 stop              # Stop the application
goto :eof

REM Main script logic
if "%1"=="" goto show_help
if "%1"=="docker-compose" (
    call :check_docker
    call :check_port
    call :build_image
    call :deploy_docker_compose
    goto :eof
)
if "%1"=="docker-run" (
    call :check_docker
    call :check_port
    call :build_image
    call :deploy_docker_run
    goto :eof
)
if "%1"=="local" (
    call :check_port
    call :deploy_local
    goto :eof
)
if "%1"=="stop" (
    call :stop_app
    goto :eof
)
if "%1"=="logs" (
    call :show_logs
    goto :eof
)
if "%1"=="status" (
    call :show_status
    goto :eof
)
if "%1"=="cleanup" (
    call :cleanup
    goto :eof
)
if "%1"=="help" goto show_help

REM Invalid option
call :print_error "Invalid option: %1"
call :show_help
exit /b 1
