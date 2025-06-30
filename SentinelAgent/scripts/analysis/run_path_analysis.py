#!/usr/bin/env python3
"""
Script to run path analysis on email assistant agent system graph
"""

import sys
import os
import json
from pathlib import Path

# Add the SentinelAgent package to Python path
sys.path.insert(0, '/Users/xuhe/Documents/agent_experiments/SentinelAgent')

from sentinelagent.core.path_analyzer import PathAnalyzer, analyze_paths_from_file

def main():
    # Input and output file paths
    graph_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/graph_email_assistant_agent_system.py.json"
    output_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_email_assistant_agent_system.py.json"
    
    print("=== SentinelAgent Path Analyzer ===")
    print(f"Input graph file: {graph_file}")
    print(f"Output path file: {output_file}")
    print()
    
    try:
        # Check if input file exists
        if not os.path.exists(graph_file):
            print(f"Error: Graph file not found: {graph_file}")
            return
        
        print("Loading graph data...")
        with open(graph_file, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        print(f"Graph summary:")
        if 'graph_summary' in graph_data:
            summary = graph_data['graph_summary']
            print(f"  - Total nodes: {summary.get('total_nodes', 'N/A')}")
            print(f"  - Total edges: {summary.get('total_edges', 'N/A')}")
            print(f"  - Node types: {summary.get('node_types', {})}")
            print(f"  - Relationship types: {summary.get('relationship_types', {})}")
        print()
        
        # Initialize path analyzer
        print("Initializing path analyzer...")
        analyzer = PathAnalyzer()
        
        # Perform path analysis
        print("Analyzing execution paths...")
        analysis_results = analyzer.analyze_graph_paths(graph_data)
        
        # Save results
        print("Saving analysis results...")
        analyzer.save_analysis_to_file(analysis_results, output_file)
        
        # Display summary of results
        print("\n=== Path Analysis Results Summary ===")
        if 'overall_assessment' in analysis_results:
            assessment = analysis_results['overall_assessment']
            print(f"Overall Risk Score: {assessment.get('total_risk_score', 'N/A')}")
            print(f"Risk Level: {assessment.get('risk_level', 'N/A')}")
            print(f"Total Paths Analyzed: {assessment.get('total_paths_analyzed', 'N/A')}")
            print(f"Suspicious Patterns Found: {assessment.get('suspicious_patterns_found', 'N/A')}")
        
        print("\n=== Node Analysis ===")
        if 'node_analysis' in analysis_results:
            node_analysis = analysis_results['node_analysis']
            print(f"Total Nodes: {node_analysis.get('total_nodes', 'N/A')}")
            print(f"Node State Distribution: {node_analysis.get('node_state_distribution', {})}")
        
        print("\n=== Edge Analysis ===")
        if 'edge_analysis' in analysis_results:
            edge_analysis = analysis_results['edge_analysis']
            print(f"Total Edges: {edge_analysis.get('total_edges', 'N/A')}")
            print(f"Edge State Distribution: {edge_analysis.get('edge_state_distribution', {})}")
        
        print("\n=== Path Analysis ===")
        if 'path_analysis' in analysis_results:
            path_analysis = analysis_results['path_analysis']
            print(f"Path Type Distribution: {path_analysis.get('path_type_distribution', {})}")
            print(f"Risk Score Distribution: {path_analysis.get('risk_score_distribution', {})}")
        
        print("\n=== Suspicious Patterns ===")
        if 'suspicious_patterns' in analysis_results:
            patterns = analysis_results['suspicious_patterns']
            if patterns:
                for i, pattern in enumerate(patterns, 1):
                    print(f"{i}. {pattern.get('pattern_type', 'Unknown')} ({pattern.get('severity', 'Unknown')} severity)")
                    print(f"   Description: {pattern.get('description', 'N/A')}")
                    print(f"   Details: {pattern.get('details', 'N/A')}")
                    if 'affected_nodes' in pattern:
                        print(f"   Affected Nodes: {pattern['affected_nodes']}")
                    if 'affected_edges' in pattern:
                        print(f"   Affected Edges: {len(pattern['affected_edges'])} edge(s)")
                    print()
            else:
                print("No suspicious patterns detected.")
        
        print("\n=== Recommendations ===")
        if 'recommendations' in analysis_results:
            recommendations = analysis_results['recommendations']
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"{i}. {rec}")
            else:
                print("No recommendations generated.")
        
        print(f"\n✓ Path analysis completed successfully!")
        print(f"✓ Detailed results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during path analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
