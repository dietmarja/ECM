#!/bin/bash

echo "🚀 Starting ECM Web Interface for Localhost Testing"
echo "=================================================="

# Check if we're in the ECM directory
if [ ! -f "README.md" ] || [ ! -d "config" ]; then
    echo "❌ Please run this script from the ECM root directory"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install additional web dependencies if not in requirements.txt
pip install flask python-docx

# Check ECM components
echo "🔍 Checking ECM components..."
python3 -c "
try:
    import sys
    sys.path.append('analysis/scripts')
    from generate_curricula_toggle import EnhancedD4SCurriculumGenerator
    print('✅ ECM components available')
except ImportError as e:
    print(f'⚠️  ECM components not fully available: {e}')
    print('   The web interface will still work with limited functionality')
"

# Create web directory if it doesn't exist
mkdir -p web

# Start the web interface
echo ""
echo "🌐 Starting ECM Web Interface..."
echo "   Access at: http://localhost:5001"
echo "   Press Ctrl+C to stop"
echo ""

cd web
python3 app.py