#!/usr/bin/env python3
"""
Graph Building Demo
Demonstrates how to build agent system relationship graphs from scan results
"""

import sys
import json
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
# removed src_path
# removed src_path insert

from sentinelagent.core.scanner import scan_directory
from sentinelagent.core.graph_builder import build_graph_from_scan, build_and_save_graph, scan_and_build_graph


def demo_graph_building():
    """Demonstrate graph building functionality"""
    print("=== Agent System Graph Builder Demo ===\n")
    
    # 1. Scan current directory
    print("1. Scanning current directory...")
    scan_result = scan_directory('.')
    print(f"   Scan complete: Found {scan_result['scan_summary']['total_agents']} agents, "
          f"{scan_result['scan_summary']['total_tools']} tools, "
          f"{scan_result['scan_summary']['total_crews']} crews, "
          f"{scan_result['scan_summary']['total_tasks']} tasks")
    
    # 2. Build relationship graph
    print("\n2. Building relationship graph...")
    graph_data = build_graph_from_scan(scan_result)
    print(f"   Graph construction complete: {graph_data['graph_summary']['total_nodes']} nodes, "
          f"{graph_data['graph_summary']['total_edges']} edges")
    
    # 3. Display graph statistics
    print("\n3. Graph statistics:")
    summary = graph_data['graph_summary']
    print(f"   - Node type distribution: {summary['node_types']}")
    print(f"   - Relationship type distribution: {summary['relationship_types']}")
    print(f"   - Average degree: {summary['average_degree']:.2f}")
    
    # 4. Display some specific nodes and edges
    print("\n4. Graph structure preview:")
    print("   Node examples:")
    for i, node in enumerate(graph_data['nodes'][:3]):  # Show first 3 nodes
        print(f"     [{i+1}] {node['type']}: {node['name']} (in {node['file']})")
        if node['type'] == 'agent':
            crews = node['metadata'].get('crews', [])
            tasks = node['metadata'].get('tasks', [])
            if crews:
                print(f"         Belongs to Crew: {[c['name'] for c in crews]}")
            if tasks:
                print(f"         Executes Tasks: {[t['name'] for t in tasks]}")
    
    if len(graph_data['nodes']) > 3:
        print(f"     ... and {len(graph_data['nodes']) - 3} more nodes")
    
    print("\n   Edge examples:")
    for i, edge in enumerate(graph_data['edges'][:5]):  # Show first 5 edges
        source_node = next(n for n in graph_data['nodes'] if n['id'] == edge['source'])
        target_node = next(n for n in graph_data['nodes'] if n['id'] == edge['target'])
        print(f"     [{i+1}] {source_node['name']} -> {target_node['name']} "
              f"({edge['relationship']}, weight: {edge['weight']})")
    
    if len(graph_data['edges']) > 5:
        print(f"     ... and {len(graph_data['edges']) - 5} more edges")
    
    # 5. Save graph to file
    print("\n5. Saving graph to file...")
    output_file = "agent_system_graph.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    print(f"   Graph saved to: {output_file}")
    
    return graph_data


def demo_direct_scan_and_build():
    """Demonstrate integrated scan and build functionality"""
    print("\n=== Integrated Scanning and Building Demo ===\n")
    
    print("Executing integrated scanning and graph building...")
    graph_data = scan_and_build_graph('.', 'complete_agent_graph.json')
    
    print(f"Complete! Built graph with {graph_data['graph_summary']['total_nodes']} nodes and "
          f"{graph_data['graph_summary']['total_edges']} edges")
    print("Graph saved to: complete_agent_graph.json")
    
    return graph_data


def analyze_graph_structure(graph_data):
    """Analyze graph structure"""
    print("\n=== Graph Structure Analysis ===\n")
    
    # Calculate in-degree and out-degree
    in_degree = {}
    out_degree = {}
    
    # Initialize degrees
    for node in graph_data['nodes']:
        node_id = node['id']
        in_degree[node_id] = 0
        out_degree[node_id] = 0
    
    # Calculate degrees
    for edge in graph_data['edges']:
        out_degree[edge['source']] += 1
        in_degree[edge['target']] += 1
    
    # Find important nodes
    print("Most important nodes (by out-degree):")
    sorted_by_out = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)
    for i, (node_id, degree) in enumerate(sorted_by_out[:3]):
        node = next(n for n in graph_data['nodes'] if n['id'] == node_id)
        print(f"  {i+1}. {node['name']} ({node['type']}) - out-degree: {degree}")
    
    print("\nMost important nodes (by in-degree):")
    sorted_by_in = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)
    for i, (node_id, degree) in enumerate(sorted_by_in[:3]):
        node = next(n for n in graph_data['nodes'] if n['id'] == node_id)
        print(f"  {i+1}. {node['name']} ({node['type']}) - in-degree: {degree}")


if __name__ == "__main__":
    # Run basic demo
    graph_data = demo_graph_building()
    
    # Analyze graph structure
    analyze_graph_structure(graph_data)
    
    # Run integrated demo
    demo_direct_scan_and_build()
    
    print("\n=== Demo Complete ===")
    print("Generated files:")
    print("- agent_system_graph.json: Basic graph build results")
    print("- complete_agent_graph.json: Integrated scanning and build results")
