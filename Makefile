.PHONY: help setup test lint format clean run deploy dev-env docker-up docker-down db-init db-migrate db-upgrade github-init github-push

# Colors for terminal output
YELLOW=\033[1;33m
NC=\033[0m # No Color
GREEN=\033[0;32m
RED=\033[0;31m

# Help command
help:
	@echo "$(GREEN)Volleyball Team Management System - Available commands:$(NC)"
	@echo "$(YELLOW)Development:$(NC)"
	@echo "  make setup      - Set up development environment"
	@echo "  make dev-env    - Start development environment with Docker"
	@echo "  make run        - Run development server"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean up generated files"
	@echo ""
	@echo "$(YELLOW)Database:$(NC)"
	@echo "  make db-init    - Initialize database"
	@echo "  make db-migrate - Create new migration"
	@echo "  make db-upgrade - Apply migrations"
	@echo ""
	@echo "$(YELLOW)Docker:$(NC)"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"
	@echo ""
	@echo "$(YELLOW)GitHub:$(NC)"
	@echo "  make github-init - Initialize GitHub repository"
	@echo "  make github-push - Push changes to GitHub"
	@echo ""
	@echo "$(YELLOW)Deployment:$(NC)"
	@echo "  make deploy     - Deploy to Render"

# Development setup
setup:
	@echo "$(GREEN)Setting up development environment...$(NC)"
	chmod +x scripts/setup_dev.sh
	./scripts/setup_dev.sh

# Run development server
run:
	@echo "$(GREEN)Starting development server...$(NC)"
	flask run

# Testing
test:
	@echo "$(GREEN)Running tests...$(NC)"
	pytest -v --cov=app --cov-report=term-missing

# Linting
lint:
	@echo "$(GREEN)Running linting checks...$(NC)"
	flake8 .
	mypy .
	black --check .
	isort --check-only .

# Code formatting
format:
	@echo "$(GREEN)Formatting code...$(NC)"
	black .
	isort .

# Cleanup
clean:
	@echo "$(GREEN)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +

# Database commands
db-init:
	@echo "$(GREEN)Initializing database...$(NC)"
	python init_db.py

db-migrate:
	@echo "$(GREEN)Creating new migration...$(NC)"
	flask db migrate -m "$(message)"

db-upgrade:
	@echo "$(GREEN)Applying migrations...$(NC)"
	flask db upgrade

# Docker commands
docker-up:
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	docker-compose up -d

docker-down:
	@echo "$(GREEN)Stopping Docker containers...$(NC)"
	docker-compose down

# Development environment
dev-env:
	@echo "$(GREEN)Starting development environment...$(NC)"
	docker-compose -f docker-compose.dev.yml up -d

# GitHub commands
github-init:
	@echo "$(GREEN)Initializing GitHub repository...$(NC)"
	chmod +x scripts/init_github.sh
	./scripts/init_github.sh

github-push:
	@echo "$(GREEN)Pushing changes to GitHub...$(NC)"
	git add .
	@if [ "$(message)" = "" ]; then \
		echo "$(RED)Error: Commit message required. Use 'make github-push message=\"Your commit message\"'$(NC)"; \
		exit 1; \
	fi
	git commit -m "$(message)"
	git push

# Deployment
deploy:
	@echo "$(GREEN)Deploying to Render...$(NC)"
	chmod +x scripts/deploy_render.sh
	./scripts/deploy_render.sh

# SSL certificates
ssl-certs:
	@echo "$(GREEN)Generating SSL certificates...$(NC)"
	chmod +x scripts/generate_ssl_certs.sh
	./scripts/generate_ssl_certs.sh

# Additional utility commands
install-deps:
	@echo "$(GREEN)Installing dependencies...$(NC)"
	pip install -r requirements.txt
	pip install -e ".[dev]"

update-deps:
	@echo "$(GREEN)Updating dependencies...$(NC)"
	pip install --upgrade -r requirements.txt
	pip install --upgrade -e ".[dev]"

check-security:
	@echo "$(GREEN)Running security checks...$(NC)"
	bandit -r app/
	safety check

generate-docs:
	@echo "$(GREEN)Generating documentation...$(NC)"
	sphinx-build -b html docs/source docs/build

# Continuous Integration
ci: lint test check-security
	@echo "$(GREEN)CI checks completed$(NC)"

# Create necessary directories
create-dirs:
	@echo "$(GREEN)Creating necessary directories...$(NC)"
	mkdir -p logs
	mkdir -p app/static/profile_pics
	mkdir -p app/static/uploads
	mkdir -p nginx/ssl
	touch app/static/profile_pics/.gitkeep
	touch app/static/uploads/.gitkeep
	touch nginx/ssl/.gitkeep

# Initialize project
init: create-dirs install-deps db-init ssl-certs
	@echo "$(GREEN)Project initialized successfully$(NC)"

# Complete setup with GitHub
setup-complete: setup github-init
	@echo "$(GREEN)Complete setup with GitHub finished successfully$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Review the GitHub repository"
	@echo "2. Set up project board and issues"
	@echo "3. Configure deployment settings"
	@echo "4. Start development!"
