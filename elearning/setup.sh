#!/bin/bash

# eLearning Platform Setup Script
# This script sets up the Django e-learning platform

set -e  # Exit on error

echo "========================================"
echo "eLearning Platform Setup"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}Python $python_version detected${NC}"

# Install requirements
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}Dependencies installed!${NC}"

# Create media directory if it doesn't exist
echo -e "\n${YELLOW}Creating media directories...${NC}"
mkdir -p media/profile_pics
mkdir -p media/course_materials
echo -e "${GREEN}Media directories created!${NC}"

# Run migrations
echo -e "\n${YELLOW}Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}Database migrations completed!${NC}"

# Collect static files
echo -e "\n${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}Static files collected!${NC}"

# Check if Redis is installed
echo -e "\n${YELLOW}Checking Redis installation...${NC}"
if command -v redis-server &> /dev/null; then
    echo -e "${GREEN}Redis is installed${NC}"

    # Check if Redis is running
    if pgrep -x "redis-server" > /dev/null; then
        echo -e "${GREEN}Redis is already running${NC}"
    else
        echo -e "${YELLOW}Starting Redis server...${NC}"
        redis-server --daemonize yes
        sleep 2
        if pgrep -x "redis-server" > /dev/null; then
            echo -e "${GREEN}Redis server started successfully${NC}"
        else
            echo -e "${RED}Failed to start Redis server${NC}"
        fi
    fi
else
    echo -e "${RED}Redis is not installed!${NC}"
    echo -e "${YELLOW}Please install Redis:${NC}"
    echo "  macOS: brew install redis"
    echo "  Ubuntu: sudo apt-get install redis-server"
    echo -e "${YELLOW}Or run without chat functionality${NC}"
fi

# Create superuser prompt
echo -e "\n${YELLOW}========================================"
echo "Setup Complete!"
echo "========================================${NC}"
echo ""
echo "To create a superuser account, run:"
echo "  python manage.py createsuperuser"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "For production deployment with WebSocket support:"
echo "  daphne -p 8000 elearning.asgi:application"
echo ""
echo -e "${GREEN}Happy Learning!${NC}"

