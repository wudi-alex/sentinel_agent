#!/usr/bin/env python3
"""
SentinelAgent Usage Examples
Demonstrates how to use scanning functionality
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sentinelagent.core.scanner import scan_directory, scan_file


def example_scan_crewai_project():
    """Example: Scan CrewAI project"""
    print("🔍 Example 1: Scan CrewAI Gmail project")
    print("-" * 50)
    
    # scancrewai_gmaildirectory
    target_dir = "../crewai_gmail"
    if Path(target_dir).exists():
        result = scan_directory(target_dir)
        print("✅ Scan completed")
        print(f"📊 Found: {result['scan_summary']['total_agents']} agents, {result['scan_summary']['total_tools']} tools")
    else:
        print(f"❌ Directory does not exist: {target_dir}")


def example_scan_autogen_project():
    """Example: Scan AutoGen project files"""
    print("\n🔍 Example 2: Scan AutoGen files")
    print("-" * 50)
    
    # scanautogenfile
    target_file = "../autogen_magneticone/autogen_remote_server_upload_file.py"
    if Path(target_file).exists():
        result = scan_file(target_file)
        print("✅ Scan completed")
        print(f"📊 Found: {len(result.get('agents', []))} agents, {len(result.get('tools', []))} tools")
    else:
        print(f"❌ File does not exist: {target_file}")


def demo_scan_current_project():
    """Example: Scan current project (sentinel)"""
    print("\n🔍 Example 3: Scan current SentinelAgent project")
    print("-" * 50)
    
    # Scan current directory
    current_dir = "."
    result = scan_directory(current_dir)
    print("✅ Self-scan completed")
    print(f"📊 Found: {result['scan_summary']['total_agents']} agents, {result['scan_summary']['total_tools']} tools")


if __name__ == "__main__":
    print("🚀 SentinelAgent Example Demonstration")
    print("=" * 50)
    
    try:
        # Run examples
        example_scan_crewai_project()
        example_scan_autogen_project()
        demo_scan_current_project()
        
        print("\n" + "=" * 50)
        print("🎉 All examples completed!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("💡 Please ensure required dependencies are installed: pip install -r requirements.txt")
