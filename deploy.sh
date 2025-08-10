#!/bin/bash

# Airline Market Demand Analyzer - Deployment Script
# This script provides multiple deployment options for the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="airline-analyzer"
PORT=8501
DOCKER_IMAGE="airline-analyzer:latest"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are available"
}

# Function to check if port is available
check_port() {
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
        print_warning "Port $PORT is already in use. Please stop the service using that port first."
        return 1
    fi
    return 0
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t $DOCKER_IMAGE .
    print_success "Docker image built successfully"
}

# Function to deploy with Docker Compose
deploy_docker_compose() {
    print_status "Deploying with Docker Compose..."
    
    if [ ! -f ".env" ]; then
        print_warning "No .env file found. Creating sample .env file..."
        cp env.example .env
        print_warning "Please update the .env file with your API keys before running the application."
    fi
    
    docker-compose up -d
    print_success "Application deployed successfully with Docker Compose"
    print_status "Access the application at: http://localhost:$PORT"
}

# Function to deploy with Docker run
deploy_docker_run() {
    print_status "Deploying with Docker run..."
    
    if [ ! -f ".env" ]; then
        print_warning "No .env file found. Creating sample .env file..."
        cp env.example .env
        print_warning "Please update the .env file with your API keys before running the application."
    fi
    
    docker run -d \
        --name $APP_NAME \
        -p $PORT:8501 \
        --env-file .env \
        --restart unless-stopped \
        $DOCKER_IMAGE
    
    print_success "Application deployed successfully with Docker run"
    print_status "Access the application at: http://localhost:$PORT"
}

# Function to deploy locally with Streamlit
deploy_local() {
    print_status "Deploying locally with Streamlit..."
    
    if [ ! -f ".env" ]; then
        print_warning "No .env file found. Creating sample .env file..."
        cp env.example .env
        print_warning "Please update the .env file with your API keys before running the application."
    fi
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run the application
    print_status "Starting Streamlit application..."
    print_success "Application deployed successfully locally"
    print_status "Access the application at: http://localhost:$PORT"
    
    streamlit run main.py --server.port=$PORT
}

# Function to stop the application
stop_app() {
    print_status "Stopping application..."
    
    # Try Docker Compose first
    if docker-compose ps | grep -q $APP_NAME; then
        docker-compose down
        print_success "Application stopped (Docker Compose)"
        return
    fi
    
    # Try Docker run
    if docker ps | grep -q $APP_NAME; then
        docker stop $APP_NAME
        docker rm $APP_NAME
        print_success "Application stopped (Docker run)"
        return
    fi
    
    print_warning "No running application found"
}

# Function to show logs
show_logs() {
    print_status "Showing application logs..."
    
    # Try Docker Compose first
    if docker-compose ps | grep -q $APP_NAME; then
        docker-compose logs -f
        return
    fi
    
    # Try Docker run
    if docker ps | grep -q $APP_NAME; then
        docker logs -f $APP_NAME
        return
    fi
    
    print_warning "No running application found"
}

# Function to show status
show_status() {
    print_status "Application status:"
    
    # Check Docker Compose
    if docker-compose ps | grep -q $APP_NAME; then
        print_success "Application is running with Docker Compose"
        docker-compose ps
        return
    fi
    
    # Check Docker run
    if docker ps | grep -q $APP_NAME; then
        print_success "Application is running with Docker run"
        docker ps | grep $APP_NAME
        return
    fi
    
    print_warning "Application is not running"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up..."
    
    # Stop and remove containers
    docker-compose down 2>/dev/null || true
    docker stop $APP_NAME 2>/dev/null || true
    docker rm $APP_NAME 2>/dev/null || true
    
    # Remove images
    docker rmi $DOCKER_IMAGE 2>/dev/null || true
    
    # Remove volumes
    docker volume prune -f
    
    print_success "Cleanup completed"
}

# Function to show help
show_help() {
    echo "Airline Market Demand Analyzer - Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker-compose    Deploy using Docker Compose (recommended)"
    echo "  docker-run        Deploy using Docker run"
    echo "  local             Deploy locally with Streamlit"
    echo "  stop              Stop the running application"
    echo "  logs              Show application logs"
    echo "  status            Show application status"
    echo "  cleanup           Clean up Docker resources"
    echo "  help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docker-compose    # Deploy with Docker Compose"
    echo "  $0 local             # Deploy locally"
    echo "  $0 stop              # Stop the application"
}

# Main script logic
main() {
    case "${1:-help}" in
        "docker-compose")
            check_docker
            check_port
            build_image
            deploy_docker_compose
            ;;
        "docker-run")
            check_docker
            check_port
            build_image
            deploy_docker_run
            ;;
        "local")
            check_port
            deploy_local
            ;;
        "stop")
            stop_app
            ;;
        "logs")
            show_logs
            ;;
        "status")
            show_status
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"
