#!/bin/bash
# Quick setup script for macOS/Linux

set -e

echo "🚀 Sales Insight Automator - Quick Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found. Please install Docker Desktop.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not found. Please install Docker Compose.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found${NC}"

# Create environment files
echo ""
echo "📝 Creating environment files..."

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
else
    echo -e "${YELLOW}⚠ backend/.env already exists, skipping${NC}"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✓ Created frontend/.env${NC}"
else
    echo -e "${YELLOW}⚠ frontend/.env already exists, skipping${NC}"
fi

# Instructions
echo ""
echo -e "${YELLOW}⚠️  Configuration Required${NC}"
echo "=========================================="
echo "Edit these files with your API keys:"
echo "1. backend/.env"
echo "   - GEMINI_API_KEY"
echo "   - SMTP_EMAIL & SMTP_PASSWORD"
echo ""
echo "2. frontend/.env"
echo "   - VITE_API_URL (if deploying)"
echo ""

# Start services
echo ""
echo "🐳 Building and starting services..."
docker-compose build
docker-compose up -d

# Wait for services
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check health
echo ""
echo "🔍 Checking service health..."

# Backend health
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
fi

echo ""
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "📱 Access the application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Next steps:"
echo "  1. Upload sales_q1_2026.csv in the frontend"
echo "  2. Enter your email address"
echo "  3. Check your inbox for the summary"
echo ""
echo "🛑 To stop services: docker-compose down"
echo ""
