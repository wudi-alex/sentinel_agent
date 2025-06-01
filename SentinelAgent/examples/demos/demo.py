#!/usr/bin/env python3
"""
SentinelAgent - Simplified Demo Script
Demonstrates core scanning functionality
"""

import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sentinelagent.core.scanner import scan_directory


def print_banner():
    """printbanner"""
    print("=" * 50)
    print("🔍 SentinelAgent - System Structure Scanner")
    print("=" * 50)


def demo_scan_directory(target_dir):
    """Demonstrate directory scanning"""
    print(f"\n📂 Scanning directory: {target_dir}")
    print("-" * 50)
    
    if not Path(target_dir).exists():
        print(f"❌ Directory does not exist: {target_dir}")
        return

    # Use simplified scan function
    result = scan_directory(target_dir)
    
    # Display scan results
    summary = result['scan_summary']
    print(f"✅ Scan completed!")
    print(f"📊 Found: {summary['total_agents']} agents, {summary['total_tools']} tools, {summary['total_files']} files")
    
    # Detailed information
    if result['agents']:
        print(f"\n🤖 Found Agents (first 3):")
        for agent in result['agents'][:3]:  # Show first 3
            print(f"   - {agent['name']} ({agent['type']})")
    
    if result['tools']:
        print(f"\n🔧 Found Tools (first 3):")
        for tool in result['tools'][:3]:  # Show first 3
            print(f"   - {tool['name']} ({tool['type']})")
    
    # Save results
    output_file = f"scan_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    return output_file


def main():
    """Main function"""
    print_banner()
    
    # Available demo targets
    demo_targets = {
        '1': '../crewai_gmail',
        '2': '../autogen_magneticone', 
        '3': '.',  # Current directory
    }
    
    print("\n🎯 Please select a target to scan:")
    print("1. CrewAI Gmail project")
    print("2. AutoGen MagneticOne project")
    print("3. SentinelAgent project itself")
    print("4. Custom path")
    
    choice = input("\nPlease enter your choice (1-4): ").strip()
    
    if choice in demo_targets:
        target = demo_targets[choice]
    elif choice == '4':
        target = input("Please enter target path: ").strip()
    else:
        print("❌ Invalid choice")
        return
    
    # Execute scan
    output_file = demo_scan_directory(target)
    
    if output_file:
        print(f"\n🎉 Demo completed!")
        print(f"💡 Tip: Check the generated JSON file for complete scan results")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 User interrupted")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print(f"💡 Please check if the target path is correct")
