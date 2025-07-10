#!/bin/bash

echo "🚀 Starting ECM Web Interface v2.0 for Localhost Testing"
echo "========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the ECM directory
if [ ! -f "README.md" ] || [ ! -d "config" ]; then
    echo -e "${RED}❌ Please run this script from the ECM root directory${NC}"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${BLUE}🐍 Python version: $python_version${NC}"

if [[ $(echo "$python_version >= 3.8" | bc) -eq 0 ]]; then
    echo -e "${YELLOW}⚠️  Python 3.8+ recommended for best compatibility${NC}"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${BLUE}📥 Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📝 Creating .env file from template...${NC}"
    cp .env.example .env 2>/dev/null || echo "# Add your environment variables here" > .env
fi

# Check ECM components
echo -e "${BLUE}🔍 Checking ECM components...${NC}"
python3 -c "
try:
    import sys
    sys.path.append('analysis/scripts')
    from generate_curricula_toggle import EnhancedD4SCurriculumGenerator
    print('${GREEN}✅ ECM components available${NC}')
except ImportError as e:
    print('${YELLOW}⚠️  ECM components not fully available: ' + str(e) + '${NC}')
    print('   The web interface will still work with limited functionality')
except Exception as e:
    print('${RED}❌ Error checking ECM components: ' + str(e) + '${NC}')
"

# Create necessary directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p web/templates
mkdir -p output/curricula
mkdir -p logs
mkdir -p temp

# Check if Redis is available (for production features)
echo -e "${BLUE}🔍 Checking Redis availability...${NC}"
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✅ Redis available (enhanced caching enabled)${NC}"
    else
        echo -e "${YELLOW}⚠️  Redis not running (using memory cache)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Redis not installed (using memory cache)${NC}"
fi

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True

# Start the web interface
echo ""
echo -e "${GREEN}🌐 Starting ECM Web Interface v2.0...${NC}"
echo -e "${BLUE}   Features: CSRF Protection, Rate Limiting, Caching, Security Headers${NC}"
echo -e "${BLUE}   Access at: http://localhost:5001${NC}"
echo -e "${BLUE}   API Status: http://localhost:5001/api/v1/status${NC}"
echo -e "${BLUE}   Health Check: http://localhost:5001/health${NC}"
echo -e "${YELLOW}   Press Ctrl+C to stop${NC}"
echo ""

cd web
python3 app.py
