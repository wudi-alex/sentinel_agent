#!/usr/bin/env python3
"""
SentinelAgent - Main CLI Entry Point
Advanced Agent System Analysis & Monitoring Platform
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import and run the CLI
if __name__ == "__main__":
    from core.cli import main
    main()
