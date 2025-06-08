#!/bin/bash
# SentinelAgent Installation Script

echo "🤖 SentinelAgent Installation Starting..."
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python version check passed: $python_version"
else
    echo "❌ Python version too low, requires 3.8+, current version: $python_version"
    exit 1
fi

# Create virtual environment (optional)
read -p "Create virtual environment? (y/n): " create_venv
if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created successfully"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Dependencies installation failed"
    exit 1
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p data/{output,uploads,demo}
mkdir -p logs
echo "✅ Directories created successfully"

# Set permissions (if installed as editable package)
chmod +x sentinelagent/cli/start_web_ui.py
chmod +x sentinelagent/cli/main.py

echo ""
echo "🎉 SentinelAgent installation completed!"
echo "=================================="
echo ""
echo "🚀 Launch methods:"
echo "  Web interface: python -m sentinelagent.cli.start_web_ui"
echo "  Command line: python -m sentinelagent.cli.main --help"
echo ""
echo "🔧 Alternative (after pip install -e .):"
echo "  Web interface: sentinelagent-web"
echo "  Command line: sentinelagent --help"
echo ""
echo "📍 Web access URL: http://localhost:5002"
echo ""
echo "📚 More info: docs/QUICK_START.md"
