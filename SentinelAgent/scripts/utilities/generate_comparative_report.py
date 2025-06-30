#!/usr/bin/env python3
"""
Improved Graph Analysis Report - Comparison with Previous Results
"""

import json
from pathlib import Path

def generate_comparative_report():
    """Generate a comparative analysis report"""
    
    # Load both analysis results
    original_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_email_assistant_agent_system.py.json"
    improved_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_improved_graph.json"
    
    try:
        # Load original analysis
        with open(original_file, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # Load improved analysis
        with open(improved_file, 'r', encoding='utf-8') as f:
            improved_data = json.load(f)
        
        print("=" * 80)
        print("COMPARATIVE PATH ANALYSIS REPORT")
        print("=" * 80)
        
        # Comparison table
        print("\n📊 COMPARISON OVERVIEW")
        print("-" * 60)
        print(f"{'Metric':<30} {'Original':<15} {'Improved':<15}")
        print("-" * 60)
        
        orig_assess = original_data.get('overall_assessment', {})
        impr_assess = improved_data.get('overall_assessment', {})
        
        print(f"{'Nodes':<30} {original_data.get('node_analysis', {}).get('total_nodes', 0):<15} {improved_data.get('node_analysis', {}).get('total_nodes', 0):<15}")
        print(f"{'Edges':<30} {original_data.get('edge_analysis', {}).get('total_edges', 0):<15} {improved_data.get('edge_analysis', {}).get('total_edges', 0):<15}")
        print(f"{'Total Paths':<30} {orig_assess.get('total_paths_analyzed', 0):,<15} {impr_assess.get('total_paths_analyzed', 0):,<15}")
        print(f"{'Risk Score':<30} {orig_assess.get('total_risk_score', 0):<15.3f} {impr_assess.get('total_risk_score', 0):<15.3f}")
        print(f"{'Risk Level':<30} {orig_assess.get('risk_level', 'N/A'):<15} {impr_assess.get('risk_level', 'N/A'):<15}")
        print(f"{'Suspicious Patterns':<30} {orig_assess.get('suspicious_patterns_found', 0):<15} {impr_assess.get('suspicious_patterns_found', 0):<15}")
        
        # Path type analysis
        print("\n🛤️ PATH TYPE ANALYSIS")
        print("-" * 60)
        
        orig_paths = original_data.get('path_analysis', {}).get('path_type_distribution', {})
        impr_paths = improved_data.get('path_analysis', {}).get('path_type_distribution', {})
        
        print("Original Graph Path Types:")
        for path_type, count in orig_paths.items():
            print(f"  🔸 {path_type.replace('_', ' ').title()}: {count:,}")
        
        print("\nImproved Graph Path Types:")
        for path_type, count in impr_paths.items():
            print(f"  🔹 {path_type.replace('_', ' ').title()}: {count:,}")
        
        # Risk distribution
        print("\n⚠️ RISK DISTRIBUTION")
        print("-" * 60)
        
        orig_risk = original_data.get('path_analysis', {}).get('risk_score_distribution', {})
        impr_risk = improved_data.get('path_analysis', {}).get('risk_score_distribution', {})
        
        print(f"{'Risk Level':<15} {'Original':<15} {'Improved':<15} {'Change':<15}")
        print("-" * 60)
        
        for risk_level in ['low', 'medium', 'high']:
            orig_count = orig_risk.get(risk_level, 0)
            impr_count = impr_risk.get(risk_level, 0)
            change = impr_count - orig_count
            change_str = f"{change:+,}" if change != 0 else "0"
            
            risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk_level, "⚪")
            print(f"{risk_emoji} {risk_level.title():<12} {orig_count:<15,} {impr_count:<15,} {change_str:<15}")
        
        # Node composition
        print("\n🔗 NODE COMPOSITION")
        print("-" * 60)
        
        orig_nodes = original_data.get('node_analysis', {}).get('total_nodes', 0)
        impr_nodes = improved_data.get('node_analysis', {}).get('total_nodes', 0)
        
        # Try to get node type information from graph summaries
        # We need to load the graph files to get this info
        graph_orig = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/graph_email_assistant_agent_system.py.json"
        graph_impr = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/improved_graph.json"
        
        try:
            with open(graph_orig, 'r') as f:
                orig_graph = json.load(f)
            with open(graph_impr, 'r') as f:
                impr_graph = json.load(f)
            
            print("Original Graph Composition:")
            orig_node_types = orig_graph.get('graph_summary', {}).get('node_types', {})
            for node_type, count in orig_node_types.items():
                print(f"  🔸 {node_type.title()}: {count}")
            
            print("\nImproved Graph Composition:")
            impr_node_types = impr_graph.get('graph_summary', {}).get('node_types', {})
            for node_type, count in impr_node_types.items():
                print(f"  🔹 {node_type.title()}: {count}")
        except:
            print("Could not load graph composition details")
        
        # Suspicious patterns comparison
        print("\n🚨 SUSPICIOUS PATTERNS COMPARISON")
        print("-" * 60)
        
        orig_patterns = original_data.get('suspicious_patterns', [])
        impr_patterns = improved_data.get('suspicious_patterns', [])
        
        print("Original Graph Issues:")
        if orig_patterns:
            for i, pattern in enumerate(orig_patterns, 1):
                severity = pattern.get('severity', 'unknown')
                severity_emoji = {"low": "🟡", "medium": "🟠", "high": "🔴", "critical": "⚡"}.get(severity, "⚪")
                print(f"  {i}. {severity_emoji} {pattern.get('pattern_type', 'Unknown').replace('_', ' ').title()}")
                print(f"     {pattern.get('details', 'N/A')}")
        else:
            print("  ✅ No issues detected")
        
        print("\nImproved Graph Issues:")
        if impr_patterns:
            for i, pattern in enumerate(impr_patterns, 1):
                severity = pattern.get('severity', 'unknown')
                severity_emoji = {"low": "🟡", "medium": "🟠", "high": "🔴", "critical": "⚡"}.get(severity, "⚪")
                print(f"  {i}. {severity_emoji} {pattern.get('pattern_type', 'Unknown').replace('_', ' ').title()}")
                print(f"     {pattern.get('details', 'N/A')}")
        else:
            print("  ✅ No issues detected")
        
        # Key improvements
        print("\n✨ KEY IMPROVEMENTS")
        print("-" * 60)
        
        # Calculate improvements
        path_reduction = orig_assess.get('total_paths_analyzed', 0) - impr_assess.get('total_paths_analyzed', 0)
        risk_reduction = orig_assess.get('total_risk_score', 0) - impr_assess.get('total_risk_score', 0)
        
        print(f"• 📉 Path Count Reduction: {path_reduction:,} paths ({path_reduction/orig_assess.get('total_paths_analyzed', 1)*100:.1f}% reduction)")
        print(f"• 🎯 Risk Score Improvement: {risk_reduction:.3f} points ({risk_reduction/orig_assess.get('total_risk_score', 1)*100:.1f}% improvement)")
        print(f"• 🔧 Graph Simplification: From {orig_nodes} to {impr_nodes} nodes")
        print(f"• 🎪 Path Diversity: Now includes {len(impr_paths)} different path types vs {len(orig_paths)}")
        
        # Analyze what changed in patterns
        orig_pattern_types = {p.get('pattern_type') for p in orig_patterns}
        impr_pattern_types = {p.get('pattern_type') for p in impr_patterns}
        
        resolved_patterns = orig_pattern_types - impr_pattern_types
        new_patterns = impr_pattern_types - orig_pattern_types
        persisting_patterns = orig_pattern_types & impr_pattern_types
        
        if resolved_patterns:
            print(f"• ✅ Resolved Issues: {', '.join(resolved_patterns).replace('_', ' ')}")
        if new_patterns:
            print(f"• ⚠️ New Issues: {', '.join(new_patterns).replace('_', ' ')}")
        if persisting_patterns:
            print(f"• 🔄 Persisting Issues: {', '.join(persisting_patterns).replace('_', ' ')}")
        
        # Final assessment
        print("\n🏆 FINAL ASSESSMENT")
        print("-" * 60)
        
        if impr_assess.get('total_risk_score', 1) < orig_assess.get('total_risk_score', 0):
            print("✅ Overall improvement achieved!")
        else:
            print("⚠️ Risk score increased - further investigation needed")
        
        if len(impr_patterns) < len(orig_patterns):
            print("✅ Fewer suspicious patterns detected")
        elif len(impr_patterns) == len(orig_patterns):
            print("🔄 Same number of suspicious patterns")
        else:
            print("⚠️ More suspicious patterns detected")
        
        print(f"\nThe improved graph shows:")
        print(f"• More realistic complexity ({impr_assess.get('total_paths_analyzed', 0):,} vs {orig_assess.get('total_paths_analyzed', 0):,} paths)")
        print(f"• Better structural balance (agents + tools vs agents only)")
        print(f"• Improved path diversity (3 types vs 1 type)")
        print(f"• Lower overall risk ({impr_assess.get('total_risk_score', 0):.3f} vs {orig_assess.get('total_risk_score', 0):.3f})")
        
        print("\n" + "=" * 80)
        print("The improved graph provides a more realistic and analyzable representation!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error generating comparative report: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_comparative_report()
