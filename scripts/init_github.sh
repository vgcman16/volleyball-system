#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Initializing GitHub repository for Volleyball System...${NC}"

# Check if gh (GitHub CLI) is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI (gh) is not installed.${NC}"
    echo -e "${YELLOW}Please install it first:${NC}"
    echo "  - macOS: brew install gh"
    echo "  - Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    echo "  - Windows: winget install GitHub.cli"
    exit 1
fi

# Check if user is authenticated with GitHub
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}Please authenticate with GitHub first:${NC}"
    gh auth login
fi

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo -e "\n${GREEN}Initializing git repository...${NC}"
    git init
fi

# Create GitHub repository
echo -e "\n${GREEN}Creating GitHub repository...${NC}"
gh repo create volleyball-system --public --description "A comprehensive Flask-based volleyball team management system" --source=. --remote=origin

# Add all files
echo -e "\n${GREEN}Adding files to repository...${NC}"
git add .

# Create initial commit
echo -e "\n${GREEN}Creating initial commit...${NC}"
git commit -m "Initial commit: Volleyball Team Management System

- Authentication system with user roles
- Mobile-responsive UI using Bootstrap 5
- Email notification system
- Database integration with PostgreSQL
- Docker containerization
- Testing framework
- Development and deployment scripts"

# Create development branch
echo -e "\n${GREEN}Creating development branch...${NC}"
git checkout -b development

# Push to GitHub
echo -e "\n${GREEN}Pushing to GitHub...${NC}"
git push -u origin main
git push -u origin development

# Create initial project board
echo -e "\n${GREEN}Creating project board...${NC}"
gh project create "Volleyball System Development" --owner "@me" --public

# Create initial milestone
echo -e "\n${GREEN}Creating initial milestone...${NC}"
gh api \
  --method POST \
  -H "Accept: application/vnd.github.v3+json" \
  /repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/milestones \
  -f title='v1.0.0 Release' \
  -f description='Initial release of the Volleyball Team Management System' \
  -f due_on='2024-03-01T00:00:00Z'

# Create initial issues
echo -e "\n${GREEN}Creating initial issues...${NC}"

# Function to create an issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    gh issue create --title "$title" --body "$body" --label "$labels"
}

# Create issues for remaining modules
create_issue "Implement Team Management Module" "
- Team creation and roster management
- Team achievements tracking
- Equipment management
- Scrapbook entries" "enhancement,high priority"

create_issue "Implement Game Management Module" "
- Game scheduling and tracking
- Game MVP system
- Player game statistics
- Real-time score updates
- Tournament tracking" "enhancement,high priority"

create_issue "Implement Practice Management Module" "
- Practice session scheduling
- Attendance tracking
- Player progress monitoring
- Performance metrics" "enhancement,high priority"

create_issue "Implement Communication System" "
- Team announcements with attachments
- Announcement acknowledgment tracking
- Messaging system
- Internal communication tools" "enhancement,medium priority"

create_issue "Implement Broadcasting Features" "
- Live broadcast statistics
- Broadcast chat functionality
- Reaction system
- Mobile broadcast support" "enhancement,medium priority"

create_issue "Implement Analytics & Statistics" "
- Player performance metrics
- Team statistics
- Season progress tracking
- Historical data analysis
- Comparative analytics" "enhancement,medium priority"

# Create branch protection rules
echo -e "\n${GREEN}Setting up branch protection rules...${NC}"
gh api \
  --method PUT \
  -H "Accept: application/vnd.github.v3+json" \
  /repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":["tests"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions=null

# Create GitHub Actions workflow
echo -e "\n${GREEN}Setting up GitHub Actions...${NC}"
mkdir -p .github/workflows

# Create CI workflow
cat > .github/workflows/ci.yml << EOL
name: CI

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main, development ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        pytest
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        
    - name: Run linting
      run: |
        flake8 .
        black --check .
        mypy .
EOL

# Final push
echo -e "\n${GREEN}Pushing final changes...${NC}"
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions workflow"
git push

echo -e "\n${GREEN}GitHub repository setup complete!${NC}"
echo -e "\nRepository URL: $(gh repo view --json url -q .url)"
echo -e "Project board: $(gh repo view --json url -q .url)/projects/1"
echo -e "\nNext steps:"
echo "1. Review and update branch protection rules"
echo "2. Set up project board columns and automation"
echo "3. Review and assign initial issues"
echo "4. Set up deployment secrets in GitHub"
