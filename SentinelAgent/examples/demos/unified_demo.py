#!/usr/bin/env python3
"""
SentinelAgent Unified Demo Script
=================================

This comprehensive demo script combines all SentinelAgent demonstration features:
1. Interactive command-line demos (scanning, graph building, file operations)
2. Web UI feature demonstrations and explanations
3. API endpoint documentation and examples
4. Security analysis feature showcase
5. Technical implementation details
6. Usage instructions and best practices

This unified script provides both interactive functionality and informational content
to demonstrate the complete capabilities of the SentinelAgent platform.
"""

import sys
import json
import time
import os
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from sentinelagent.core.scanner import scan_directory, scan_file
    from sentinelagent.core.graph_builder import build_graph_from_scan, scan_and_build_graph
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("⚠️  Core modules not available - some interactive features will be disabled")


# =============================================================================
# Utility Functions for Formatted Output
# =============================================================================

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 40)

def print_success(message):
    """Print a success message"""
    print(f"✅ {message}")

def print_info(message):
    """Print an info message"""
    print(f"ℹ️  {message}")

def print_warning(message):
    """Print a warning message"""
    print(f"⚠️  {message}")

def print_error(message):
    """Print an error message"""
    print(f"❌ {message}")

def print_banner():
    """Print main banner"""
    print("=" * 60)
    print("🔍 SentinelAgent - Unified Demo Platform")
    print("   AI Agent System Analysis & Monitoring")
    print("=" * 60)


# =============================================================================
# Interactive Demo Functions (from demo_enhanced.py and demo.py)
# =============================================================================

def demo_basic_scanning():
    """Basic scanning demonstration"""
    if not CORE_AVAILABLE:
        print_error("Core modules not available for scanning demo")
        return None
        
    print_section("Basic Scanning Demo")
    
    # Scan current directory
    print("📂 Scanning current directory...")
    try:
        result = scan_directory('.')
        
        # Display results
        summary = result['scan_summary']
        print_success("Scan completed!")
        print(f"📊 Found:")
        print(f"   🤖 Agents: {summary['total_agents']}")
        print(f"   🔧 Tools: {summary['total_tools']}")
        print(f"   👥 Crews: {summary['total_crews']}")
        print(f"   📋 Tasks: {summary['total_tasks']}")
        print(f"   📄 Python files: {summary['python_files']}")
        
        return result
    except Exception as e:
        print_error(f"Scanning failed: {e}")
        return None


def demo_graph_building(scan_result):
    """Graph building demonstration"""
    if not CORE_AVAILABLE or not scan_result:
        print_error("Cannot build graph - scanning failed or modules unavailable")
        return None
        
    print_section("Graph Construction Demo")
    
    try:
        print("🌐 Building relationship graph...")
        graph_data = build_graph_from_scan(scan_result)
        
        summary = graph_data['graph_summary']
        print_success("Graph construction complete!")
        print(f"📊 Statistics:")
        print(f"   📊 Total nodes: {summary['total_nodes']}")
        print(f"   🔗 Total edges: {summary['total_edges']}")
        print(f"   📈 Average degree: {summary['average_degree']:.2f}")
        
        print(f"\n📋 Node type distribution:")
        for node_type, count in summary['node_types'].items():
            print(f"   {node_type}: {count}")
        
        print(f"\n🔗 Relationship type distribution:")
        for rel_type, count in summary['relationship_types'].items():
            print(f"   {rel_type}: {count}")
        
        return graph_data
    except Exception as e:
        print_error(f"Graph building failed: {e}")
        return None


def demo_file_scanning():
    """File scanning demonstration"""
    if not CORE_AVAILABLE:
        print_error("Core modules not available for file scanning demo")
        return
        
    print_section("File Scanning Demo")
    
    # Look for a Python file to scan
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    if not py_files:
        print_warning("No Python files found in current directory")
        return
        
    target_file = py_files[0]
    print(f"📄 Scanning file: {target_file}")
    
    try:
        result = scan_file(target_file)
        summary = result['scan_summary']
        print_success("File scan completed!")
        print(f"📊 Found:")
        print(f"   🤖 Agents: {summary['total_agents']}")
        print(f"   🔧 Tools: {summary['total_tools']}")
        print(f"   👥 Crews: {summary['total_crews']}")
        print(f"   📋 Tasks: {summary['total_tasks']}")
    except Exception as e:
        print_error(f"File scanning failed: {e}")


def demo_integrated_workflow():
    """Integrated workflow demo"""
    if not CORE_AVAILABLE:
        print_error("Core modules not available for integrated workflow demo")
        return
        
    print_section("Integrated Workflow Demo")
    
    try:
        print("🔄 Executing integrated scanning and graph building...")
        graph_data = scan_and_build_graph('.', 'unified_demo_graph.json')
        
        print_success(f"Complete! Generated graph with {graph_data['graph_summary']['total_nodes']} nodes")
        print("📁 Results saved to: unified_demo_graph.json")
    except Exception as e:
        print_error(f"Integrated workflow failed: {e}")


