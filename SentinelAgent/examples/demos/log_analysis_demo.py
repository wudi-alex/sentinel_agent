#!/usr/bin/env python3
"""
Advanced Log Analysis Demo
=========================

This demo focuses on specialized log analysis features that complement unified_demo.py.
For basic log analysis, use unified_demo.py.

This demo provides:
- Advanced anomaly detection in logs
- Performance pattern analysis
- Security incident detection
- Log correlation and trend analysis
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from sentinelagent.core.log_analyzer import ExecutionLogAnalyzer
    from sentinelagent.core.tools import LogAnalysisTool
    LOG_ANALYSIS_AVAILABLE = True
except ImportError:
    LOG_ANALYSIS_AVAILABLE = False
    print("⚠️  Log analysis modules not available - using pre-existing analysis files only")


def find_available_logs():
    """Find available log files for analysis"""
    log_locations = [
        "/Users/xuhe/Documents/agent_experiments/autogen_magneticone/logs",
        "/Users/xuhe/Documents/agent_experiments/crewai_gmail/logs",
        ".",
        "logs"
    ]
    
    found_logs = []
    for location in log_locations:
        log_dir = Path(location)
        if log_dir.exists():
            # Find .txt, .csv, and .log files
            for pattern in ["*.txt", "*.csv", "*.log"]:
                found_logs.extend(log_dir.glob(pattern))
    
    return found_logs[:10]  # Return first 10 log files


def analyze_performance_patterns(analysis_result):
    """Analyze performance patterns in log analysis results"""
    if not analysis_result:
        print("❌ No analysis result available for performance analysis")
        return
        
    print("=" * 60)
    print("⚡ Performance Pattern Analysis")
    print("=" * 60)
    
    # Analyze execution paths for performance insights
    execution_paths = analysis_result.execution_paths
    print(f"📊 Analyzing {len(execution_paths)} execution paths for performance patterns...")
    
    if execution_paths:
        # Calculate average path lengths and times
        path_lengths = [len(path.nodes) for path in execution_paths]
        avg_length = sum(path_lengths) / len(path_lengths)
        max_length = max(path_lengths)
        min_length = min(path_lengths)
        
        print(f"\n📈 Execution Path Statistics:")
        print(f"   • Average path length: {avg_length:.2f} nodes")
        print(f"   • Longest path: {max_length} nodes")
        print(f"   • Shortest path: {min_length} nodes")
        
        # Find potentially problematic paths (very long)
        long_paths = [path for path in execution_paths if len(path.nodes) > avg_length * 2]
        if long_paths:
            print(f"\n⚠️  Performance Concern - Long Execution Paths ({len(long_paths)}):")
            for i, path in enumerate(long_paths[:3], 1):  # Show first 3
                print(f"   {i}. Path with {len(path.nodes)} nodes ({len(path.log_entries)} log entries)")
    
    # Analyze errors for performance impact
    errors = analysis_result.errors
    if errors:
        print(f"\n🚨 Error Analysis ({len(errors)} errors detected):")
        
        # Categorize errors by type
        error_types = {}
        for error in errors:
            error_type = error.error_type
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {error_type}: {count} occurrences")
        
        # Find performance-related errors
        performance_errors = [e for e in errors if any(keyword in e.description.lower() 
                            for keyword in ['timeout', 'slow', 'performance', 'delay', 'lag'])]
        
        if performance_errors:
            print(f"\n🐌 Performance-Related Errors ({len(performance_errors)}):")
            for error in performance_errors[:3]:  # Show first 3
                print(f"   • {error.error_type}: {error.description}")
    
    # Analyze warnings for optimization opportunities
    warnings = analysis_result.warnings
    if warnings:
        optimization_warnings = [w for w in warnings if any(keyword in w.description.lower() 
                               for keyword in ['optimize', 'inefficient', 'resource', 'memory', 'cpu'])]
        
        if optimization_warnings:
            print(f"\n🔧 Optimization Opportunities ({len(optimization_warnings)}):")
            for warning in optimization_warnings[:3]:  # Show first 3
                print(f"   • {warning.warning_type}: {warning.description}")


def analyze_security_incidents(analysis_result):
    """Analyze security-related incidents in logs"""
    if not analysis_result:
        print("❌ No analysis result available for security analysis")
        return
        
    print("=" * 60)
    print("🔒 Security Incident Analysis")
    print("=" * 60)
    
    errors = analysis_result.errors
    warnings = analysis_result.warnings
    
    # Find security-related errors
    security_errors = [e for e in errors if any(keyword in e.description.lower() 
                      for keyword in ['security', 'unauthorized', 'access', 'permission', 
                                    'authentication', 'authorization', 'breach', 'attack'])]
    
    if security_errors:
        print(f"🚨 Security Errors Detected ({len(security_errors)}):")
        for i, error in enumerate(security_errors, 1):
            severity_indicator = "🔴" if error.severity.value == "critical" else "🟠" if error.severity.value == "high" else "🟡"
            print(f"   {i}. {severity_indicator} {error.error_type} [{error.severity.value.upper()}]")
            print(f"      Description: {error.description}")
    else:
        print("✅ No security-related errors detected")
    
    # Find security-related warnings
    security_warnings = [w for w in warnings if any(keyword in w.description.lower() 
                        for keyword in ['security', 'suspicious', 'unusual', 'anomaly'])]
    
    if security_warnings:
        print(f"\n⚠️  Security Warnings ({len(security_warnings)}):")
        for i, warning in enumerate(security_warnings[:5], 1):  # Show first 5
            print(f"   {i}. {warning.warning_type}: {warning.description}")
    
    # Analyze execution paths for suspicious patterns
    execution_paths = analysis_result.execution_paths
    if execution_paths:
        print(f"\n🔍 Execution Path Security Analysis:")
        
        # Look for unusual access patterns
        admin_paths = [path for path in execution_paths if any('admin' in node.lower() or 'root' in node.lower() 
                      for node in path.nodes)]
        
        if admin_paths:
            print(f"   🔐 Administrative access paths detected: {len(admin_paths)}")
            print("      Review these paths for unauthorized access attempts")
        
        # Look for error-prone paths
        error_paths = [path for path in execution_paths if len(path.log_entries) > 0 and 
                      any('error' in entry.lower() or 'fail' in entry.lower() 
                          for entry in path.log_entries)]
        
        if error_paths:
            print(f"   ⚠️  Paths with errors: {len(error_paths)}")
            print("      These may indicate attack attempts or system vulnerabilities")


def analyze_anomaly_patterns(analysis_result):
    """Analyze anomaly patterns and outliers in log data"""
    if not analysis_result:
        print("❌ No analysis result available for anomaly analysis")
        return
        
    print("=" * 60)
    print("🔍 Advanced Anomaly Detection")
    print("=" * 60)
    
    execution_paths = analysis_result.execution_paths
    errors = analysis_result.errors
    warnings = analysis_result.warnings
    
    if execution_paths:
        # Analyze path frequency patterns
        path_patterns = {}
        for path in execution_paths:
            # Create a pattern signature based on node types/count
            signature = f"{len(path.nodes)}_nodes_{len(path.log_entries)}_entries"
            path_patterns[signature] = path_patterns.get(signature, 0) + 1
        
        print(f"📊 Execution Pattern Analysis ({len(path_patterns)} unique patterns):")
        
        # Find unusual patterns (low frequency)
        total_paths = len(execution_paths)
        unusual_patterns = [(pattern, count) for pattern, count in path_patterns.items() 
                          if count / total_paths < 0.1]  # Less than 10% frequency
        
        if unusual_patterns:
            print(f"\n🔍 Unusual Execution Patterns ({len(unusual_patterns)}):")
            for pattern, count in unusual_patterns[:5]:  # Show first 5
                percentage = (count / total_paths) * 100
                print(f"   • {pattern}: {count} occurrences ({percentage:.1f}%)")
        
        # Analyze error clustering
        if errors:
            error_timeline = {}
            for error in errors:
                # Group errors by type and rough timing
                key = f"{error.error_type}"
                error_timeline[key] = error_timeline.get(key, 0) + 1
            
            print(f"\n🚨 Error Pattern Analysis:")
            
            # Find error spikes (high frequency errors)
            avg_error_frequency = len(errors) / len(error_timeline) if error_timeline else 0
            high_frequency_errors = [(error_type, count) for error_type, count in error_timeline.items() 
                                   if count > avg_error_frequency * 2]
            
            if high_frequency_errors:
                print(f"   ⚠️  High-frequency error types (potential systemic issues):")
                for error_type, count in high_frequency_errors:
                    print(f"      • {error_type}: {count} occurrences")
        
        # Analyze warning patterns
        if warnings:
            warning_types = {}
            for warning in warnings:
                warning_types[warning.warning_type] = warning_types.get(warning.warning_type, 0) + 1
            
            print(f"\n⚠️  Warning Pattern Analysis:")
            for warning_type, count in sorted(warning_types.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   • {warning_type}: {count} occurrences")


def generate_comprehensive_log_report(analysis_results, output_file="comprehensive_log_analysis.md"):
    """Generate a comprehensive log analysis report"""
    if not analysis_results:
        print("❌ Cannot generate report - no analysis results")
        return
    
    print(f"\n📄 Generating comprehensive log analysis report: {output_file}")
    
    # Aggregate statistics from all analysis results
    total_paths = sum(len(result.execution_paths) for result in analysis_results)
    total_errors = sum(len(result.errors) for result in analysis_results)
    total_warnings = sum(len(result.warnings) for result in analysis_results)
    
    report_content = f"""# Comprehensive Log Analysis Report
