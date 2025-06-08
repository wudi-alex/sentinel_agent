#!/usr/bin/env python3
"""
SentinelAgent - Main CLI Entry Point
Advanced Agent System Analysis & Monitoring Platform
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for the CLI"""
    from sentinelagent.core.cli import main as cli_main
    return cli_main()

# Import and run the CLI
if __name__ == "__main__":
    sys.exit(main() or 0)
