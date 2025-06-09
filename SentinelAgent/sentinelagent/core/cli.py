#!/usr/bin/env python3
"""
SentinelAgent - Command Line Interface
CLI tool for AI Agent system analysis and monitoring platform
"""

import sys
import json
from pathlib import Path
from .scanner import scan_directory, scan_file
from .graph_builder import build_graph_from_scan, build_and_save_graph, scan_and_build_graph
from .path_analyzer import analyze_graph_paths, analyze_and_save_paths, analyze_paths_from_file
from .log_analyzer import ExecutionLogAnalyzer
from ..utils.path_resolver import resolve_path


def print_usage():
    """Print usage instructions"""
    print("🔍 SentinelAgent - Agent System Analysis & Monitoring Platform")
    print("\nUsage:")
    print("  sentinelagent <target_path> [options]")
    print("  sentinelagent --analyze-graph <graph_file> [options]")
    print("  sentinelagent --analyze-logs <log_file> [options]")
    print("\nAlternative (using Python module):")
    print("  python -m sentinelagent.cli.main <target_path> [options]")
    print("\nArguments:")
    print("  target_path        Directory or file path to scan")
    print("\nOptions:")
    print("  -o, --output     Specify scan output file name (default: scan_result.json)")
    print("  -g, --graph      Build and save relationship graph (requires graph output file name)")
    print("  -p, --paths      Perform path analysis and save (requires path analysis output file name)")
    print("  -a, --all        Perform full analysis (scan + graph build + path analysis)")
    print("  --analyze-graph  Analyze an existing graph file")
    print("  --analyze-logs   Analyze execution log file")
    print("  --log-format     Specify log format (csv/txt/auto, default: auto)")
    print("  --log-output     Specify log analysis output file")
    print("  -v, --verbose    Show detailed information")
    print("  -h, --help       Show this help message")
    print("\nExamples:")
    print("  sentinelagent /Users/xuhe/Documents/agent_experiments/crewai_gmail")
    print("  sentinelagent /Users/xuhe/Documents/agent_experiments/crewai_gmail --output gmail_scan.json")
    print("  sentinelagent /Users/xuhe/Documents/agent_experiments/crewai_gmail --graph gmail_graph.json")
    print("  sentinelagent /Users/xuhe/Documents/agent_experiments/crewai_gmail --paths gmail_paths.json") 
    print("  sentinelagent /Users/xuhe/Documents/agent_experiments/crewai_gmail --all")
    print("  sentinelagent --analyze-graph gmail_graph.json")
    print("  sentinelagent --analyze-logs /Users/xuhe/Documents/agent_experiments/autogen_magneticone/logs/log_2025-05-17_17-47-03.txt")
    print("  sentinelagent --analyze-logs /Users/xuhe/Documents/agent_experiments/autogen_magneticone/logs/magentic-one-file-code-execution.csv --log-format csv")
    print("  sentinelagent tools.py --verbose")
    print("\nWeb Interface:")
    print("  sentinelagent-web                    # Start web interface")
    print("  python -m sentinelagent.cli.start_web_ui  # Alternative method")
    print("\nNote:")
    print("  • Install as package: pip install -e .")
    print("  • Relative paths like '../crewai_gmail' will be automatically resolved in Docker containers")
    print("  • Paths in the container will be mapped to the /app/projects/ directory")


def format_summary(summary):
    """Format summary information"""
    return f"""📊 Scan summary:
  🤖 Agents: {summary['total_agents']}
  🔧 Tools: {summary['total_tools']}
  👥 Crews: {summary['total_crews']}
  📋 Tasks: {summary['total_tasks']}
  📄 Files: {summary['total_files']}"""


def format_details(result, verbose=False):
    """Format detailed information"""
    details = []
    
    if result['agents'] and verbose:
        details.append("\n🤖 Discovered Agents:")
        for agent in result['agents'][:10]:  # Show up to 10
            details.append(f"  - {agent['name']} ({agent['type']})")
            if 'role' in agent.get('arguments', {}):
                details.append(f"    Role: {agent['arguments']['role']}")
    
    if result['tools'] and verbose:
        details.append("\n🔧 Discovered Tools:")
        for tool in result['tools'][:10]:  # Show up to 10
            details.append(f"  - {tool['name']} ({tool['type']})")
    
    return "\n".join(details)


