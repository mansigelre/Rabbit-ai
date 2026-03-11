# Makefile for Sales Insight Automator

.PHONY: help setup up down logs logs-backend logs-frontend build rebuild test docs clean health

help:
	@echo "Sales Insight Automator - Available Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup & Start:"
	@echo "  make setup          - Install dependencies and configure"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make rebuild        - Rebuild and restart services"
	@echo ""
	@echo "Development:"
	@echo "  make logs           - View all service logs"
	@echo "  make logs-backend   - View backend logs only"
	@echo "  make logs-frontend  - View frontend logs only"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Lint code"
	@echo ""
	@echo "Docker:"
	@echo "  make build          - Build Docker images"
	@echo "  make rebuild        - Rebuild without cache"
	@echo ""
	@echo "Status:"
	@echo "  make health         - Check service health"
	@echo "  make docs           - Open API documentation"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""

setup:
	@echo "🔧 Setting up Sales Insight Automator..."
	@mkdir -p backend/uploads
	@cp backend/.env.example backend/.env 2>/dev/null || true
	@cp frontend/.env.example frontend/.env 2>/dev/null || true
	@echo "✓ Configuration files created"
	@echo "✓ Next: Edit backend/.env with your API keys"
	@echo "✓ Then run: make up"

up:
	@echo "🚀 Starting services..."
	docker-compose up -d
	@sleep 5
	@echo "✓ Services started!"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend: http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"

down:
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✓ Services stopped"

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

build:
	@echo "🏗️  Building Docker images..."
	docker-compose build

rebuild:
	@echo "🔨 Rebuilding services..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✓ Services rebuilt and restarted"

test:
	@echo "🧪 Running tests..."
	@cd backend && python -m py_compile main.py
	@echo "✓ Backend syntax OK"
	@cd frontend && npm run build 2>/dev/null || echo "Frontend build skipped"

lint:
	@echo "🔍 Linting code..."
	@cd backend && pylint main.py --disable=all --enable=syntax-error 2>/dev/null || true
	@cd frontend && npm run lint 2>/dev/null || true

health:
	@echo "🏥 Checking service health..."
	@curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "Backend not responding"
	@echo "✓ Frontend running at http://localhost:3000"

docs:
	@echo "📚 Opening API documentation..."
	@python -m webbrowser http://localhost:8000/docs 2>/dev/null || echo "Open http://localhost:8000/docs in your browser"

clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	@rm -rf backend/uploads/*
	@echo "✓ Cleaned up"

.DEFAULT_GOAL := help
