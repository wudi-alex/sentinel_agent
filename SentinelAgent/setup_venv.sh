#!/bin/bash
# SentinelAgent Virtual Environment Setup Script
# This script creates and configures a Python virtual environment for SentinelAgent

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="SentinelAgent"
VENV_NAME="venv"
PYTHON_VERSION="python3"

echo -e "${BLUE}🤖 ${PROJECT_NAME} Virtual Environment Setup${NC}"
echo "=============================================="

# Check if Python 3 is available
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo -e "${RED}❌ Error: $PYTHON_VERSION is not installed or not in PATH${NC}"
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Get Python version
PYTHON_VER=$($PYTHON_VERSION --version 2>&1)
echo -e "${GREEN}✅ Found: $PYTHON_VER${NC}"

# Check if virtual environment already exists
if [ -d "$VENV_NAME" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment '$VENV_NAME' already exists${NC}"
    read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🗑️  Removing existing virtual environment...${NC}"
        rm -rf $VENV_NAME
    else
        echo -e "${BLUE}ℹ️  Using existing virtual environment${NC}"
        source $VENV_NAME/bin/activate
        echo -e "${GREEN}✅ Virtual environment activated${NC}"
        exit 0
    fi
fi

# Create virtual environment
echo -e "${BLUE}📦 Creating virtual environment '$VENV_NAME'...${NC}"
$PYTHON_VERSION -m venv $VENV_NAME

# Activate virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source $VENV_NAME/bin/activate

# Upgrade pip
echo -e "${BLUE}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Install wheel and setuptools
echo -e "${BLUE}⚙️  Installing build tools...${NC}"
pip install wheel setuptools

# Install requirements
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}📋 Installing project dependencies...${NC}"
    pip install -r requirements.txt
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, skipping dependency installation${NC}"
fi

# Install the project in development mode
if [ -f "setup.py" ]; then
    echo -e "${BLUE}🔧 Installing ${PROJECT_NAME} in development mode...${NC}"
    pip install -e .
else
    echo -e "${YELLOW}⚠️  setup.py not found, skipping project installation${NC}"
fi

# Display success message and instructions
echo -e "${GREEN}🎉 Virtual environment setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📖 Usage Instructions:${NC}"
echo -e "  ${GREEN}Activate:${NC}   source venv/bin/activate"
echo -e "  ${GREEN}Deactivate:${NC} deactivate"
echo ""
echo -e "${BLUE}🚀 Quick Start:${NC}"
echo "  source venv/bin/activate"
echo "  sentinelagent-web"
echo ""
echo -e "${YELLOW}💡 Tip: The virtual environment is ready to use!${NC}"
