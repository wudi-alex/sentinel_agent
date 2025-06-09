#!/usr/bin/env python3
"""
Advanced Graph Analysis Demo
============================

This demo focuses on advanced graph structure analysis and metrics.
For basic graph building, use unified_demo.py.

This demo provides:
- Advanced graph structure analysis
- Node importance ranking (in-degree/out-degree)  
- Graph topology insights
- Detailed graph metrics
"""

import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from sentinelagent.core.graph_builder import scan_and_build_graph
    GRAPH_BUILDER_AVAILABLE = True
except ImportError:
    GRAPH_BUILDER_AVAILABLE = False
    print("⚠️  Graph builder not available - using pre-existing graph files only")


def load_or_create_graph():
    """Load existing graph or create new one"""
    graph_files = ['unified_demo_graph.json', 'agent_system_graph.json', 'complete_agent_graph.json']
    
    # Try to load existing graph
    for graph_file in graph_files:
        if Path(graph_file).exists():
            print(f"📊 Loading existing graph: {graph_file}")
            with open(graph_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    # Create new graph if none exist and builder is available
    if GRAPH_BUILDER_AVAILABLE:
        print("📊 No existing graph found, creating new one...")
        graph_data = scan_and_build_graph('.', 'graph_analysis_demo.json')
        print("✅ Graph created and saved to: graph_analysis_demo.json")
        return graph_data
    else:
        print("❌ No graph files found and builder unavailable")
        return None


def analyze_graph_structure(graph_data):
    """Analyze advanced graph structure and metrics"""
    if not graph_data:
        print("❌ No graph data available for analysis")
        return
        
    print("=" * 60)
    print("🔍 Advanced Graph Structure Analysis")
    print("=" * 60)
    
    # Basic statistics
    nodes = graph_data.get('nodes', [])
    edges = graph_data.get('edges', [])
    
    print(f"\n📊 Basic Graph Statistics:")
    print(f"   • Total nodes: {len(nodes)}")
    print(f"   • Total edges: {len(edges)}")
    
    if len(nodes) == 0:
        print("⚠️  No nodes found in graph")
        return
    
    # Calculate in-degree and out-degree
    in_degree = {}
    out_degree = {}
    
    # Initialize degrees
    for node in nodes:
        node_id = node['id']
        in_degree[node_id] = 0
        out_degree[node_id] = 0
    
    # Calculate degrees
    for edge in edges:
        source = edge.get('source')
        target = edge.get('target')
        if source in out_degree:
            out_degree[source] += 1
        if target in in_degree:
            in_degree[target] += 1
    
    # Calculate graph metrics
    total_degree = sum(out_degree.values())
    avg_degree = total_degree / len(nodes) if len(nodes) > 0 else 0
    max_in_degree = max(in_degree.values()) if in_degree else 0
    max_out_degree = max(out_degree.values()) if out_degree else 0
    
    print(f"   • Average degree: {avg_degree:.2f}")
    print(f"   • Maximum in-degree: {max_in_degree}")
    print(f"   • Maximum out-degree: {max_out_degree}")
    
    # Calculate density
    possible_edges = len(nodes) * (len(nodes) - 1)
    density = len(edges) / possible_edges if possible_edges > 0 else 0
    print(f"   • Graph density: {density:.3f}")
    
    # Node type analysis
    node_types = {}
    for node in nodes:
        node_type = node.get('type', 'unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    print(f"\n📋 Node Type Distribution:")
    for node_type, count in sorted(node_types.items()):
        percentage = (count / len(nodes)) * 100
        print(f"   • {node_type}: {count} ({percentage:.1f}%)")
    
    # Relationship type analysis  
    relationship_types = {}
    for edge in edges:
        rel_type = edge.get('relationship', 'unknown')
        relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
    
    if relationship_types:
        print(f"\n🔗 Relationship Type Distribution:")
        for rel_type, count in sorted(relationship_types.items()):
            percentage = (count / len(edges)) * 100
            print(f"   • {rel_type}: {count} ({percentage:.1f}%)")
    
    # Find most important nodes by out-degree (influence)
    print(f"\n🌟 Most Influential Nodes (by out-degree):")
    sorted_by_out = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)
    for i, (node_id, degree) in enumerate(sorted_by_out[:5]):
        node = next((n for n in nodes if n['id'] == node_id), None)
        if node:
            node_name = node.get('name', node_id)
            node_type = node.get('type', 'unknown')
            print(f"   {i+1}. {node_name} ({node_type}) - out-degree: {degree}")
    
    # Find most important nodes by in-degree (popularity)
    print(f"\n🎯 Most Popular Nodes (by in-degree):")
    sorted_by_in = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)
    for i, (node_id, degree) in enumerate(sorted_by_in[:5]):
        node = next((n for n in nodes if n['id'] == node_id), None)
        if node:
            node_name = node.get('name', node_id)
            node_type = node.get('type', 'unknown')
            print(f"   {i+1}. {node_name} ({node_type}) - in-degree: {degree}")
    
    # Find isolated nodes (no connections)
    isolated_nodes = [node_id for node_id in in_degree 
                     if in_degree[node_id] == 0 and out_degree[node_id] == 0]
    
    if isolated_nodes:
        print(f"\n🔍 Isolated Nodes ({len(isolated_nodes)}):")
        for node_id in isolated_nodes[:5]:  # Show first 5
            node = next((n for n in nodes if n['id'] == node_id), None)
            if node:
                node_name = node.get('name', node_id)
                node_type = node.get('type', 'unknown')
                print(f"   • {node_name} ({node_type})")
        if len(isolated_nodes) > 5:
            print(f"   ... and {len(isolated_nodes) - 5} more")
    
    # Calculate betweenness approximation (simplified)
    print(f"\n📈 Graph Topology Insights:")
    
    # Estimate connectivity
    connected_nodes = len([node_id for node_id in in_degree 
                          if in_degree[node_id] > 0 or out_degree[node_id] > 0])
    connectivity_ratio = connected_nodes / len(nodes) if len(nodes) > 0 else 0
    
    print(f"   • Connected nodes: {connected_nodes}/{len(nodes)} ({connectivity_ratio:.1%})")
    
    # Identify potential hubs (nodes with high degree)
    hub_threshold = avg_degree * 2
    hubs = [node_id for node_id in out_degree 
            if (in_degree[node_id] + out_degree[node_id]) > hub_threshold]
    
    if hubs:
        print(f"   • Potential hubs: {len(hubs)} nodes")
        print(f"   • Hub threshold: {hub_threshold:.1f} total degree")
    
    # Edge weight analysis if available
    edge_weights = [edge.get('weight', 1.0) for edge in edges if 'weight' in edge]
    if edge_weights:
        avg_weight = sum(edge_weights) / len(edge_weights)
        min_weight = min(edge_weights)
        max_weight = max(edge_weights)
        
        print(f"\n⚖️  Edge Weight Analysis:")
        print(f"   • Average weight: {avg_weight:.3f}")
        print(f"   • Weight range: {min_weight:.3f} - {max_weight:.3f}")
    
    return {
        'in_degree': in_degree,
        'out_degree': out_degree,
        'metrics': {
            'avg_degree': avg_degree,
            'density': density,
            'connectivity_ratio': connectivity_ratio,
            'isolated_nodes': len(isolated_nodes),
            'hubs': len(hubs)
        }
    }


