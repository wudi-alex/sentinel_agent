#!/usr/bin/env python3
"""
Path Analysis Report Summary for Email Assistant Agent System
"""

import json
from pathlib import Path

def generate_summary_report():
    """Generate a concise summary report"""
    
    # Load the full analysis results
    analysis_file = "/Users/xuhe/Documents/agent_experiments/SentinelAgent/paths_email_assistant_agent_system.py.json"
    
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("=" * 80)
        print("EMAIL ASSISTANT AGENT SYSTEM - PATH ANALYSIS SUMMARY")
        print("=" * 80)
        
        # Basic Information
        print("\n📊 BASIC INFORMATION")
        print("-" * 40)
        analysis_info = data.get('analysis_info', {})
        print(f"Analysis Time: {analysis_info.get('timestamp', 'N/A')}")
        print(f"Rules Applied: {analysis_info.get('rules_applied', 'N/A')}")
        
        # Overall Assessment
        print("\n🎯 OVERALL ASSESSMENT")
        print("-" * 40)
        assessment = data.get('overall_assessment', {})
        risk_score = assessment.get('total_risk_score', 0)
        risk_level = assessment.get('risk_level', 'unknown')
        
        # Use emojis for risk level visualization
        risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk_level, "⚪")
        
        print(f"Overall Risk Score: {risk_score:.3f}")
        print(f"Risk Level: {risk_emoji} {risk_level.upper()}")
        print(f"Total Paths Analyzed: {assessment.get('total_paths_analyzed', 0):,}")
        print(f"Suspicious Patterns Found: {assessment.get('suspicious_patterns_found', 0)}")
        
        # Node Analysis
        print("\n🔗 NODE ANALYSIS")
        print("-" * 40)
        node_analysis = data.get('node_analysis', {})
        print(f"Total Nodes: {node_analysis.get('total_nodes', 0)}")
        
        state_dist = node_analysis.get('node_state_distribution', {})
        for state, count in state_dist.items():
            state_emoji = {"normal": "🟢", "suspicious": "🟡", "critical": "🔴"}.get(state, "⚪")
            print(f"  {state_emoji} {state.title()}: {count}")
        
        # Edge Analysis
        print("\n🔀 EDGE ANALYSIS")
        print("-" * 40)
        edge_analysis = data.get('edge_analysis', {})
        print(f"Total Edges: {edge_analysis.get('total_edges', 0)}")
        
        edge_state_dist = edge_analysis.get('edge_state_distribution', {})
        for state, count in edge_state_dist.items():
            state_emoji = {"normal": "🟢", "suspicious": "🟡", "anomalous": "🔴", "forbidden": "⛔"}.get(state, "⚪")
            print(f"  {state_emoji} {state.title()}: {count}")
        
        # Path Analysis
        print("\n🛤️ PATH ANALYSIS")
        print("-" * 40)
        path_analysis = data.get('path_analysis', {})
        
        print("Path Type Distribution:")
        path_types = path_analysis.get('path_type_distribution', {})
        for path_type, count in path_types.items():
            print(f"  📍 {path_type.replace('_', ' ').title()}: {count:,}")
        
        print("\nRisk Score Distribution:")
        risk_dist = path_analysis.get('risk_score_distribution', {})
        for risk, count in risk_dist.items():
            risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk, "⚪")
            print(f"  {risk_emoji} {risk.title()} Risk: {count:,}")
        
        # Suspicious Patterns - Most Important Part
        print("\n⚠️ SUSPICIOUS PATTERNS DETECTED")
        print("-" * 40)
        patterns = data.get('suspicious_patterns', [])
        
        if patterns:
            for i, pattern in enumerate(patterns, 1):
                severity = pattern.get('severity', 'unknown')
                severity_emoji = {"low": "🟡", "medium": "🟠", "high": "🔴", "critical": "⚡"}.get(severity, "⚪")
                
                print(f"\n{i}. {severity_emoji} {pattern.get('pattern_type', 'Unknown').replace('_', ' ').title()}")
                print(f"   Severity: {severity.upper()}")
                print(f"   Description: {pattern.get('description', 'N/A')}")
                print(f"   Details: {pattern.get('details', 'N/A')}")
                
                if 'affected_nodes' in pattern:
                    nodes = pattern['affected_nodes']
                    if len(nodes) <= 5:
                        print(f"   Affected Nodes: {', '.join(nodes)}")
                    else:
                        print(f"   Affected Nodes: {len(nodes)} nodes ({', '.join(nodes[:3])}, ...)")
                
                if 'affected_paths' in pattern:
                    paths = pattern['affected_paths']
                    print(f"   Affected Paths: {len(paths)} path(s)")
                    if len(paths) <= 3:
                        for j, path in enumerate(paths):
                            if len(path) <= 6:
                                print(f"     Path {j+1}: {' → '.join(path)}")
                            else:
                                print(f"     Path {j+1}: {' → '.join(path[:3])} → ... → {' → '.join(path[-2:])}")
        else:
            print("✅ No suspicious patterns detected!")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS")
        print("-" * 40)
        recommendations = data.get('recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                # Add appropriate emoji based on content
                if "CRITICAL" in rec.upper():
                    emoji = "🚨"
                elif "review" in rec.lower():
                    emoji = "🔍"
                elif "simplify" in rec.lower():
                    emoji = "🔧"
                else:
                    emoji = "💡"
                
                print(f"{i}. {emoji} {rec}")
        else:
            print("✅ No specific recommendations needed.")
        
        # Key Insights
        print("\n🔍 KEY INSIGHTS")
        print("-" * 40)
        
        total_paths = assessment.get('total_paths_analyzed', 0)
        if total_paths > 10000:
            print("• ⚠️ Very high number of execution paths detected - indicates complex system")
        
        if 'circular_dependencies' in [p.get('pattern_type') for p in patterns]:
            print("• 🔄 Circular dependencies found - potential infinite loop risk")
        
        if 'complex_collaborations' in [p.get('pattern_type') for p in patterns]:
            print("• 🕸️ Complex agent collaboration chains detected - may need simplification")
        
        if all(state == 'normal' for state in node_analysis.get('node_state_distribution', {}).keys()):
            print("• ✅ All nodes appear to be in normal state")
        
        if risk_level == 'low':
            print("• ✅ Overall system risk is low")
        
        print("\n" + "=" * 80)
        print("Analysis completed. See detailed results in the JSON file for more information.")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error reading analysis file: {e}")

if __name__ == "__main__":
    generate_summary_report()