def format_path_summary(path_analysis):
    """Format path analysis summary"""
    overall = path_analysis.get('overall_assessment', {})
    return f"""🛣️  Path analysis summary:
  🎯 Overall risk score: {overall.get('total_risk_score', 0):.3f}
  ⚠️  Risk level: {overall.get('risk_level', 'unknown').upper()}
  📊 Paths analyzed: {overall.get('total_paths_analyzed', 0)}
  🚨 Suspicious patterns found: {overall.get('suspicious_patterns_found', 0)}"""


def format_path_details(path_analysis, verbose=False):
    """Format path analysis detailed information"""
    details = []
    
    if verbose:
        # Display path type distribution
        path_types = path_analysis.get('path_analysis', {}).get('path_type_distribution', {})
        if path_types:
            details.append("\n🛣️  Path type distribution:")
            for path_type, count in path_types.items():
                details.append(f"  - {path_type}: {count}")
        
        # Display suspicious patterns
        patterns = path_analysis.get('suspicious_patterns', [])
        if patterns:
            details.append("\n🚨 Suspicious patterns found:")
            for i, pattern in enumerate(patterns[:5], 1):  # Show up to 5
                details.append(f"  {i}. {pattern.get('pattern_type', 'unknown')} "
                             f"(Severity: {pattern.get('severity', 'unknown')})")
                details.append(f"     {pattern.get('details', '')}")
            if len(patterns) > 5:
                details.append(f"  ... {len(patterns) - 5} more patterns")
        
        # Display recommendations
        recommendations = path_analysis.get('recommendations', [])
        if recommendations:
            details.append("\n💡 Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):  # Show up to 3
                details.append(f"  {i}. {rec}")
            if len(recommendations) > 3:
                details.append(f"  ... {len(recommendations) - 3} more recommendations")
    
    return "\n".join(details)


def format_log_summary(analysis_result):
    """Format log analysis summary"""
    stats = analysis_result.statistics
    return f"""📊 Log analysis summary:
  🛣️  Execution paths: {len(analysis_result.execution_paths)}
  ❌ Errors: {len(analysis_result.errors)}
  ⚠️  Warnings: {len(analysis_result.warnings)}
  📝 Log entries: {stats.get('total_entries', 0)}
  🤖 Active Agents: {stats.get('active_agents', 0)}
  ⏱️  Execution duration: {stats.get('total_duration', 'N/A')}"""


def format_log_details(analysis_result, verbose=False):
    """Format log analysis detailed information"""
    details = []
    
    if verbose and analysis_result.errors:
        details.append("\n❌ Errors found:")
        for i, error in enumerate(analysis_result.errors[:10], 1):  # Show up to 10
            details.append(f"  {i}. {error.error_type} ({error.severity.value.upper()})")
            details.append(f"     Node: {error.node_or_edge}")
            details.append(f"     Description: {error.description}")
            if error.suggested_fix:
                details.append(f"     Suggestion: {error.suggested_fix}")
    
    if verbose and analysis_result.warnings:
        details.append("\n⚠️  Warnings:")
        for i, warning in enumerate(analysis_result.warnings[:5], 1):  # Show up to 5
            details.append(f"  {i}. {warning}")
    
    if verbose and analysis_result.recommendations:
        details.append("\n💡 Recommendations:")
        for i, rec in enumerate(analysis_result.recommendations[:5], 1):  # Show up to 5
            details.append(f"  {i}. {rec}")
    
    return "\n".join(details)


def main():
    """Main function"""
    args = sys.argv[1:]
    
    # Parse arguments
    if not args or '--help' in args or '-h' in args:
        print_usage()
        return
    
    # Check if analyze graph file pattern
    if '--analyze-graph' in args:
        return analyze_graph_mode(args)
    
    # Check if analyze log file pattern
    if '--analyze-logs' in args:
        return analyze_logs_mode(args)
    
    target_path = args[0]
    output_file = "scan_result.json"
    graph_file = None
    paths_file = None
    verbose = False
    full_analysis = False
    
    # Parse options
    i = 1
    while i < len(args):
        if args[i] in ['-o', '--output'] and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] in ['-g', '--graph'] and i + 1 < len(args):
            graph_file = args[i + 1]
            i += 2
        elif args[i] in ['-p', '--paths'] and i + 1 < len(args):
            paths_file = args[i + 1]
            i += 2
        elif args[i] in ['-a', '--all']:
            full_analysis = True
            i += 1
        elif args[i] in ['-v', '--verbose']:
            verbose = True
            i += 1
        else:
            i += 1
    
    # If full analysis enabled, auto set output file names
    if full_analysis:
        base_name = Path(target_path).name
        if not graph_file:
            graph_file = f"graph_{base_name}.json"
        if not paths_file:
            paths_file = f"paths_{base_name}.json"
    # Check target path - support path parsing
    original_path = target_path
    resolved_path = resolve_path(target_path)
    path = Path(resolved_path)
    
    if not path.exists():
        print(f"❌ Error: Path does not exist '{original_path}' (resolved as: {resolved_path})")
        return

    # Execute scan
    print(f"🔍 Scanning: {original_path}")
    if original_path != resolved_path:
        print(f"    Resolved path: {resolved_path}")
    print("-" * 50)

    try:
        if path.is_dir():
            result = scan_directory(resolved_path)
            scan_type = "Directory"
        else:
            result = scan_file(resolved_path)
            scan_type = "File"
        
        # Display scan result
        print(f"✅ {scan_type} scan completed!")
        print(format_summary(result['scan_summary']))
        
        if verbose:
            print(format_details(result, verbose=True))
        
        # Save scan result
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Scan result saved to: {output_file}")
        
        # Build and save graph (if graph output file specified)
        graph_data = None
        if graph_file or paths_file:
            print(f"\n🔗 Building relationship graph...")
            graph_data = build_and_save_graph(result, graph_file or "temp_graph.json")
            print(f"✅ Relationship graph built!")
            print(f"📊 Graph stats: {graph_data['graph_summary']['total_nodes']} nodes, "
                  f"{graph_data['graph_summary']['total_edges']} edges")
            if graph_file:
                print(f"💾 Graph saved to: {graph_file}")
        
        # Path analysis (if path output file specified or full analysis enabled)
        if paths_file:
            print(f"\n🛣️  Analyzing paths...")
            if graph_data is None:
                # If graph not built yet, build it first
                graph_data = build_graph_from_scan(result)
            
            path_analysis = analyze_and_save_paths(graph_data, paths_file)
            print(f"✅ Path analysis completed!")
            print(format_path_summary(path_analysis))
            
            if verbose:
                print(format_path_details(path_analysis, verbose=True))
            
            print(f"💾 Path analysis saved to: {paths_file}")
        
        # Information hints
        if not verbose and (result['agents'] or result['tools']):
            print("💡 Use --verbose option to see detailed information")
        
        if not graph_file and result['scan_summary']['total_agents'] > 0:
            print("💡 Use --graph option to build component relationship graph")
        
        if not paths_file and result['scan_summary']['total_agents'] > 0:
            print("💡 Use --paths option for path analysis")
        
        if not full_analysis and result['scan_summary']['total_agents'] > 0:
            print("💡 Use --all option to perform full analysis")
    
    except Exception as e:
        print(f"❌ Scan failed: {e}")
        return 1