def generate_graph_report(graph_data, analysis_result, output_file="graph_analysis_report.md"):
    """Generate a detailed graph analysis report"""
    if not graph_data or not analysis_result:
        print("❌ Cannot generate report - missing data")
        return
    
    print(f"\n📄 Generating detailed report: {output_file}")
    
    nodes = graph_data.get('nodes', [])
    edges = graph_data.get('edges', [])
    metrics = analysis_result.get('metrics', {})
    
    report_content = f"""# Graph Analysis Report
Generated: {Path().cwd()}

## Summary
- **Total Nodes**: {len(nodes)}
- **Total Edges**: {len(edges)}
- **Average Degree**: {metrics.get('avg_degree', 0):.2f}
- **Graph Density**: {metrics.get('density', 0):.3f}
- **Connectivity**: {metrics.get('connectivity_ratio', 0):.1%}

## Key Insights
- **Isolated Nodes**: {metrics.get('isolated_nodes', 0)}
- **Hub Nodes**: {metrics.get('hubs', 0)}

## Node Analysis
"""
    
    # Add node type breakdown
    node_types = {}
    for node in nodes:
        node_type = node.get('type', 'unknown')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    report_content += "### Node Types\n"
    for node_type, count in sorted(node_types.items()):
        percentage = (count / len(nodes)) * 100 if nodes else 0
        report_content += f"- **{node_type}**: {count} ({percentage:.1f}%)\n"
    
    # Add relationship analysis
    relationship_types = {}
    for edge in edges:
        rel_type = edge.get('relationship', 'unknown')
        relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
    
    if relationship_types:
        report_content += "\n### Relationship Types\n"
        for rel_type, count in sorted(relationship_types.items()):
            percentage = (count / len(edges)) * 100 if edges else 0
            report_content += f"- **{rel_type}**: {count} ({percentage:.1f}%)\n"
    
    # Save report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Report saved: {output_file}")


def main():
    """Main demo function"""
    print("🔍 SentinelAgent - Advanced Graph Analysis Demo")
    print("=" * 60)
    print("Note: For basic graph building, use unified_demo.py")
    print("This demo focuses on advanced graph structure analysis.")
    print("=" * 60)
    
    try:
        # Load or create graph
        graph_data = load_or_create_graph()
        
        if not graph_data:
            print("\n❌ No graph data available. Please:")
            print("1. Run unified_demo.py first to create a graph, or")
            print("2. Ensure graph builder modules are available")
            return
        
        # Perform advanced analysis
        analysis_result = analyze_graph_structure(graph_data)
        
        if analysis_result:
            # Generate detailed report
            generate_graph_report(graph_data, analysis_result)
            
            print("\n✅ Advanced graph analysis complete!")
            print("\n💡 Next steps:")
            print("   • Review the generated graph_analysis_report.md")
            print("   • Use insights for system optimization")
            print("   • Run path_demo.py for security-focused analysis")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
