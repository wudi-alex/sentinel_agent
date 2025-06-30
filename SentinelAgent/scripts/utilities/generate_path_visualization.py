#!/usr/bin/env python3
"""
Path Visualization Script
Generates a human-readable document showing all execution paths from the analysis results
"""

import json
from pathlib import Path
from collections import defaultdict

def load_data():
    """Load both the analysis results and the graph data"""
    # Load path analysis results
    paths_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_improved_graph.json"
    graph_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/improved_graph.json"
    
    with open(paths_file, 'r', encoding='utf-8') as f:
        paths_data = json.load(f)
    
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    return paths_data, graph_data

def create_node_mapping(graph_data):
    """Create mapping from node IDs to meaningful names"""
    node_mapping = {}
    
    for node in graph_data.get('nodes', []):
        node_id = node['id']
        node_name = node['name']
        node_type = node['type']
        role = node.get('metadata', {}).get('role', '')
        
        # Create a descriptive name
        if node_type == 'agent' and role:
            display_name = f"{node_name}({role})"
        else:
            display_name = f"{node_name}({node_type})"
        
        node_mapping[node_id] = display_name
    
    return node_mapping

def generate_path_document():
    """Generate the path visualization document"""
    
    print("Loading data...")
    paths_data, graph_data = load_data()
    node_mapping = create_node_mapping(graph_data)
    
    # Get path analysis data
    detailed_paths = paths_data.get('path_analysis', {}).get('detailed_paths', [])
    total_paths = len(detailed_paths)
    
    print(f"Found {total_paths} paths to process...")
    
    # Output file
    output_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_visualization.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write("SENTINEL AGENT - EXECUTION PATHS VISUALIZATION\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {paths_data.get('analysis_info', {}).get('timestamp', 'Unknown')}\n")
        f.write(f"Total Paths: {total_paths}\n")
        f.write(f"Overall Risk Score: {paths_data.get('overall_assessment', {}).get('total_risk_score', 'N/A')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Group paths by type for better organization
        paths_by_type = defaultdict(list)
        for path_info in detailed_paths:
            path_type = path_info.get('path_type', 'unknown')
            paths_by_type[path_type].append(path_info)
        
        # Write node mapping reference
        f.write("NODE REFERENCE:\n")
        f.write("-" * 40 + "\n")
        for node_id, display_name in node_mapping.items():
            f.write(f"{node_id}: {display_name}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        # Process each path type
        for path_type, paths in sorted(paths_by_type.items()):
            f.write(f"PATH TYPE: {path_type.upper().replace('_', ' ')}\n")
            f.write(f"Count: {len(paths)} paths\n")
            f.write("-" * 60 + "\n")
            
            # Sort paths by length, then by risk score
            sorted_paths = sorted(paths, key=lambda x: (x.get('length', 0), x.get('risk_score', 0)))
            
            for i, path_info in enumerate(sorted_paths, 1):
                path_nodes = path_info.get('path', [])
                risk_score = path_info.get('risk_score', 0)
                path_length = path_info.get('length', 0)
                
                # Convert node IDs to display names
                path_display = []
                for node_id in path_nodes:
                    display_name = node_mapping.get(node_id, node_id)
                    path_display.append(display_name)
                
                # Create the path string
                path_string = " -> ".join(path_display)
                
                # Risk level indicator
                if risk_score == 0:
                    risk_indicator = "🟢"
                elif risk_score < 0.3:
                    risk_indicator = "🟡"
                elif risk_score < 0.7:
                    risk_indicator = "🟠"
                else:
                    risk_indicator = "🔴"
                
                # Write the path line
                f.write(f"{i:3d}. {path_string} ; path_type: {path_type} ; risk_score: {risk_score:.3f} {risk_indicator}\n")
            
            f.write("\n")
        
        # Statistical summary
        f.write("=" * 80 + "\n")
        f.write("STATISTICAL SUMMARY\n")
        f.write("=" * 80 + "\n")
        
        # Path type distribution
        f.write("Path Type Distribution:\n")
        for path_type, paths in sorted(paths_by_type.items()):
            percentage = len(paths) / total_paths * 100
            f.write(f"  {path_type.replace('_', ' ').title()}: {len(paths)} ({percentage:.1f}%)\n")
        f.write("\n")
        
        # Risk distribution
        risk_counts = {"zero": 0, "low": 0, "medium": 0, "high": 0}
        for path_info in detailed_paths:
            risk = path_info.get('risk_score', 0)
            if risk == 0:
                risk_counts["zero"] += 1
            elif risk < 0.3:
                risk_counts["low"] += 1
            elif risk < 0.7:
                risk_counts["medium"] += 1
            else:
                risk_counts["high"] += 1
        
        f.write("Risk Score Distribution:\n")
        for risk_level, count in risk_counts.items():
            percentage = count / total_paths * 100
            emoji = {"zero": "🟢", "low": "🟡", "medium": "🟠", "high": "🔴"}[risk_level]
            f.write(f"  {emoji} {risk_level.title()}: {count} ({percentage:.1f}%)\n")
        f.write("\n")
        
        # Length distribution
        length_counts = defaultdict(int)
        for path_info in detailed_paths:
            length = path_info.get('length', 0)
            length_counts[length] += 1
        
        f.write("Path Length Distribution:\n")
        for length in sorted(length_counts.keys()):
            count = length_counts[length]
            percentage = count / total_paths * 100
            f.write(f"  Length {length}: {count} paths ({percentage:.1f}%)\n")
        f.write("\n")
        
        # Top risky paths
        risky_paths = [p for p in detailed_paths if p.get('risk_score', 0) > 0]
        if risky_paths:
            f.write("TOP 10 HIGHEST RISK PATHS:\n")
            f.write("-" * 40 + "\n")
            sorted_risky = sorted(risky_paths, key=lambda x: x.get('risk_score', 0), reverse=True)
            
            for i, path_info in enumerate(sorted_risky[:10], 1):
                path_nodes = path_info.get('path', [])
                risk_score = path_info.get('risk_score', 0)
                path_type = path_info.get('path_type', 'unknown')
                
                path_display = []
                for node_id in path_nodes:
                    display_name = node_mapping.get(node_id, node_id)
                    path_display.append(display_name)
                
                path_string = " -> ".join(path_display)
                f.write(f"{i:2d}. {path_string} ; risk: {risk_score:.3f} ; type: {path_type}\n")
        else:
            f.write("NO HIGH RISK PATHS DETECTED 🎉\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("End of Path Visualization Report\n")
        f.write("=" * 80 + "\n")
    
    print(f"✅ Path visualization document generated: {output_file}")
    return output_file

def generate_summary_stats():
    """Generate and display summary statistics"""
    paths_data, graph_data = load_data()
    detailed_paths = paths_data.get('path_analysis', {}).get('detailed_paths', [])
    
    print("\n📊 QUICK STATISTICS")
    print("-" * 40)
    print(f"Total Paths: {len(detailed_paths)}")
    
    # Path types
    type_counts = defaultdict(int)
    for path in detailed_paths:
        type_counts[path.get('path_type', 'unknown')] += 1
    
    print("Path Types:")
    for path_type, count in sorted(type_counts.items()):
        print(f"  • {path_type.replace('_', ' ').title()}: {count}")
    
    # Risk distribution
    risk_scores = [p.get('risk_score', 0) for p in detailed_paths]
    zero_risk = sum(1 for r in risk_scores if r == 0)
    avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
    max_risk = max(risk_scores) if risk_scores else 0
    
    print(f"Risk Analysis:")
    print(f"  • Zero Risk Paths: {zero_risk} ({zero_risk/len(detailed_paths)*100:.1f}%)")
    print(f"  • Average Risk Score: {avg_risk:.3f}")
    print(f"  • Maximum Risk Score: {max_risk:.3f}")

if __name__ == "__main__":
    print("🚀 Starting Path Visualization Generation...")
    
    try:
        output_file = generate_path_document()
        generate_summary_stats()
        
        print(f"\n✅ Process completed successfully!")
        print(f"📄 Output file: {output_file}")
        print(f"\n💡 The document contains all {524} execution paths in human-readable format.")
        print(f"   Each line shows: path -> nodes ; path_type ; risk_score")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