def analyze_graph_mode(args):
    """Analyze graph file pattern"""
    graph_file = None
    paths_file = None
    verbose = False
    
    # Find graph file argument
    try:
        graph_idx = args.index('--analyze-graph')
        if graph_idx + 1 < len(args):
            graph_file = args[graph_idx + 1]
    except (ValueError, IndexError):
        print("❌ Error: --analyze-graph requires a graph file path")
        return 1
    
    # Parse other options
    i = 0
    while i < len(args):
        if args[i] in ['-p', '--paths'] and i + 1 < len(args):
            paths_file = args[i + 1]
            i += 2
        elif args[i] in ['-v', '--verbose']:
            verbose = True
            i += 1
        else:
            i += 1
    
    # Set default output file name
    if not paths_file:
        graph_path = Path(graph_file)
        paths_file = f"paths_{graph_path.stem}.json"
    
    # Check if graph file exists
    if not Path(graph_file).exists():
        print(f"❌ Error: Graph file does not exist '{graph_file}'")
        return 1
    
    print(f"🛣️  Analyzing graph file: {graph_file}")
    print("-" * 50)
    
    try:
        # Read graph data and analyze paths
        path_analysis = analyze_paths_from_file(graph_file, paths_file)
        
        print(f"✅ Path analysis completed!")
        print(format_path_summary(path_analysis))
        
        if verbose:
            print(format_path_details(path_analysis, verbose=True))
        
        print(f"💾 Path analysis saved to: {paths_file}")
        
        # Information hint
        if not verbose:
            print("💡 Use --verbose option to see detailed information")
    
    except Exception as e:
        print(f"❌ Path analysis failed: {e}")
        return 1


