# SentinelAgent Directory Structure

This document describes the reorganized directory structure of SentinelAgent.

## Overview

The SentinelAgent project has been reorganized into a clean, maintainable structure that follows Python packaging best practices.

## Directory Structure

```
SentinelAgent/
├── sentinelagent/                 # Main Python package
│   ├── __init__.py               # Package initialization
│   ├── core/                     # Core functionality modules
│   │   ├── __init__.py
│   │   ├── scanner.py            # System scanning and file analysis
│   │   ├── inspector.py          # Code inspection and pattern detection
│   │   ├── graph_builder.py      # System graph construction
│   │   ├── path_analyzer.py      # Execution path analysis
│   │   └── log_analyzer.py       # Log analysis and anomaly detection
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py
│   │   ├── path_resolver.py      # Path resolution utilities
│   │   └── file_utils.py         # File handling utilities
│   ├── web/                      # Web interface
│   │   ├── __init__.py
│   │   ├── app.py                # Flask web application
│   │   ├── templates/            # HTML templates
│   │   │   └── index.html
│   │   └── static/               # Static assets
│   │       ├── css/
│   │       ├── js/
│   │       └── images/
│   └── cli/                      # Command-line interface
│       ├── __init__.py
│       ├── main.py               # Main CLI entry point
│       └── start_web_ui.py       # Web UI launcher
├── examples/                     # Usage examples
│   ├── example.py                # Basic usage examples
│   └── demos/                    # Demo scripts
│       ├── unified_demo.py       # Main comprehensive demo (start here)
│       ├── graph_demo.py         # Advanced graph analysis demo
│       ├── path_demo.py          # Security-focused path analysis demo
│       └── log_analysis_demo.py  # Specialized log analysis demo
├── docs/                         # Documentation
│   ├── DEMO_GUIDE.md             # Comprehensive demo guide and instructions
│   ├── PROJECT_REORGANIZATION_COMPLETE.md
│   ├── QUICK_START.md            # Quick start guide
│   └── deployment/               # Deployment documentation
│       └── DOCKER_DEPLOYMENT.md
├── scripts/                      # Utility scripts
│   ├── install.sh                # Installation script
│   ├── docker_build.sh           # Docker build script
│   └── docker_deploy.sh          # Docker deployment script
├── tests/                        # Test suite
├── config/                       # Configuration files
│   └── sentinel_agent.conf
├── data/                         # Data directory
│   ├── demo/                     # Demo data
│   ├── output/                   # Analysis output
│   └── uploads/                  # File uploads
├── setup.py                      # Python package setup
├── MANIFEST.in                   # Package manifest
├── requirements.txt              # Python dependencies
├── README.md                     # Project README
├── launch.py                     # Convenient launcher script
├── sentinel_agent                # Main executable entry point
├── Dockerfile                    # Docker configuration
└── docker-compose.yml           # Docker Compose configuration
```

## Key Changes Made

### 1. **Package Structure**
- Moved all source code into `sentinelagent/` package
- Added proper `__init__.py` files for Python imports
- Organized code into logical modules: `core`, `utils`, `web`, `cli`

### 2. **Entry Points**
- `launch.py` - Convenient launcher with multiple commands
- `sentinel_agent` - Main executable entry point
- `setup.py` - Proper Python package setup with console scripts

### 3. **Documentation Organization**
- Moved completion docs to `docs/`
- Organized deployment docs in `docs/deployment/`
- Kept README.md in project root

### 4. **Examples Organization**
- Basic examples in `examples/`
- Demo scripts organized in `examples/demos/`

### 5. **Import Path Updates**
- Updated all imports to use `sentinelagent.*` structure
- Fixed relative imports in Flask app
- Updated CLI scripts for new structure

## Usage

### Installation
```bash
# Install in development mode
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

### Running SentinelAgent

#### Method 1: Using the launcher script
```bash
# Start web UI
python launch.py web

# Scan a directory
python launch.py scan /path/to/analyze

# Run complete demo
python launch.py demo --type complete
```

#### Method 2: Using console scripts (after pip install)
```bash
# Start web UI
sentinelagent-web

# Use main CLI
sentinelagent
```

#### Method 3: Direct execution
```bash
# Start web UI
python sentinelagent/cli/start_web_ui.py

# Run main CLI
python sentinelagent/cli/main.py
```

### Importing in Python Code
```python
# Import core modules
from sentinelagent.core.scanner import scan_directory
from sentinelagent.core.graph_builder import build_graph
from sentinelagent.core.path_analyzer import analyze_paths

# Import utilities
from sentinelagent.utils.path_resolver import resolve_path
```

## Benefits of New Structure

1. **Clean Package Structure**: Follows Python packaging best practices
2. **Better Organization**: Logical separation of concerns
3. **Easier Installation**: Proper setup.py with console scripts
4. **Maintainable Imports**: Clear import paths
5. **Docker-Ready**: Still supports containerized deployment
6. **Development-Friendly**: Easy to extend and modify

## Migration Notes

- All old import paths have been updated
- Web UI still accessible on localhost:5002
- All demo functionality preserved
- Docker configuration still works
- No functional changes, only structural improvements

## Backup

A complete backup of the previous structure was created in:
`../SentinelAgent_backup_YYYYMMDD_HHMMSS/`

This allows reverting if needed while preserving the reorganization work.
