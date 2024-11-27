#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Volleyball System development environment...${NC}"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo -e "${RED}Error: Python version must be >= 3.8.0${NC}"
    echo -e "Current version: $python_version"
    exit 1
fi

# Create virtual environment
echo -e "\n${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "\n${GREEN}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "\n${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt
pip install -e ".[dev]"

# Create necessary directories
echo -e "\n${GREEN}Creating necessary directories...${NC}"
mkdir -p logs
mkdir -p app/static/profile_pics
mkdir -p app/static/uploads
mkdir -p nginx/ssl

# Generate SSL certificates for development
echo -e "\n${GREEN}Generating SSL certificates for development...${NC}"
bash scripts/generate_ssl_certs.sh

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "\n${GREEN}Creating .env file...${NC}"
    cat > .env << EOL
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/volleyball_db
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_USE_TLS=false
MAIL_USERNAME=null
MAIL_PASSWORD=null
EOL
fi

# Initialize git hooks
echo -e "\n${GREEN}Setting up git hooks...${NC}"
cat > .git/hooks/pre-commit << EOL
#!/bin/bash
echo "Running pre-commit checks..."

# Run tests
python -m pytest

# Run linting
flake8 .

# Run type checking
mypy .

# Run code formatting check
black --check .
EOL

chmod +x .git/hooks/pre-commit

# Initialize database
echo -e "\n${GREEN}Initializing database...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker detected. Starting PostgreSQL container...${NC}"
    docker run --name volleyball-postgres \
        -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_DB=volleyball_db \
        -p 5432:5432 \
        -d postgres:13-alpine
    
    # Wait for PostgreSQL to start
    sleep 5
fi

# Run database migrations
echo -e "\n${GREEN}Running database migrations...${NC}"
flask db upgrade

# Initialize development data
echo -e "\n${GREEN}Initializing development data...${NC}"
python init_db.py

# Start development services
echo -e "\n${GREEN}Starting development services...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${YELLOW}Starting development containers...${NC}"
    docker-compose -f docker-compose.dev.yml up -d
fi

echo -e "\n${GREEN}Development environment setup complete!${NC}"
echo -e "\nTo start developing:"
echo -e "1. Activate virtual environment: ${YELLOW}source venv/bin/activate${NC}"
echo -e "2. Start the development server: ${YELLOW}flask run${NC}"
echo -e "\nAdditional development tools:"
echo -e "- Run tests: ${YELLOW}pytest${NC}"
echo -e "- Run linting: ${YELLOW}flake8${NC}"
echo -e "- Format code: ${YELLOW}black .${NC}"
echo -e "- Type checking: ${YELLOW}mypy .${NC}"
echo -e "\nDevelopment URLs:"
echo -e "- Application: ${YELLOW}http://localhost:5000${NC}"
echo -e "- MailHog (email testing): ${YELLOW}http://localhost:8025${NC}"
echo -e "- PgAdmin: ${YELLOW}http://localhost:5050${NC}"
echo -e "\n${GREEN}Happy coding!${NC}"

# Create docker-compose.dev.yml if it doesn't exist
if [ ! -f docker-compose.dev.yml ]; then
    echo -e "\n${GREEN}Creating docker-compose.dev.yml...${NC}"
    cat > docker-compose.dev.yml << EOL
version: '3.8'

services:
  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    depends_on:
      - db

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
EOL
fi

# Add git ignore rules for development
echo -e "\n${GREEN}Updating .gitignore for development...${NC}"
cat >> .gitignore << EOL

# Development
.env
.venv
*.pyc
__pycache__/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.DS_Store
*.sqlite
*.db
logs/
app/static/profile_pics/*
!app/static/profile_pics/.gitkeep
app/static/uploads/*
!app/static/uploads/.gitkeep
nginx/ssl/*
!nginx/ssl/.gitkeep
EOL

echo -e "\n${GREEN}Setup complete! Your development environment is ready.${NC}"