def demo_target_scanning():
    """Target-specific scanning demo from demo.py"""
    if not CORE_AVAILABLE:
        print_error("Core modules not available for target scanning demo")
        return
        
    print_section("Target Scanning Demo")
    
    # Available demo targets
    demo_targets = {
        '1': '/Users/xuhe/Documents/agent_experiments/crewai_gmail',
        '2': '/Users/xuhe/Documents/agent_experiments/autogen_magneticone', 
        '3': '.',  # Current directory
    }
    
    print("🎯 Available scan targets:")
    print("1. CrewAI Gmail project")
    print("2. AutoGen MagneticOne project")
    print("3. SentinelAgent project (current directory)")
    print("4. Custom path")
    
    choice = input("\nPlease enter your choice (1-4): ").strip()
    
    if choice in demo_targets:
        target = demo_targets[choice]
    elif choice == '4':
        target = input("Please enter target path: ").strip()
    else:
        print_error("Invalid choice")
        return
    
    # Execute scan
    print(f"\n📂 Scanning directory: {target}")
    
    if not Path(target).exists():
        print_error(f"Directory does not exist: {target}")
        return

    try:
        result = scan_directory(target)
        
        # Display scan results
        summary = result['scan_summary']
        print_success("Scan completed!")
        print(f"📊 Summary: {summary['total_agents']} agents, {summary['total_tools']} tools, {summary['total_files']} files")
        
        # Detailed information
        if result['agents']:
            print(f"\n🤖 Found Agents (first 3):")
            for agent in result['agents'][:3]:
                print(f"   - {agent['name']} ({agent['type']})")
        
        if result['tools']:
            print(f"\n🔧 Found Tools (first 3):")
            for tool in result['tools'][:3]:
                print(f"   - {tool['name']} ({tool['type']})")
        
        # Save results
        output_file = f"unified_scan_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {output_file}")
        return result
        
    except Exception as e:
        print_error(f"Scanning failed: {e}")
        return None


