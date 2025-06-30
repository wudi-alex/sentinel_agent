#!/usr/bin/env python3
"""
Quick Path Viewer - Extract specific path types for easier analysis
"""

import json
import sys

def view_paths_by_type(path_type_filter=None, max_paths=20, min_risk=0.0):
    """View paths filtered by type and risk"""
    
    # Load data
    paths_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_improved_graph.json"
    graph_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/improved_graph.json"
    
    with open(paths_file, 'r', encoding='utf-8') as f:
        paths_data = json.load(f)
    
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    # Create node mapping
    node_mapping = {}
    for node in graph_data.get('nodes', []):
        node_id = node['id']
        node_name = node['name']
        node_type = node['type']
        role = node.get('metadata', {}).get('role', '')
        
        if node_type == 'agent' and role:
            display_name = f"{node_name}({role})"
        else:
            display_name = f"{node_name}({node_type})"
        
        node_mapping[node_id] = display_name
    
    # Get detailed paths
    detailed_paths = paths_data.get('path_analysis', {}).get('detailed_paths', [])
    
    # Filter paths
    filtered_paths = []
    for path_info in detailed_paths:
        path_type = path_info.get('path_type', '')
        risk_score = path_info.get('risk_score', 0)
        
        # Apply filters
        if path_type_filter and path_type != path_type_filter:
            continue
        if risk_score < min_risk:
            continue
        
        filtered_paths.append(path_info)
    
    # Sort by risk score (descending) then by length
    filtered_paths.sort(key=lambda x: (-x.get('risk_score', 0), x.get('length', 0)))
    
    # Limit results
    display_paths = filtered_paths[:max_paths]
    
    print(f"🔍 PATH ANALYSIS VIEWER")
    print(f"Filter: {path_type_filter or 'All types'}")
    print(f"Min Risk: {min_risk}")
    print(f"Showing: {len(display_paths)} of {len(filtered_paths)} matching paths")
    print("=" * 80)
    
    for i, path_info in enumerate(display_paths, 1):
        path_nodes = path_info.get('path', [])
        risk_score = path_info.get('risk_score', 0)
        path_type = path_info.get('path_type', 'unknown')
        length = path_info.get('length', 0)
        
        # Convert to display names
        path_display = []
        for node_id in path_nodes:
            display_name = node_mapping.get(node_id, node_id)
            path_display.append(display_name)
        
        # Risk indicator
        if risk_score == 0:
            risk_indicator = "🟢"
        elif risk_score < 0.3:
            risk_indicator = "🟡"
        elif risk_score < 0.7:
            risk_indicator = "🟠"
        else:
            risk_indicator = "🔴"
        
        path_string = " -> ".join(path_display)
        print(f"{i:3d}. {path_string}")
        print(f"     path_type: {path_type} ; risk_score: {risk_score:.3f} {risk_indicator} ; length: {length}")
        print()

def show_summary():
    """Show quick summary of all path types"""
    
    # Load data
    paths_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_improved_graph.json"
    
    with open(paths_file, 'r', encoding='utf-8') as f:
        paths_data = json.load(f)
    
    path_analysis = paths_data.get('path_analysis', {})
    path_types = path_analysis.get('path_type_distribution', {})
    risk_dist = path_analysis.get('risk_score_distribution', {})
    
    print("📊 QUICK SUMMARY")
    print("=" * 40)
    print(f"Total Paths: {sum(path_types.values())}")
    print("\nPath Types:")
    for path_type, count in sorted(path_types.items()):
        print(f"  • {path_type.replace('_', ' ').title()}: {count}")
    
    print("\nRisk Distribution:")
    for risk_level, count in risk_dist.items():
        emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk_level, "⚪")
        print(f"  {emoji} {risk_level.title()}: {count}")

def main():
    """Main function with command line interface"""
    
    if len(sys.argv) == 1:
        print("🚀 Path Visualization Quick Viewer")
        print("Usage examples:")
        print("  python quick_path_viewer.py summary                    # Show summary")
        print("  python quick_path_viewer.py all                        # Show all paths (first 20)")
        print("  python quick_path_viewer.py agent_collaboration        # Show agent collaboration paths")
        print("  python quick_path_viewer.py mixed_interaction           # Show mixed interaction paths")
        print("  python quick_path_viewer.py agent_tool_usage           # Show agent tool usage paths")
        print("  python quick_path_viewer.py risky                      # Show paths with risk > 0")
        print("  python quick_path_viewer.py long                       # Show paths with length >= 4")
        return
    
    command = sys.argv[1].lower()
    
    if command == "summary":
        show_summary()
    
    elif command == "all":
        view_paths_by_type(max_paths=20)
    
    elif command == "agent_collaboration":
        view_paths_by_type("agent_collaboration", max_paths=15)
    
    elif command == "mixed_interaction":
        view_paths_by_type("mixed_interaction", max_paths=15)
    
    elif command == "agent_tool_usage":
        view_paths_by_type("agent_tool_usage", max_paths=15)
    
    elif command == "risky":
        view_paths_by_type(min_risk=0.001, max_paths=15)
    
    elif command == "long":
        # Load data to filter by length
        paths_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_improved_graph.json"
        graph_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/improved_graph.json"
        
        with open(paths_file, 'r', encoding='utf-8') as f:
            paths_data = json.load(f)
        
        with open(graph_file, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        # Create node mapping
        node_mapping = {}
        for node in graph_data.get('nodes', []):
            node_id = node['id']
            node_name = node['name']
            node_type = node['type']
            role = node.get('metadata', {}).get('role', '')
            
            if node_type == 'agent' and role:
                display_name = f"{node_name}({role})"
            else:
                display_name = f"{node_name}({node_type})"
            
            node_mapping[node_id] = display_name
        
        detailed_paths = paths_data.get('path_analysis', {}).get('detailed_paths', [])
        long_paths = [p for p in detailed_paths if p.get('length', 0) >= 4]
        long_paths.sort(key=lambda x: (-x.get('length', 0), -x.get('risk_score', 0)))
        
        print(f"🔍 LONG PATHS (length >= 4)")
        print(f"Found: {len(long_paths)} paths")
        print("=" * 80)
        
        for i, path_info in enumerate(long_paths[:15], 1):
            path_nodes = path_info.get('path', [])
            risk_score = path_info.get('risk_score', 0)
            path_type = path_info.get('path_type', 'unknown')
            length = path_info.get('length', 0)
            
            path_display = []
            for node_id in path_nodes:
                display_name = node_mapping.get(node_id, node_id)
                path_display.append(display_name)
            
            risk_indicator = "🟢" if risk_score == 0 else "🟡" if risk_score < 0.3 else "🟠" if risk_score < 0.7 else "🔴"
            
            path_string = " -> ".join(path_display)
            print(f"{i:3d}. {path_string}")
            print(f"     path_type: {path_type} ; risk_score: {risk_score:.3f} {risk_indicator} ; length: {length}")
            print()
    
    else:
        print(f"Unknown command: {command}")
        main()

if __name__ == "__main__":
    main()
