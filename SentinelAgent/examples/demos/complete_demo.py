#!/usr/bin/env python3
"""
Complete SentinelAgent Demo Script
==================================

This script demonstrates all major features of SentinelAgent:
1. System scanning
2. Relationship graph building  
3. Path analysis with security insights
4. Log analysis with anomaly detection
5. Comprehensive reporting

Run this script to see a complete demonstration of SentinelAgent capabilities.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add src directory to Python path
project_root = Path(__file__).parent.parent
# removed src_path
# removed src_path insert

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

def main():
    """Main demo function"""
    print_header("SentinelAgent Complete Demo")
    print_info("AI Agent System Analysis & Monitoring Platform")
    print_info(f"Demo running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run all demo sections
        demo_web_ui_features()
        demo_api_endpoints()
        demo_security_features()
        demo_usage_instructions()
        demo_technical_details()
        
        print_header("Demo Complete")
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
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user.")
    except Exception as e:
        print_error(f"Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
