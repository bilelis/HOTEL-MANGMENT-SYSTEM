#!/bin/bash

# Hotel Management System - Setup Script
# This script sets up the complete Hotel Management System

set -e

echo "🏨 Hotel Management System Setup"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ from https://nodejs.org/"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.9+ from https://python.org/"
        exit 1
    fi
    
    # Check PostgreSQL
    if ! command -v psql &> /dev/null; then
        print_error "PostgreSQL is not installed. Please install PostgreSQL 12+ from https://postgresql.org/"
        exit 1
    fi
    
    print_success "All requirements are installed"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Create .env file
    print_status "Creating environment configuration..."
    cp env.example .env
    
    print_warning "Please edit backend/.env with your database credentials"
    
    cd ..
    print_success "Backend setup completed"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Create .env file
    print_status "Creating environment configuration..."
    cp env.example .env
    
    cd ..
    print_success "Frontend setup completed"
}

# Setup database
setup_database() {
    print_status "Setting up database..."
    
    # Create database
    print_status "Creating PostgreSQL database..."
    createdb hotel_management 2>/dev/null || print_warning "Database 'hotel_management' might already exist"
    
    # Run database setup
    print_status "Running database setup..."
    psql -d hotel_management -f database/setup.sql
    
    # Insert seed data
    print_status "Inserting seed data..."
    psql -d hotel_management -f database/seed_data.sql
    
    print_success "Database setup completed"
}

# Create startup scripts
create_startup_scripts() {
    print_status "Creating startup scripts..."
    
    # Backend startup script
    cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
python -m app.main
EOF
    chmod +x start-backend.sh
    
    # Frontend startup script
    cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run dev
EOF
    chmod +x start-frontend.sh
    
    # Full system startup script
    cat > start-system.sh << 'EOF'
#!/bin/bash
echo "Starting Hotel Management System..."
echo "Backend will start on http://localhost:8000"
echo "Frontend will start on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Start backend in background
cd backend
source venv/bin/activate
python -m app.main &
BACKEND_PID=$!

# Start frontend in background
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
EOF
    chmod +x start-system.sh
    
    print_success "Startup scripts created"
}

# Main setup function
main() {
    echo ""
    print_status "Starting Hotel Management System setup..."
    echo ""
    
    # Check requirements
    check_requirements
    
    # Setup backend
    setup_backend
    echo ""
    
    # Setup frontend
    setup_frontend
    echo ""
    
    # Setup database
    setup_database
    echo ""
    
    # Create startup scripts
    create_startup_scripts
    echo ""
    
    # Final instructions
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit backend/.env with your database credentials"
    echo "2. Start the system: ./start-system.sh"
    echo "3. Or start individually:"
    echo "   - Backend: ./start-backend.sh"
    echo "   - Frontend: ./start-frontend.sh"
    echo ""
    echo "Access the application:"
    echo "- Frontend: http://localhost:3000"
    echo "- Backend API: http://localhost:8000"
    echo "- API Documentation: http://localhost:8000/docs"
    echo ""
    echo "Demo credentials:"
    echo "- Admin: admin / admin123"
    echo "- Reception: reception / reception123"
    echo "- Cashier: cashier / cashier123"
    echo ""
    print_success "Hotel Management System is ready to use!"
}

# Run main function
main "$@"
