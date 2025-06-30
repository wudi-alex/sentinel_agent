# SentinelAgent Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: Minimum 2GB RAM (4GB+ recommended for large projects)
- **Storage**: 500MB+ free space

## Installation Methods

### Method 1: Package Installation (Recommended)

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd SentinelAgent
```

#### 2. Install as Editable Package
```bash
pip install -e .
```

This will:
- Install all dependencies from `requirements.txt`
- Create console entry points (`sentinelagent`, `sentinelagent-web`)
- Make the package available for import

#### 3. Verify Installation
```bash
sentinelagent --help
sentinelagent-web
```

### Method 2: Direct Dependencies

#### 1. Install Dependencies Only
```bash
pip install -r requirements.txt
```

#### 2. Use Module Paths
```bash
python -m sentinelagent.cli.main --help
python -m sentinelagent.cli.start_web_ui
```

### Method 3: Virtual Environment (Recommended for Development)

#### 1. Create Virtual Environment
```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\\Scripts\\activate
```

#### 2. Install in Virtual Environment
```bash
pip install -e .
```

#### 3. Deactivate When Done
```bash
deactivate
```

## Automated Installation

### Using the Install Script
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

The script will:
- Check Python version (3.8+ required)
- Optionally create a virtual environment
- Install dependencies
- Set permissions
- Provide usage instructions

## Docker Installation

### Quick Docker Setup
```bash
# Build image
docker build -t sentinelagent .

# Run container
docker run -p 5002:5002 sentinelagent
```

### Docker Compose (Production)
```bash
docker-compose up -d
```

See [Docker Deployment Guide](DOCKER_DEPLOYMENT.md) for details.

## Verification

### Test CLI Installation
```bash
# Test help system
sentinelagent --help

# Test scan functionality
sentinelagent . --output test_scan.json

# Clean up test
rm test_scan.json
```

### Test Web Interface
```bash
# Start web interface
sentinelagent-web

# Or using module path
python -m sentinelagent.cli.start_web_ui
```

Open browser to: http://localhost:5002

### Test Import
```python
# Test Python imports
python -c "from sentinelagent.core.scanner import scan_directory; print('✅ Import successful')"
```

## Troubleshooting

### Common Issues

#### "Command not found: sentinelagent"
**Problem**: Entry points not properly installed

**Solutions**:
```bash
# Reinstall as editable package
pip install -e .

# Or use module path
python -m sentinelagent.cli.main --help
```

#### "ModuleNotFoundError: No module named 'sentinelagent'"
**Problem**: Package not in Python path

**Solutions**:
```bash
# Install properly
pip install -e .

# Or check current directory
pwd  # Should be in SentinelAgent root

# Or add to path manually
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### "Permission denied" on scripts
**Problem**: Execute permissions not set

**Solution**:
```bash
chmod +x scripts/install.sh
chmod +x sentinelagent/cli/*.py
```

#### "Port already in use" for web interface
**Problem**: Port 5002 is occupied

**Solutions**:
```bash
# Check what's using the port
lsof -i :5002

# Kill the process (replace PID)
kill <PID>

# Or modify the port in the code
# Edit sentinelagent/web/app.py
```

#### Dependency conflicts
**Problem**: Package version conflicts

**Solutions**:
```bash
# Use virtual environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install -e .

# Or update pip and try again
pip install --upgrade pip
pip install -e .
```

### Platform-Specific Issues

#### macOS
```bash
# If you get SSL certificate errors
/Applications/Python\ 3.x/Install\ Certificates.command

# If command line tools missing
xcode-select --install
```

#### Windows
```bash
# If you get execution policy errors
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# If path issues persist
pip install -e . --user
```

#### Linux
```bash
# If you get permission errors
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# If system Python conflicts
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Development Setup

### For Contributors
```bash
# Clone with development dependencies
git clone <repository-url>
cd SentinelAgent

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (if configured)
pre-commit install

# Run tests
python -m pytest tests/
```

### IDE Setup

#### VS Code
1. Install Python extension
2. Set Python interpreter to virtual environment
3. Configure launch.json for debugging

#### PyCharm
1. Create new project from existing sources
2. Configure Python interpreter
3. Mark `sentinelagent` as sources root

## Updating

### Update Installation
```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -e .

# Or update specific packages
pip install -r requirements.txt --upgrade
```

### Migration Notes
- Check the project documentation for any updates
- Backup your data directory before major updates
- Test in development environment first

## Uninstallation

### Remove Package
```bash
pip uninstall sentinelagent
```

### Clean Virtual Environment
```bash
deactivate
rm -rf venv
```

### Remove Data (Optional)
```bash
# Remove analysis results
rm -rf data/generated_outputs/*

# Remove logs
rm -rf logs/*
```

## Support

If you encounter issues not covered here:
1. Check the [Issues](https://github.com/your-repo/SentinelAgent/issues) page
2. Review the [Documentation](README.md)
3. Create a new issue with detailed information

Include in bug reports:
- Operating system and version
- Python version (`python --version`)
- Installation method used
- Complete error message
- Steps to reproduce