def analyze_logs_mode(args):
    """Analyze log file pattern"""
    log_file = None
    log_format = "auto"
    output_file = None
    verbose = False
    
    # Find log file argument
    try:
        log_idx = args.index('--analyze-logs')
        if log_idx + 1 < len(args):
            log_file = args[log_idx + 1]
    except (ValueError, IndexError):
        print("❌ Error: --analyze-logs requires a log file path")
        return 1
    
    # Parse other options
    i = 0
    while i < len(args):
        if args[i] == '--log-format' and i + 1 < len(args):
            log_format = args[i + 1]
            i += 2
        elif args[i] == '--log-output' and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] in ['-v', '--verbose']:
            verbose = True
            i += 1
        else:
            i += 1
    
    # Set default output file name
    if not output_file:
        log_path = Path(log_file)
        output_file = f"analysis_{log_path.stem}.json"
    
    # Check if log file exists
    if not Path(log_file).exists():
        print(f"❌ Error: Log file does not exist '{log_file}'")
        return 1
    
    print(f"📊 Analyzing log file: {log_file}")
    print(f"📝 Log format: {log_format}")
    print("-" * 50)
    
    try:
        # Create analyzer and analyze log
        analyzer = ExecutionLogAnalyzer()
        analysis_result = analyzer.analyze_log_file(log_file, log_format)
        
        print(f"✅ Log analysis completed!")
        print(format_log_summary(analysis_result))
        
        if verbose:
            print(format_log_details(analysis_result, verbose=True))
        
        # Save analysis result
        analysis_dict = {
            'execution_paths': [
                {
                    'path_id': path.path_id,
                    'nodes': path.nodes,
                    'edges': path.edges,
                    'start_time': path.start_time.isoformat() if path.start_time else None,
                    'end_time': path.end_time.isoformat() if path.end_time else None,
                    'status': path.status,
                    'log_entries_count': len(path.log_entries)
                }
                for path in analysis_result.execution_paths
            ],
            'errors': [
                {
                    'error_type': error.error_type,
                    'severity': error.severity.value,
                    'description': error.description,
                    'node_or_edge': error.node_or_edge,
                    'suggested_fix': error.suggested_fix,
                    'context': error.context
                }
                for error in analysis_result.errors
            ],
            'warnings': analysis_result.warnings,
            'statistics': analysis_result.statistics,
            'recommendations': analysis_result.recommendations,
            'summary': analysis_result.summary
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Analysis result saved to: {output_file}")
        
        # Information hint
        if not verbose and (analysis_result.errors or analysis_result.warnings):
            print("💡 Use --verbose option to see detailed information")
    
    except Exception as e:
        print(f"❌ Log analysis failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main() or 0)
