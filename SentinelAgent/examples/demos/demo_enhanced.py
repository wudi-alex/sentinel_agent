#!/usr/bin/env python3
"""
SentinelAgent Demo - Enhanced Version
Demonstrates scanning and graph building functionality
"""

import sys
import json
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
# removed src_path
# removed src_path insert

from sentinelagent.core.scanner import scan_directory, scan_file
from sentinelagent.core.graph_builder import build_graph_from_scan, scan_and_build_graph


def demo_basic_scanning():
    """Basic scanning demonstration"""
    print("=== Basic Scanning Demo ===\n")
    
    # Scan current directory
    print("Scanning current directory...")
    result = scan_directory('.')
    
    # Display results
    summary = result['scan_summary']
    print(f"Scan completed! Found:")
    print(f"  🤖 Agents: {summary['total_agents']}")
    print(f"  🔧 Tools: {summary['total_tools']}")
    print(f"  👥 Crews: {summary['total_crews']}")
    print(f"  📋 Tasks: {summary['total_tasks']}")
    print(f"  📄 Python files: {summary['python_files']}")
    
    return result


def demo_graph_building(scan_result):
    """Graph building demonstration"""
    print("\n=== Graph Construction Demo ===\n")
    
    print("Building relationship graph...")
    graph_data = build_graph_from_scan(scan_result)
    
    summary = graph_data['graph_summary']
    print(f"Graph construction complete!")
    print(f"  📊 Total nodes: {summary['total_nodes']}")
    print(f"  🔗 Total edges: {summary['total_edges']}")
    print(f"  📈 Average degree: {summary['average_degree']:.2f}")
    
    print(f"\nNode type distribution:")
    for node_type, count in summary['node_types'].items():
        print(f"  {node_type}: {count}")
    
    print(f"\nRelationship type distribution:")
    for rel_type, count in summary['relationship_types'].items():
        print(f"  {rel_type}: {count}")
    
    return graph_data


def demo_file_scanning():
    """File scanning demonstration"""
    print("\n=== File Scanning Demo ===\n")
    
    print("Scanning scanner.py file...")
    result = scan_file('scanner.py')
    
    summary = result['scan_summary']
    print(f"File scan completed! Found:")
    print(f"  🤖 Agents: {summary['total_agents']}")
    print(f"  🔧 Tools: {summary['total_tools']}")
    print(f"  👥 Crews: {summary['total_crews']}")
    print(f"  📋 Tasks: {summary['total_tasks']}")


def demo_integrated_workflow():
    """Integrated workflow demo"""
    print("\n=== Integrated Workflow Demo ===\n")
    
    print("Executing integrated scanning and graph building...")
    graph_data = scan_and_build_graph('.', 'demo_complete_graph.json')
    
    print(f"✅ Complete! Generated graph with {graph_data['graph_summary']['total_nodes']} nodes")
    print("📁 Results saved to: demo_complete_graph.json")


def interactive_demo():
    """Interactive demo"""
    print("🔍 SentinelAgent - Interactive Demo")
    print("=" * 50)
    
    while True:
        print("\nPlease select an operation:")
        print("1. Basic directory scanning")
        print("2. Graph building demo")
        print("3. File scanning demo")
        print("4. Integrated workflow")
        print("5. View generated files")
        print("0. Exit")
        
        choice = input("\nPlease enter your choice (0-5): ").strip()
        
        if choice == '0':
            print("Thank you for using SentinelAgent!")
            break
        elif choice == '1':
            scan_result = demo_basic_scanning()
            
            # Ask whether to build graph
            if input("\nBuild relationship graph? (y/n): ").lower().startswith('y'):
                demo_graph_building(scan_result)
                
        elif choice == '2':
            print("Need to execute scan first...")
            scan_result = demo_basic_scanning()
            demo_graph_building(scan_result)
            
        elif choice == '3':
            demo_file_scanning()
            
        elif choice == '4':
            demo_integrated_workflow()
            
        elif choice == '5':
            import os
            json_files = [f for f in os.listdir('.') if f.endswith('.json')]
            if json_files:
                print(f"\nGenerated JSON files:")
                for i, file in enumerate(json_files, 1):
                    size = os.path.getsize(file) / 1024  # KB
                    print(f"  {i}. {file} ({size:.1f} KB)")
            else:
                print("\nNo JSON files generated yet")
        else:
            print("Invalid selection, please try again")


if __name__ == "__main__":
    interactive_demo()
