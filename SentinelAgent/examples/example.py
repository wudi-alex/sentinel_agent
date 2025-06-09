#!/usr/bin/env python3
"""
SentinelAgent Usage Examples
Focused demonstration on CrewAI Gmail and AutoGen MagneticOne projects
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sentinelagent.core.scanner import scan_directory, scan_file


def display_scan_results(result: Dict[str, Any], title: str):
    """Helper function to display scan results in a formatted way"""
    print(f"\n📊 {title} Results:")
    print("-" * 60)
    
    # Summary
    summary = result.get('scan_summary', {})
    print(f"📁 Files scanned: {summary.get('total_files', 0)}")
    print(f"🤖 Agents found: {summary.get('total_agents', 0)}")
    print(f"🔧 Tools found: {summary.get('total_tools', 0)}")
    print(f"⚠️  Security issues: {summary.get('security_issues', 0)}")
    
    # Agents details
    agents = result.get('agents', [])
    if agents:
        print(f"\n🤖 Agent Details ({len(agents)} found):")
        for i, agent in enumerate(agents, 1):
            print(f"  {i}. {agent.get('name', 'Unknown')}")
            print(f"     Type: {agent.get('type', 'Unknown')}")
            print(f"     Role: {agent.get('role', 'Not specified')}")
            if agent.get('file'):
                print(f"     File: {agent['file']}")
    
    # Tools details
    tools = result.get('tools', [])
    if tools:
        print(f"\n🔧 Tool Details ({len(tools)} found):")
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool.get('name', 'Unknown')}")
            print(f"     Type: {tool.get('type', 'Unknown')}")
            if tool.get('description'):
                print(f"     Description: {tool['description']}")
            if tool.get('file'):
                print(f"     File: {tool['file']}")
    
    # Security issues
    security_issues = result.get('security_issues', [])
    if security_issues:
        print(f"\n⚠️  Security Issues ({len(security_issues)} found):")
        for i, issue in enumerate(security_issues, 1):
            print(f"  {i}. {issue.get('type', 'Unknown')}: {issue.get('description', 'No description')}")
            if issue.get('file'):
                print(f"     File: {issue['file']}")
            if issue.get('line'):
                print(f"     Line: {issue['line']}")


def example_crewai_gmail_comprehensive():
    """Comprehensive analysis of CrewAI Gmail project"""
    print("🔍 CrewAI Gmail Project Analysis")
    print("=" * 60)
    
    target_dir = "/Users/xuhe/Documents/agent_experiments/crewai_gmail"
    
    if not Path(target_dir).exists():
        print(f"❌ Directory does not exist: {target_dir}")
        print("💡 Please ensure the crewai_gmail project exists in the expected location")
        return
    
    print(f"📂 Scanning directory: {target_dir}")
    
    # Full directory scan
    result = scan_directory(target_dir)
    display_scan_results(result, "CrewAI Gmail Project")
    
    # Individual file analysis
    key_files = [
        "crewai_mail_test.py",
        "tools.py", 
        "google_service_utils.py",
        "Attack_Paths.py"
    ]
    
    print(f"\n🔍 Individual File Analysis:")
    print("-" * 60)
    
    for filename in key_files:
        file_path = Path(target_dir) / filename
        if file_path.exists():
            print(f"\n📄 Analyzing {filename}...")
            file_result = scan_file(str(file_path))
            
            # Brief summary for each file
            agents_count = len(file_result.get('agents', []))
            tools_count = len(file_result.get('tools', []))
            security_count = len(file_result.get('security_issues', []))
            
            print(f"   🤖 Agents: {agents_count}")
            print(f"   🔧 Tools: {tools_count}")
            print(f"   ⚠️  Security: {security_count}")
            
            # Show specific findings for important files
            if filename == "tools.py" and file_result.get('tools'):
                print("   📋 Tools found:")
                for tool in file_result['tools']:
                    print(f"      - {tool.get('name', 'Unknown')} ({tool.get('type', 'Unknown')})")
        else:
            print(f"   ❌ File not found: {filename}")


def example_autogen_magneticone_comprehensive():
    """Comprehensive analysis of AutoGen MagneticOne project"""
    print("\n🔍 AutoGen MagneticOne Project Analysis")
    print("=" * 60)
    
    target_dir = "/Users/xuhe/Documents/agent_experiments/autogen_magneticone"
    
    if not Path(target_dir).exists():
        print(f"❌ Directory does not exist: {target_dir}")
        print("💡 Please ensure the autogen_magneticone project exists in the expected location")
        return
    
    print(f"📂 Scanning directory: {target_dir}")
    
    # Full directory scan
    result = scan_directory(target_dir)
    display_scan_results(result, "AutoGen MagneticOne Project")
    
    # Individual file analysis
    key_files = [
        "autogen_remote_server_upload_file.py",
        "payload.py",
        "forbiden_web_server.py"
    ]
    
    print(f"\n🔍 Individual File Analysis:")
    print("-" * 60)
    
    for filename in key_files:
        file_path = Path(target_dir) / filename
        if file_path.exists():
            print(f"\n📄 Analyzing {filename}...")
            file_result = scan_file(str(file_path))
            
            # Brief summary for each file
            agents_count = len(file_result.get('agents', []))
            tools_count = len(file_result.get('tools', []))
            security_count = len(file_result.get('security_issues', []))
            
            print(f"   🤖 Agents: {agents_count}")
            print(f"   🔧 Tools: {tools_count}")
            print(f"   ⚠️  Security: {security_count}")
            
            # Show security issues for payload.py (likely to have them)
            if filename == "payload.py" and file_result.get('security_issues'):
                print("   🚨 Security issues found:")
                for issue in file_result['security_issues']:
                    print(f"      - {issue.get('type', 'Unknown')}: {issue.get('description', 'No description')}")
        else:
            print(f"   ❌ File not found: {filename}")


def save_detailed_results():
    """Save detailed scan results to JSON files for further analysis"""
    print("\n💾 Saving Detailed Results")
    print("=" * 60)
    
    # Define target directories
    targets = {
        "crewai_gmail": "/Users/xuhe/Documents/agent_experiments/crewai_gmail",
        "autogen_magneticone": "/Users/xuhe/Documents/agent_experiments/autogen_magneticone"
    }
    
    results_dir = Path(__file__).parent / "scan_results"
    results_dir.mkdir(exist_ok=True)
    
    for project_name, target_dir in targets.items():
        if Path(target_dir).exists():
            print(f"📊 Scanning {project_name}...")
            result = scan_directory(target_dir)
            
            # Save to JSON
            output_file = results_dir / f"{project_name}_scan_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Results saved to: {output_file}")
        else:
            print(f"   ❌ Skipping {project_name}: directory not found")


def show_cli_examples():
    """Show CLI usage examples for both projects"""
    print("\n💻 CLI Usage Examples")
    print("=" * 60)
    
    print("🔧 Basic scanning commands:")
    print("# Scan CrewAI Gmail project:")
    print("python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail")
    print()
    print("# Scan AutoGen MagneticOne project:")
    print("python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/autogen_magneticone")
    print()
    
    print("📊 Advanced analysis:")
    print("# Full analysis with security checks:")
    print("python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail --all")
    print()
    print("# Save results to custom file:")
    print("python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/autogen_magneticone --output autogen_analysis.json")
    print()
    
    print("🔍 Individual file scanning:")
    print("# Scan specific files:")
    print("python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail/tools.py")
    print("python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/autogen_magneticone/payload.py")
    print()
    
    print("🌐 Web interface:")
    print("# Start web UI for interactive analysis:")
    print("python -m sentinelagent.cli.start_web_ui")
    print("# Then navigate to: http://localhost:8000")


def main():
    """Main function to run all examples"""
    print("🚀 SentinelAgent Focused Examples")
    print("=" * 60)
    print("Demonstrating analysis of CrewAI Gmail and AutoGen MagneticOne projects")
    print()
    
    try:
        # Run comprehensive analyses
        example_crewai_gmail_comprehensive()
        example_autogen_magneticone_comprehensive()
        
        # Save detailed results
        save_detailed_results()
        
        # Show CLI examples
        show_cli_examples()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed successfully!")
        print()
        print("📁 Check the 'scan_results' directory for detailed JSON outputs")
        print("🌐 Try the web interface: python -m sentinelagent.cli.start_web_ui")
        print("📖 See docs/DEMO_GUIDE.md for comprehensive usage guide")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("💡 Please ensure:")
        print("   - Required dependencies are installed: pip install -r requirements.txt")
        print("   - Target project directories exist")
        print("   - SentinelAgent is properly installed")


if __name__ == "__main__":
    main()
