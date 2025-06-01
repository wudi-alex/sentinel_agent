#!/usr/bin/env python3
"""
Path Analysis Demo
Demonstrates agent system path analysis functionality
"""

import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sentinelagent.core.inspector import InspectorAgent
from sentinelagent.core.graph_builder import scan_and_build_graph
from sentinelagent.core.path_analyzer import analyze_paths_from_file, analyze_graph_paths


def demo_complete_analysis():
    """Demonstrate complete analysis workflow"""
    print("=" * 60)
    print("Path Analysis Demo - Complete Analysis Workflow")
    print("=" * 60)
    
    # createInspector
    inspector = InspectorAgent()
    
    # Analyze current directory
    current_dir = str(Path.cwd())
    print(f"Analyzing directory: {current_dir}")
    
    # Execute complete analysis
    result = inspector.comprehensive_analysis(
        target_path=current_dir,
        scan_output="demo_scan.json",
        graph_output="demo_graph.json", 
        path_output="demo_paths.json"
    )
    
    # displaypathanalyzeresultsummary
    path_analysis = result['path_analysis']
    overall = path_analysis.get('overall_assessment', {})
    
    print("\n" + "=" * 40)
    print("Path Analysis Results Summary")
    print("=" * 40)
    print(f"Overall risk score: {overall.get('total_risk_score', 0)}")
    print(f"Risk level: {overall.get('risk_level', 'unknown')}")
    print(f"Paths analyzed: {overall.get('total_paths_analyzed', 0)}")
    print(f"Suspicious patterns found: {overall.get('suspicious_patterns_found', 0)}")
    
    # Display node state distribution
    node_analysis = path_analysis.get('node_analysis', {})
    node_states = node_analysis.get('node_state_distribution', {})
    print(f"\nNode state distribution:")
    for state, count in node_states.items():
        print(f"  {state}: {count}")
    
    # Display suspicious patterns
    patterns = path_analysis.get('suspicious_patterns', [])
    if patterns:
        print(f"\nDetected suspicious patterns:")
        for i, pattern in enumerate(patterns, 1):
            print(f"  {i}. {pattern.get('pattern_type', 'unknown')} "
                  f"(severity: {pattern.get('severity', 'unknown')})")
            print(f"     {pattern.get('details', '')}")
    
    # Display recommendations
    recommendations = path_analysis.get('recommendations', [])
    if recommendations:
        print(f"\nImprovement recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    return result


def demo_path_types_analysis():
    """Demonstrate path type analysis"""
    print("\n" + "=" * 60)
    print("Path Type Analysis Demo")
    print("=" * 60)
    
    # Check if existing graph file exists
    graph_file = "demo_graph.json"
    if not Path(graph_file).exists():
        print(f"Graph file {graph_file} does not exist, running complete analysis first...")
        demo_complete_analysis()
    
    # Read graph data
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    # Execute path analysis
    path_analysis = analyze_graph_paths(graph_data)
    
    # Display path type distribution
    path_types = path_analysis.get('path_analysis', {}).get('path_type_distribution', {})
    print("Path type distribution:")
    for path_type, count in path_types.items():
        print(f"  {path_type}: {count}")
    
    # Display detailed path information
    detailed_paths = path_analysis.get('path_analysis', {}).get('detailed_paths', [])
    print(f"\nDetailed path information (total {len(detailed_paths)} paths):")
    
    for i, path_info in enumerate(detailed_paths[:5], 1):  # Show only first 5
        print(f"\nPath {i}:")
        print(f"  Path: {' -> '.join(path_info['path'])}")
        print(f"  Type: {path_info['path_type']}")
        print(f"  Length: {path_info['length']}")
        print(f"  Risk score: {path_info['risk_score']:.3f}")
    
    if len(detailed_paths) > 5:
        print(f"\n... {len(detailed_paths) - 5} more paths")


def demo_anomaly_detection():
    """Demonstrate anomaly detection functionality"""
    print("\n" + "=" * 60)
    print("Anomaly Detection Demo")
    print("=" * 60)
    
    # Check if path analysis file exists
    paths_file = "demo_paths.json"
    if not Path(paths_file).exists():
        print(f"Path analysis file {paths_file} does not exist, running complete analysis first...")
        demo_complete_analysis()
    
    # Read path analysis data
    with open(paths_file, 'r', encoding='utf-8') as f:
        path_analysis = json.load(f)
    
    # Analyze anomaly patterns
    patterns = path_analysis.get('suspicious_patterns', [])
    
    print(f"Detected {len(patterns)} suspicious patterns:")
    
    for i, pattern in enumerate(patterns, 1):
        print(f"\nAnomaly pattern {i}:")
        print(f"  Type: {pattern.get('pattern_type', 'unknown')}")
        print(f"  Severity: {pattern.get('severity', 'unknown')}")
        print(f"  Description: {pattern.get('description', '')}")
        print(f"  Details: {pattern.get('details', '')}")
        
        # Display affected nodes/edges
        if 'affected_nodes' in pattern:
            print(f"  Affected nodes: {', '.join(pattern['affected_nodes'])}")
        if 'affected_edges' in pattern:
            print(f"  Affected edge count: {len(pattern['affected_edges'])}")
        if 'affected_paths' in pattern:
            print(f"  Affected path count: {len(pattern['affected_paths'])}")
    
    # Analyze risk distribution
    risk_dist = path_analysis.get('path_analysis', {}).get('risk_score_distribution', {})
    total_paths = sum(risk_dist.values())
    
    if total_paths > 0:
        print(f"\nRisk score distribution:")
        print(f"  Low risk (<0.3): {risk_dist.get('low', 0)} ({risk_dist.get('low', 0)/total_paths*100:.1f}%)")
        print(f"  Medium risk (0.3-0.7): {risk_dist.get('medium', 0)} ({risk_dist.get('medium', 0)/total_paths*100:.1f}%)")
        print(f"  High risk (>0.7): {risk_dist.get('high', 0)} ({risk_dist.get('high', 0)/total_paths*100:.1f}%)")


def demo_security_insights():
    """Demonstrate security insight functionality"""
    print("\n" + "=" * 60)
    print("Security Insights Demo")
    print("=" * 60)
    
    # Check if path analysis file exists
    paths_file = "demo_paths.json"
    if not Path(paths_file).exists():
        print(f"Path analysis file {paths_file} does not exist, running complete analysis first...")
        demo_complete_analysis()
    
    # Read path analysis data
    with open(paths_file, 'r', encoding='utf-8') as f:
        path_analysis = json.load(f)
    
    overall = path_analysis.get('overall_assessment', {})
    
    print("Security Assessment Summary:")
    print(f"  Overall risk score: {overall.get('total_risk_score', 0):.3f}")
    print(f"  Risk level: {overall.get('risk_level', 'unknown').upper()}")
    
    # Security recommendations
    recommendations = path_analysis.get('recommendations', [])
    if recommendations:
        print(f"\nSecurity recommendations:")
        for i, rec in enumerate(recommendations, 1):
            # Determine priority based on recommendation content
            priority = "HIGH" if "CRITICAL" in rec else "MEDIUM" if "Review" in rec else "LOW"
            print(f"  [{priority}] {rec}")
    
    # Node security state
    node_analysis = path_analysis.get('node_analysis', {})
    nodes_with_states = node_analysis.get('nodes_with_states', {})
    suspicious_nodes = [nid for nid, state in nodes_with_states.items() if state == 'suspicious']
    
    if suspicious_nodes:
        print(f"\nSuspicious nodes requiring attention:")
        for node_id in suspicious_nodes[:5]:  # Show only first 5
            print(f"  - {node_id}")
        if len(suspicious_nodes) > 5:
            print(f"  ... {len(suspicious_nodes) - 5} more")
    
    # Edge security state
    edge_analysis = path_analysis.get('edge_analysis', {})
    edge_dist = edge_analysis.get('edge_state_distribution', {})
    
    print(f"\nConnection security state:")
    for state, count in edge_dist.items():
        print(f"  {state}: {count}")


def interactive_demo():
    """Interactive demo"""
    print("\n" + "=" * 60)
    print("Interactive Path Analysis Demo")
    print("=" * 60)
    
    while True:
        print("\nSelect demo option:")
        print("1. Complete analysis workflow")
        print("2. Path type analysis")
        print("3. Anomaly detection demo")
        print("4. Security insights demo")
        print("5. Analyze custom directory")
        print("0. Exit")
        
        choice = input("\nPlease select (0-5): ").strip()
        
        if choice == '0':
            print("Demo finished!")
            break
        elif choice == '1':
            demo_complete_analysis()
        elif choice == '2':
            demo_path_types_analysis()
        elif choice == '3':
            demo_anomaly_detection()
        elif choice == '4':
            demo_security_insights()
        elif choice == '5':
            target_dir = input("Please enter the directory path to analyze: ").strip()
            if target_dir and Path(target_dir).exists():
                inspector = InspectorAgent()
                inspector.comprehensive_analysis(target_dir)
            else:
                print("Directory does not exist!")
        else:
            print("Invalid selection, please try again.")


if __name__ == "__main__":
    # Run all demos
    print("Path Analysis System Demo")
    print("This demo will showcase various features of the agent system path analysis")
    
    try:
        # 1. Complete analysis
        demo_complete_analysis()
        
        # 2. Path type analysis
        demo_path_types_analysis()
        
        # 3. Anomaly detection
        demo_anomaly_detection()
        
        # 4. Security insights
        demo_security_insights()
        
        # 5. Interactive demo
        interactive_demo()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError occurred during demo: {e}")
        import traceback
        traceback.print_exc()
