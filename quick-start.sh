#!/bin/bash

# MGNREGA Dashboard - Quick Start Script
# This script sets up and starts the entire application

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker is installed: $(docker --version)"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose is installed: $(docker-compose --version)"
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker."
        exit 1
    fi
    print_success "Docker daemon is running"
}

# Setup environment
setup_environment() {
    print_header "Setting Up Environment"
    
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from example..."
        cp .env.example .env
        print_success "Created .env file"
        print_warning "Please edit .env file with your configuration:"
        echo "  - Set DATA_GOV_API_KEY"
        echo "  - Set strong passwords for POSTGRES_PASSWORD and REDIS_PASSWORD"
        echo ""
        read -p "Press Enter to continue after editing .env file..."
    else
        print_success ".env file exists"
    fi
}

# Build containers
build_containers() {
    print_header "Building Docker Containers"
    
    echo "This may take a few minutes on first run..."
    docker-compose build
    print_success "Containers built successfully"
}

# Start services
start_services() {
    print_header "Starting Services"
    
    docker-compose up -d
    print_success "Services started"
    
    echo ""
    echo "Waiting for services to be ready..."
    sleep 10
}

# Initialize database
initialize_database() {
    print_header "Initializing Database"
    
    echo "Creating database schema..."
    docker-compose exec -T db psql -U postgres -d mgnrega < db/schema.sql 2>/dev/null || {
        print_warning "Schema might already exist, continuing..."
    }
    
    echo "Seeding sample data..."
    docker-compose exec backend python scripts/seed_data.py || {
        print_warning "Seeding failed or already done"
    }
    
    print_success "Database initialized"
}

# Check service health
check_health() {
    print_header "Checking Service Health"
    
    # Check backend
    if curl -s http://localhost:8000/api/v1/health > /dev/null; then
        print_success "Backend is healthy"
    else
        print_warning "Backend might still be starting up"
    fi
    
    # Check frontend
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "Frontend is accessible"
    else
        print_warning "Frontend might still be starting up"
    fi
    
    # Check database
    if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        print_success "Database is ready"
    else
        print_error "Database is not ready"
    fi
    
    # Check redis
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        print_success "Redis is ready"
    else
        print_warning "Redis might not be ready"
    fi
}

# Show access info
show_access_info() {
    print_header "Access Information"
    
    echo "Your MGNREGA Dashboard is now running!"
    echo ""
    echo "📱 Frontend:        http://localhost:3000"
    echo "🔧 Backend API:     http://localhost:8000"
    echo "📚 API Docs:        http://localhost:8000/api/docs"
    echo "🗄️  Database:       localhost:5432"
    echo "💾 Redis:           localhost:6379"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "To stop services:"
    echo "  docker-compose down"
    echo ""
    echo "To restart services:"
    echo "  docker-compose restart"
    echo ""
    print_success "Setup complete! Visit http://localhost:3000 to get started."
}

# Main execution
main() {
    print_header "MGNREGA Dashboard - Quick Start"
    
    check_prerequisites
    setup_environment
    build_containers
    start_services
    initialize_database
    
    echo ""
    echo "Waiting for all services to stabilize..."
    sleep 5
    
    check_health
    show_access_info
}

# Run main function
main
