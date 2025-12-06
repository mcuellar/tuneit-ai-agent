#!/bin/bash
# Setup script for TuneIt AI Agent

set -e

echo "==========================================="
echo "TuneIt AI Agent - Setup Script"
echo "==========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "Error: Python $required_version or higher is required"
    echo "Found: Python $python_version"
    exit 1
fi
echo "✓ Python $python_version found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Setup environment file
echo "Setting up environment configuration..."
if [ -f ".env" ]; then
    echo ".env file already exists"
else
    cp .env.example .env
    echo "✓ .env file created from .env.example"
    echo ""
    echo "⚠️  Please edit .env to configure your MCP server URL and other settings"
fi
echo ""

# Create watch directory
echo "Creating watch directory..."
mkdir -p job_descriptions
echo "✓ job_descriptions directory created"
echo ""

echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env to configure your MCP server URL"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the agent: python run.py"
echo ""
echo "For more information, see README.md"
