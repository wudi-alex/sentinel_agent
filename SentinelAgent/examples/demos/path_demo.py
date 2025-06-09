#!/usr/bin/env python3
"""
Advanced Path Analysis Demo
===========================

This demo focuses on specialized path analysis features that complement unified_demo.py.
For basic path analysis, use unified_demo.py.

This demo provides:
- Advanced path security analysis
- Risk assessment methodologies
- Path traversal vulnerability detection
- Security-focused path insights
"""

import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from sentinelagent.core.inspector import InspectorAgent
    from sentinelagent.core.path_analyzer import analyze_paths_from_file, analyze_graph_paths
    PATH_ANALYSIS_AVAILABLE = True
except ImportError:
    PATH_ANALYSIS_AVAILABLE = False
    print("⚠️  Path analysis modules not available - using pre-existing analysis files only")


def load_or_create_path_analysis():
    """Load existing path analysis or create new one"""
    path_files = ['unified_demo_paths.json', 'demo_paths.json', 'agent_system_paths.json']
    
    # Try to load existing analysis
    for path_file in path_files:
        if Path(path_file).exists():
            print(f"📊 Loading existing path analysis: {path_file}")
            with open(path_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    # Create new analysis if none exist and modules are available
    if PATH_ANALYSIS_AVAILABLE:
        print("📊 No existing path analysis found, creating new one...")
        try:
            inspector = InspectorAgent()
            result = inspector.comprehensive_analysis(
                target_path='.',
                path_output="specialized_path_analysis.json"
            )
            path_analysis = result.get('path_analysis', {})
            print("✅ Path analysis created and saved to: specialized_path_analysis.json")
            return path_analysis
        except Exception as e:
            print(f"❌ Failed to create path analysis: {e}")
            return None
    else:
        print("❌ No path analysis files found and modules unavailable")
        return None
    
def analyze_security_vulnerabilities(path_analysis):
    """Analyze security vulnerabilities in path analysis"""
    if not path_analysis:
        print("❌ No path analysis data available for security analysis")
        return
        
    print("=" * 60)
    print("🔒 Advanced Security Vulnerability Analysis")
    print("=" * 60)
    
    # Analyze suspicious patterns with security focus
    patterns = path_analysis.get('suspicious_patterns', [])
    
    if patterns:
        print(f"\n🚨 Security Threat Analysis ({len(patterns)} patterns detected):")
        
        # Categorize threats by severity
        critical_threats = [p for p in patterns if p.get('severity') == 'critical']
        high_threats = [p for p in patterns if p.get('severity') == 'high']
        medium_threats = [p for p in patterns if p.get('severity') == 'medium']
        
        if critical_threats:
            print(f"\n🔴 CRITICAL Threats ({len(critical_threats)}):")
            for threat in critical_threats:
                print(f"   • {threat.get('pattern_type', 'Unknown')}")
                print(f"     Description: {threat.get('description', 'No description')}")
                if 'affected_nodes' in threat:
                    print(f"     Affected nodes: {len(threat['affected_nodes'])}")
        
        if high_threats:
            print(f"\n🟠 HIGH Risk Threats ({len(high_threats)}):")
            for threat in high_threats:
                print(f"   • {threat.get('pattern_type', 'Unknown')}")
                print(f"     Description: {threat.get('description', 'No description')}")
        
        if medium_threats:
            print(f"\n🟡 MEDIUM Risk Threats ({len(medium_threats)}):")
            for threat in medium_threats[:3]:  # Show first 3
                print(f"   • {threat.get('pattern_type', 'Unknown')}")
            if len(medium_threats) > 3:
                print(f"   ... and {len(medium_threats) - 3} more")
    
    # Security recommendations analysis
    recommendations = path_analysis.get('recommendations', [])
    if recommendations:
        print(f"\n🛡️  Security Hardening Recommendations:")
        
        # Categorize recommendations by urgency
        security_recs = [r for r in recommendations if any(keyword in r.lower() 
                        for keyword in ['security', 'vulnerability', 'access', 'permission', 'encryption'])]
        
        for i, rec in enumerate(security_recs, 1):
            priority = "🔴 URGENT" if "critical" in rec.lower() else "🟠 HIGH" if "important" in rec.lower() else "🟡 STANDARD"
            print(f"   {i}. [{priority}] {rec}")
    
    # Path traversal risk analysis
    overall = path_analysis.get('overall_assessment', {})
    risk_score = overall.get('total_risk_score', 0)
    
    print(f"\n📊 Risk Assessment Summary:")
    print(f"   • Overall Risk Score: {risk_score:.3f}")
    print(f"   • Risk Level: {overall.get('risk_level', 'unknown').upper()}")
    
    if risk_score > 0.7:
        print("   🚨 SECURITY ALERT: High risk system detected!")
        print("      Immediate security review recommended")
    elif risk_score > 0.4:
        print("   ⚠️  CAUTION: Medium risk system")
        print("      Security improvements recommended")
    else:
        print("   ✅ Low risk system - good security posture")


def analyze_path_traversal_patterns(path_analysis):
    """Analyze path traversal and access patterns"""
    if not path_analysis:
        print("❌ No path analysis data available")
        return
        
    print("=" * 60)
    print("🛣️  Path Traversal Security Analysis")
    print("=" * 60)
    
    # Analyze detailed paths for security patterns
    detailed_paths = path_analysis.get('path_analysis', {}).get('detailed_paths', [])
    
    if detailed_paths:
        print(f"📋 Analyzing {len(detailed_paths)} paths for security vulnerabilities...")
        
        # Find high-risk paths
        high_risk_paths = [p for p in detailed_paths if p.get('risk_score', 0) > 0.7]
        medium_risk_paths = [p for p in detailed_paths if 0.4 <= p.get('risk_score', 0) <= 0.7]
        
        print(f"\n🚨 High-Risk Paths ({len(high_risk_paths)}):")
        for i, path in enumerate(high_risk_paths[:5], 1):  # Show first 5
            path_str = ' → '.join(path['path'])
            print(f"   {i}. Risk: {path['risk_score']:.3f} | {path_str}")
            print(f"      Type: {path.get('path_type', 'unknown')} | Length: {path.get('length', 0)}")
        
        if len(high_risk_paths) > 5:
            print(f"   ... and {len(high_risk_paths) - 5} more high-risk paths")
        
        if medium_risk_paths:
            print(f"\n⚠️  Medium-Risk Paths ({len(medium_risk_paths)}):")
            for i, path in enumerate(medium_risk_paths[:3], 1):  # Show first 3
                path_str = ' → '.join(path['path'])
                print(f"   {i}. Risk: {path['risk_score']:.3f} | {path_str}")
        
        # Analyze path types for security implications
        path_types = path_analysis.get('path_analysis', {}).get('path_type_distribution', {})
        print(f"\n📊 Path Type Security Analysis:")
        
        for path_type, count in path_types.items():
            risk_level = "HIGH" if "admin" in path_type.lower() or "root" in path_type.lower() else \
                        "MEDIUM" if "execute" in path_type.lower() or "write" in path_type.lower() else "LOW"
            print(f"   • {path_type}: {count} paths [{risk_level} risk]")


def analyze_node_security_states(path_analysis):
    """Analyze node security states and access patterns"""
    if not path_analysis:
        print("❌ No path analysis data available")
        return
        
    print("=" * 60)
    print("🔍 Node Security State Analysis")
    print("=" * 60)
    
    node_analysis = path_analysis.get('node_analysis', {})
    
    # Node state distribution analysis
    node_states = node_analysis.get('node_state_distribution', {})
    print(f"📊 Node Security State Distribution:")
    
    total_nodes = sum(node_states.values())
    if total_nodes > 0:
        for state, count in node_states.items():
            percentage = (count / total_nodes) * 100
            risk_indicator = "🚨" if state == "suspicious" else "⚠️" if state == "warning" else "✅"
            print(f"   {risk_indicator} {state.title()}: {count} ({percentage:.1f}%)")
    
    # Detailed node state analysis
    nodes_with_states = node_analysis.get('nodes_with_states', {})
    
    suspicious_nodes = [nid for nid, state in nodes_with_states.items() if state == 'suspicious']
    warning_nodes = [nid for nid, state in nodes_with_states.items() if state == 'warning']
    
    if suspicious_nodes:
        print(f"\n🚨 Suspicious Nodes Requiring Immediate Attention:")
        for i, node_id in enumerate(suspicious_nodes[:5], 1):  # Show first 5
            print(f"   {i}. {node_id}")
        if len(suspicious_nodes) > 5:
            print(f"   ... and {len(suspicious_nodes) - 5} more")
    
    if warning_nodes:
        print(f"\n⚠️  Warning Nodes for Review:")
        for i, node_id in enumerate(warning_nodes[:3], 1):  # Show first 3
            print(f"   {i}. {node_id}")
        if len(warning_nodes) > 3:
            print(f"   ... and {len(warning_nodes) - 3} more")
    
    # Edge security analysis
    edge_analysis = path_analysis.get('edge_analysis', {})
    edge_states = edge_analysis.get('edge_state_distribution', {})
    
    if edge_states:
        print(f"\n🔗 Connection Security Analysis:")
        total_edges = sum(edge_states.values())
        for state, count in edge_states.items():
            percentage = (count / total_edges) * 100 if total_edges > 0 else 0
            risk_indicator = "🚨" if "suspicious" in state else "⚠️" if "warning" in state else "✅"
            print(f"   {risk_indicator} {state.title()}: {count} ({percentage:.1f}%)")


def generate_security_report(path_analysis, output_file="path_security_report.md"):
    """Generate a detailed security-focused path analysis report"""
    if not path_analysis:
        print("❌ Cannot generate security report - missing data")
        return
    
    print(f"\n📄 Generating security report: {output_file}")
    
    overall = path_analysis.get('overall_assessment', {})
    patterns = path_analysis.get('suspicious_patterns', [])
    recommendations = path_analysis.get('recommendations', [])
    
    report_content = f"""# Path Security Analysis Report
Generated: {Path().cwd()}

## 🚨 Security Assessment Summary
- **Overall Risk Score**: {overall.get('total_risk_score', 0):.3f}
- **Risk Level**: {overall.get('risk_level', 'unknown').upper()}
- **Suspicious Patterns**: {len(patterns)}
- **Security Recommendations**: {len(recommendations)}

## 🔒 Critical Security Findings
"""
    
    # Add critical threats
    critical_threats = [p for p in patterns if p.get('severity') == 'critical']
    if critical_threats:
        report_content += f"\n### Critical Threats ({len(critical_threats)})\n"
        for threat in critical_threats:
            report_content += f"- **{threat.get('pattern_type', 'Unknown')}**\n"
            report_content += f"  - Description: {threat.get('description', 'No description')}\n"
            report_content += f"  - Severity: {threat.get('severity', 'unknown').upper()}\n\n"
    
    # Add security recommendations
    security_recs = [r for r in recommendations if any(keyword in r.lower() 
                    for keyword in ['security', 'vulnerability', 'access', 'permission'])]
    
    if security_recs:
        report_content += "\n### Security Recommendations\n"
        for i, rec in enumerate(security_recs, 1):
            priority = "🔴 URGENT" if "critical" in rec.lower() else "🟠 HIGH" if "important" in rec.lower() else "🟡 STANDARD"
            report_content += f"{i}. [{priority}] {rec}\n"
    
    # Save report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Security report saved: {output_file}")


def main():
    """Main demo function"""
    print("🔒 SentinelAgent - Advanced Path Security Analysis Demo")
    print("=" * 60)
    print("Note: For basic path analysis, use unified_demo.py")
    print("This demo focuses on security-specific path analysis features.")
    print("=" * 60)
    
    try:
        # Load or create path analysis
        path_analysis = load_or_create_path_analysis()
        
        if not path_analysis:
            print("\n❌ No path analysis data available. Please:")
            print("1. Run unified_demo.py first to create path analysis, or")
            print("2. Ensure path analysis modules are available")
            return
        
        # Perform security-focused analysis
        print("\n🔍 Performing advanced security analysis...")
        
        # 1. Security vulnerability analysis
        analyze_security_vulnerabilities(path_analysis)
        
        # 2. Path traversal analysis
        analyze_path_traversal_patterns(path_analysis)
        
        # 3. Node security state analysis
        analyze_node_security_states(path_analysis)
        
        # 4. Generate security report
        generate_security_report(path_analysis)
        
        print("\n✅ Advanced security analysis complete!")
        print("\n💡 Next steps:")
        print("   • Review the generated path_security_report.md")
        print("   • Address critical security findings immediately")
        print("   • Implement recommended security measures")
        print("   • Run graph_demo.py for structural analysis")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during security analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