def interactive_core_demo():
    """Interactive demo for core functionality"""
    print_header("SentinelAgent Interactive Core Demo")
    
    if not CORE_AVAILABLE:
        print_error("Core modules not available - cannot run interactive demo")
        return
    
    scan_result = None
    
    while True:
        print_section("Interactive Demo Menu")
        print("1. Basic directory scanning")
        print("2. Graph building demo (requires scan data)")
        print("3. File scanning demo")
        print("4. Target-specific scanning")
        print("5. Integrated workflow")
        print("6. View generated files")
        print("0. Return to main menu")
        
        choice = input("\nPlease enter your choice (0-6): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            scan_result = demo_basic_scanning()
            
            # Ask whether to build graph
            if scan_result and input("\n🌐 Build relationship graph? (y/n): ").lower().startswith('y'):
                demo_graph_building(scan_result)
                
        elif choice == '2':
            if scan_result:
                demo_graph_building(scan_result)
            else:
                print_warning("Need to execute scan first...")
                scan_result = demo_basic_scanning()
                if scan_result:
                    demo_graph_building(scan_result)
            
        elif choice == '3':
            demo_file_scanning()
            
        elif choice == '4':
            scan_result = demo_target_scanning()
            
        elif choice == '5':
            demo_integrated_workflow()
            
        elif choice == '6':
            json_files = [f for f in os.listdir('.') if f.endswith('.json')]
            if json_files:
                print_section("Generated JSON Files")
                for i, file in enumerate(json_files, 1):
                    size = os.path.getsize(file) / 1024  # KB
                    print(f"   {i}. {file} ({size:.1f} KB)")
            else:
                print_info("No JSON files generated yet")
        else:
            print_error("Invalid selection, please try again")


# =============================================================================
# Web UI and Feature Demonstration (from complete_demo.py)
# =============================================================================

def demo_web_ui_features():
    """Demonstrate Web UI features"""
    print_header("SentinelAgent Web UI Demo")
    
    print_info("The SentinelAgent Web UI provides a complete interface for:")
    print("   • 🔍 Agent System Scanning")
    print("   • 🌐 Relationship Graph Visualization") 
    print("   • 🛣️  Path Analysis with Security Insights")
    print("   • 📊 Log Analysis with Anomaly Detection")
    print("   • 📁 Analysis Results Management")
    print("   • 🎮 Interactive Demo Mode")
    
    print_section("Available Demo Features")
    print("1. Scanner Tab:")
    print("   - Load Demo Data: Complete agent system scan results")
    print("   - Shows agents, tools, crews, and tasks found in the system")
    
    print("\n2. Graph Tab:")
    print("   - Load Demo Graph: Interactive relationship visualization")
    print("   - D3.js powered graph with node types and relationships")
    print("   - Real-time statistics and metrics")
    
    print("\n3. Path Analysis Tab:")
    print("   - Load Demo Paths: Security-focused path analysis")
    print("   - Risk scoring and vulnerability detection")
    print("   - Critical path identification")
    
    print("\n4. Log Analysis Tab:")
    print("   - Load Demo Logs: Execution log analysis with anomalies")
    print("   - Performance metrics and success rates")
    print("   - Security insights and recommendations")
    
    print("\n5. Results Tab:")
    print("   - Load Demo Results: Pre-generated analysis results")
    print("   - Multiple result types (scan, graph, paths, logs)")
    print("   - Detailed result viewing and management")
    
    print_section("Demo Data Overview")
    demo_data = {
        "system_overview": {
            "agents": 3,
            "tools": 2, 
            "crews": 1,
            "tasks": 4,
            "total_components": 10
        },
        "security_analysis": {
            "overall_risk_score": 0.42,
            "risk_level": "medium",
            "critical_vulnerabilities": 1,
            "suspicious_patterns": 2,
            "security_recommendations": 5
        },
        "execution_analysis": {
            "total_log_entries": 156,
            "execution_paths": 4,
            "anomalies_detected": 4,
            "success_rate": "87.5%",
            "performance_issues": 2
        }
    }
    
    for category, metrics in demo_data.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for metric, value in metrics.items():
            print(f"   • {metric.replace('_', ' ').title()}: {value}")


def demo_api_endpoints():
    """Demonstrate API endpoints"""
    print_header("SentinelAgent API Endpoints")
    
    endpoints = {
        "Core Analysis": {
            "/api/scan": "Execute agent system scan",
            "/api/build-graph": "Build relationship graph from scan data",
            "/api/analyze-paths": "Perform path analysis with security insights", 
            "/api/analyze-logs": "Analyze execution logs for anomalies"
        },
        "Demo Data": {
            "/api/demo-data": "Load demo scan results",
            "/api/demo-graph": "Load demo relationship graph",
            "/api/demo-paths": "Load demo path analysis",
            "/api/demo-logs": "Load demo log analysis",
            "/api/demo-results": "Load demo results list"
        },
        "Results Management": {
            "/api/results": "List all analysis result files",
            "/api/result/<filename>": "Get specific analysis result",
            "/api/demo-result/<type>": "Get demo result by type"
        },
        "Utility": {
            "/api/examples": "List example projects",
            "/health": "Health check endpoint"
        }
    }
    
    for category, endpoints_dict in endpoints.items():
        print_section(category)
        for endpoint, description in endpoints_dict.items():
            print(f"   {endpoint:<25} - {description}")


def demo_security_features():
    """Demonstrate security analysis features"""
    print_header("Security Analysis Features")
    
    print_section("Vulnerability Detection")
    vulnerabilities = [
        {
            "id": "VULN-001",
            "severity": "CRITICAL",
            "title": "Privilege Escalation in Task Manager",
            "description": "Task manager can access admin functions without authorization"
        },
        {
            "id": "VULN-002", 
            "severity": "HIGH",
            "title": "Unencrypted Cross-Agent Communication",
            "description": "Sensitive data transmitted without encryption"
        },
        {
            "id": "VULN-003",
            "severity": "MEDIUM", 
            "title": "Insufficient Input Validation",
            "description": "Email processing lacks proper input sanitization"
        }
    ]
    
    for vuln in vulnerabilities:
        severity_color = "🔴" if vuln["severity"] == "CRITICAL" else "🟠" if vuln["severity"] == "HIGH" else "🟡"
        print(f"{severity_color} {vuln['id']} - {vuln['severity']}")
        print(f"   Title: {vuln['title']}")
        print(f"   Description: {vuln['description']}")
        print()
    
    print_section("Security Recommendations")
    recommendations = [
        "Implement role-based access control",
        "Add TLS encryption for inter-agent communication", 
        "Implement comprehensive input validation",
        "Add real-time security monitoring",
        "Regular security audits and penetration testing"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")


def demo_usage_instructions():
    """Show usage instructions"""
    print_header("How to Use SentinelAgent")
    
    print_section("Web UI Access")
    print("1. Start the web service:")
    print("   python scripts/start_web_ui.py")
    print("\n2. Open your browser and navigate to:")
    print("   http://localhost:5002")
    
    print_section("Quick Demo Steps")
    steps = [
        "Navigate to the Scanner tab",
        "Click 'Load Demo Data' to see agent system scan results",
        "Switch to Graph tab and click 'Load Demo Graph'", 
        "Explore the interactive relationship visualization",
        "Go to Path Analysis tab and click 'Load Demo Paths'",
        "Review security insights and risk analysis",
        "Check Log Analysis tab and click 'Load Demo Logs'",
        "Examine execution paths and anomaly detection",
        "Visit Results tab and click 'Load Demo Results'",
        "Browse different result types and view details"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"   {i:2d}. {step}")
    
    print_section("Real Project Analysis")
    print("To analyze your own agent project:")
    print("1. Enter your project path in Scanner tab")
    print("2. Click 'Start Scan' to analyze the codebase") 
    print("3. Use scan results to build relationship graph")
    print("4. Perform path analysis for security insights")
    print("5. Analyze execution logs if available")
    print("6. Review all results in Results tab")


def demo_technical_details():
    """Show technical implementation details"""
    print_header("Technical Implementation")
    
    print_section("Architecture")
    components = {
        "Backend": "Python Flask + CORS support",
        "Frontend": "Vue.js 3 + Element Plus UI",
        "Visualization": "D3.js for interactive graphs", 
        "Analysis": "NetworkX, Pandas for data processing",
        "File Processing": "JSON, CSV, Text parsing"
    }
    
    for component, tech in components.items():
        print(f"   • {component:<15}: {tech}")
    
    print_section("Supported Agent Frameworks")
    frameworks = [
        "✅ CrewAI - Full support for crews, agents, tasks, tools",
        "✅ AutoGen - Agent conversations and workflows",
        "✅ LangChain - Agent chains and tool integrations", 
        "✅ Custom Frameworks - Extensible architecture"
    ]
    
    for framework in frameworks:
        print(f"   {framework}")
    
    print_section("Analysis Capabilities")
    capabilities = [
        "🔍 Static code analysis for agent detection",
        "🌐 Dynamic relationship graph building",
        "🛣️  Execution path analysis with risk scoring",
        "📊 Log parsing and anomaly detection", 
        "🔒 Security vulnerability assessment",
        "📈 Performance metrics and optimization"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")


# =============================================================================
# Main Menu and Application Logic
# =============================================================================

def show_main_menu():
    """Display the main menu"""
    print_section("Main Demo Menu")
    print("1. 🎮 Interactive Core Demos (scanning, graph building)")
    print("2. 🌐 Web UI Features Overview")
    print("3. 🔗 API Endpoints Documentation")
    print("4. 🔒 Security Analysis Features")
    print("5. 📖 Usage Instructions")
    print("6. 🔧 Technical Implementation Details")
    print("7. 🎯 Run All Demonstrations")
    print("0. Exit")


def run_all_demonstrations():
    """Run all demonstration modules"""
    print_header("Running All SentinelAgent Demonstrations")
    print_info(f"Demo session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run informational demos
    demo_web_ui_features()
    demo_api_endpoints()
    demo_security_features()
    demo_usage_instructions()
    demo_technical_details()
    
    # Run interactive demo if core is available
    if CORE_AVAILABLE:
        print_info("Core modules available - running interactive demos")
        demo_basic_scanning()
    else:
        print_warning("Core modules not available - skipping interactive demos")
    
    print_header("All Demonstrations Complete")
    print_success("All SentinelAgent features demonstrated successfully!")
    
    print_section("Next Steps")
    print("1. 🌐 Access the Web UI at http://localhost:5002")
    print("2. 🎮 Try the interactive demo features")
    print("3. 📊 Load your own agent projects for analysis")
    print("4. 🔒 Review security recommendations")
    print("5. 📖 Check the documentation for advanced features")
    
    print("\n💡 Pro Tips:")
    print("   • Use demo data to understand the interface")
    print("   • Combine multiple analysis types for comprehensive insights")
    print("   • Export results for further processing")
    print("   • Integrate with CI/CD pipelines for automated analysis")


def main():
    """Main application function"""
    print_banner()
    print_info("Unified Demo Platform - All SentinelAgent Features")
    print_info(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not CORE_AVAILABLE:
        print_warning("Some interactive features may be limited due to missing core modules")
    
    try:
        while True:
            show_main_menu()
            choice = input("\nPlease enter your choice (0-7): ").strip()
            
            if choice == '0':
                print_success("Thank you for using SentinelAgent!")
                break
            elif choice == '1':
                interactive_core_demo()
            elif choice == '2':
                demo_web_ui_features()
            elif choice == '3':
                demo_api_endpoints()
            elif choice == '4':
                demo_security_features()
            elif choice == '5':
                demo_usage_instructions()
            elif choice == '6':
                demo_technical_details()
            elif choice == '7':
                run_all_demonstrations()
            else:
                print_error("Invalid selection, please try again")
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user.")
        print_success("Thank you for using SentinelAgent!")
    except Exception as e:
        print_error(f"Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
