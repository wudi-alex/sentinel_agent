#!/usr/bin/env python3
"""
Watchdog - Main CLI Entry Point
Agent System Analysis Tool
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
    from src.cli import main
    main()
