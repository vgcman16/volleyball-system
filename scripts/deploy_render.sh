#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Volleyball System deployment to Render...${NC}"

# Check if render-cli is installed
if ! command -v render &> /dev/null; then
    echo -e "${YELLOW}render-cli not found. Installing...${NC}"
    curl -o render https://render.com/download/cli
    chmod +x render
    sudo mv render /usr/local/bin/
fi

# Check for required environment variables
echo -e "${GREEN}Checking environment variables...${NC}"

required_vars=(
    "DATABASE_URL"
    "SECRET_KEY"
    "MAIL_SERVER"
    "MAIL_PORT"
    "MAIL_USE_TLS"
    "MAIL_USERNAME"
    "MAIL_PASSWORD"
)

missing_vars=()
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo -e "${RED}Error: Missing required environment variables:${NC}"
    printf '%s\n' "${missing_vars[@]}"
    echo -e "${YELLOW}Please set these variables in your Render dashboard or export them locally.${NC}"
    exit 1
fi

# Create render.yaml if it doesn't exist
if [ ! -f render.yaml ]; then
    echo -e "${YELLOW}Creating render.yaml configuration file...${NC}"
    cat > render.yaml << EOL
services:
  - type: web
    name: volleyball-system
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: DATABASE_URL
        fromDatabase:
          name: volleyball-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
    autoDeploy: true
    healthCheckPath: /health

databases:
  - name: volleyball-db
    databaseName: volleyball_db
    user: volleyball_user
    plan: starter

staticSites:
  - name: volleyball-static
    buildCommand: mkdir -p dist && cp -r app/static/* dist/
    publishPath: dist
    pullRequestPreviewsEnabled: true
EOL
fi

# Prepare the application
echo -e "${GREEN}Preparing application for deployment...${NC}"

# Create necessary directories
mkdir -p logs
mkdir -p app/static/profile_pics
mkdir -p app/static/uploads

# Run database migrations
echo -e "${GREEN}Running database migrations...${NC}"
flask db upgrade

# Collect static files
echo -e "${GREEN}Collecting static files...${NC}"
mkdir -p dist
cp -r app/static/* dist/

# Deploy to Render
echo -e "${GREEN}Deploying to Render...${NC}"
render deploy

# Check deployment status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Deployment successful!${NC}"
    echo -e "${GREEN}Your application should be available at: https://volleyball-system.onrender.com${NC}"
    echo -e "${YELLOW}Note: It may take a few minutes for the application to be fully available.${NC}"
    
    echo -e "\n${GREEN}Post-deployment steps:${NC}"
    echo "1. Set up your custom domain in the Render dashboard"
    echo "2. Configure SSL certificates"
    echo "3. Set up monitoring and alerts"
    echo "4. Review security settings"
    echo "5. Set up backup schedules for your database"
else
    echo -e "${RED}Deployment failed. Please check the error messages above.${NC}"
    exit 1
fi

# Additional checks
echo -e "\n${GREEN}Running post-deployment checks...${NC}"

# Check database connection
echo -e "Checking database connection..."
python3 << EOL
from app import create_app, db
app = create_app('production')
with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
EOL

# Check email configuration
echo -e "Checking email configuration..."
python3 << EOL
from app import create_app
from flask_mail import Mail
app = create_app('production')
with app.app_context():
    try:
        mail = Mail(app)
        print("Email configuration successful!")
    except Exception as e:
        print(f"Email configuration failed: {e}")
EOL

echo -e "\n${GREEN}Deployment process completed!${NC}"
echo -e "${YELLOW}Please check the Render dashboard for more details and monitoring.${NC}"