Generated: {Path().cwd()}

## 📊 Executive Summary
- **Total Execution Paths**: {total_paths}
- **Total Errors**: {total_errors}
- **Total Warnings**: {total_warnings}
- **Files Analyzed**: {len(analysis_results)}

## 🚨 Critical Findings
"""
    
    # Add critical errors
    all_errors = []
    for result in analysis_results:
        all_errors.extend(result.errors)
    
    critical_errors = [e for e in all_errors if e.severity.value == "critical"]
    if critical_errors:
        report_content += f"\n### Critical Errors ({len(critical_errors)})\n"
        for error in critical_errors[:5]:  # Show first 5
            report_content += f"- **{error.error_type}**: {error.description}\n"
    
    # Add security findings
    security_errors = [e for e in all_errors if any(keyword in e.description.lower() 
                      for keyword in ['security', 'unauthorized', 'access', 'permission'])]
    
    if security_errors:
        report_content += f"\n### Security Issues ({len(security_errors)})\n"
        for error in security_errors[:3]:  # Show first 3
            report_content += f"- **{error.error_type}**: {error.description}\n"
    
    # Add performance insights
    report_content += f"\n## ⚡ Performance Insights\n"
    if total_paths > 0:
        avg_path_length = sum(len(path.nodes) for result in analysis_results 
                            for path in result.execution_paths) / total_paths
        report_content += f"- Average execution path length: {avg_path_length:.2f} nodes\n"
        report_content += f"- Error rate: {(total_errors / total_paths * 100):.1f}%\n"
    
    # Save report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Comprehensive report saved: {output_file}")


def main():
    """Main demo function"""
    print("📊 SentinelAgent - Advanced Log Analysis Demo")
    print("=" * 60)
    print("Note: For basic log analysis, use unified_demo.py")
    print("This demo focuses on advanced log analysis and anomaly detection.")
    print("=" * 60)
    
    if not LOG_ANALYSIS_AVAILABLE:
        print("❌ Log analysis modules not available")
        print("Please ensure all dependencies are installed")
        return
    
    try:
        # Find available log files
        log_files = find_available_logs()
        
        if not log_files:
            print("❌ No log files found for analysis")
            print("Please ensure log files are available in expected locations")
            return
        
        print(f"📁 Found {len(log_files)} log files for analysis")
        
        # Create analyzer
        analyzer = ExecutionLogAnalyzer()
        analysis_results = []
        
        # Analyze each log file
        for i, log_file in enumerate(log_files[:3], 1):  # Analyze first 3 files
            print(f"\n📊 Analyzing log file {i}: {log_file.name}")
            
            try:
                result = analyzer.analyze_log_file(str(log_file))
                analysis_results.append(result)
                
                print(f"   ✅ Analysis complete:")
                print(f"      - Execution paths: {len(result.execution_paths)}")
                print(f"      - Errors: {len(result.errors)}")
                print(f"      - Warnings: {len(result.warnings)}")
                
            except Exception as e:
                print(f"   ❌ Analysis failed: {e}")
        
        if analysis_results:
            print(f"\n🔍 Performing advanced analysis on {len(analysis_results)} log files...")
            
            # Perform advanced analysis on the first result
            main_result = analysis_results[0]
            
            # 1. Performance pattern analysis
            analyze_performance_patterns(main_result)
            
            # 2. Security incident analysis
            analyze_security_incidents(main_result)
            
            # 3. Anomaly detection
            analyze_anomaly_patterns(main_result)
            
            # 4. Generate comprehensive report
            generate_comprehensive_log_report(analysis_results)
            
            print("\n✅ Advanced log analysis complete!")
            print("\n💡 Next steps:")
            print("   • Review the generated comprehensive_log_analysis.md")
            print("   • Address critical errors and security issues")
            print("   • Investigate anomaly patterns")
            print("   • Monitor performance indicators")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during log analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
