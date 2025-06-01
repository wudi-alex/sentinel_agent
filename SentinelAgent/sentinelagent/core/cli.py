#!/usr/bin/env python3
"""
SentinelAgent - 命令行接口
AI Agent系统分析与监控平台的命令行工具
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
    """打印使用说明"""
    print("🔍 Inspector Agent - Agent系统结构扫描器")
    print("\n使用方法:")
    print("  python cli.py <目标路径> [选项]")
    print("  python cli.py --analyze-graph <图文件> [选项]")
    print("  python cli.py --analyze-logs <日志文件> [选项]")
    print("\n参数:")
    print("  目标路径          要扫描的目录或文件路径")
    print("\n选项:")
    print("  -o, --output     指定扫描输出文件名 (默认: scan_result.json)")
    print("  -g, --graph      同时构建关系图并保存 (需要指定图输出文件名)")
    print("  -p, --paths      同时进行路径分析并保存 (需要指定路径分析输出文件名)")
    print("  -a, --all        执行完整分析 (扫描+图构建+路径分析)")
    print("  --analyze-graph  分析已有的图文件")
    print("  --analyze-logs   分析执行日志文件")
    print("  --log-format     指定日志格式 (csv/txt/auto, 默认: auto)")
    print("  --log-output     指定日志分析输出文件")
    print("  -v, --verbose    显示详细信息")
    print("  -h, --help       显示此帮助信息")
    print("\n示例:")
    print("  python cli.py ../crewai_gmail")
    print("  python cli.py ../crewai_gmail --output gmail_scan.json")
    print("  python cli.py ../crewai_gmail --graph gmail_graph.json")
    print("  python cli.py ../crewai_gmail --paths gmail_paths.json") 
    print("  python cli.py ../crewai_gmail --all")
    print("  python cli.py --analyze-graph gmail_graph.json")
    print("  python cli.py --analyze-logs ../autogen_magneticone/logs/log_2025-05-17_17-47-03.txt")
    print("  python cli.py --analyze-logs ../magentic-one-file-code-execution.csv --log-format csv")
    print("  python cli.py tools.py --verbose")
    print("\n注意:")
    print("  • 相对路径如 '../crewai_gmail' 在Docker容器中会自动解析")
    print("  • 容器中的路径会映射到 /app/projects/ 目录下")


def format_summary(summary):
    """格式化摘要信息"""
    return f"""📊 扫描摘要:
  🤖 Agents: {summary['total_agents']}
  🔧 Tools: {summary['total_tools']}
  👥 Crews: {summary['total_crews']}
  📋 Tasks: {summary['total_tasks']}
  📄 Files: {summary['total_files']}"""


def format_details(result, verbose=False):
    """格式化详细信息"""
    details = []
    
    if result['agents'] and verbose:
        details.append("\n🤖 发现的Agents:")
        for agent in result['agents'][:10]:  # 最多显示10个
            details.append(f"  - {agent['name']} ({agent['type']})")
            if 'role' in agent.get('arguments', {}):
                details.append(f"    角色: {agent['arguments']['role']}")
    
    if result['tools'] and verbose:
        details.append("\n🔧 发现的Tools:")
        for tool in result['tools'][:10]:  # 最多显示10个
            details.append(f"  - {tool['name']} ({tool['type']})")
    
    return "\n".join(details)


def format_path_summary(path_analysis):
    """格式化路径分析摘要"""
    overall = path_analysis.get('overall_assessment', {})
    return f"""🛣️  路径分析摘要:
  🎯 总体风险评分: {overall.get('total_risk_score', 0):.3f}
  ⚠️  风险等级: {overall.get('risk_level', 'unknown').upper()}
  📊 分析路径数: {overall.get('total_paths_analyzed', 0)}
  🚨 可疑模式数: {overall.get('suspicious_patterns_found', 0)}"""


def format_path_details(path_analysis, verbose=False):
    """格式化路径分析详细信息"""
    details = []
    
    if verbose:
        # 显示路径类型分布
        path_types = path_analysis.get('path_analysis', {}).get('path_type_distribution', {})
        if path_types:
            details.append("\n🛣️  路径类型分布:")
            for path_type, count in path_types.items():
                details.append(f"  - {path_type}: {count}")
        
        # 显示可疑模式
        patterns = path_analysis.get('suspicious_patterns', [])
        if patterns:
            details.append("\n🚨 发现的可疑模式:")
            for i, pattern in enumerate(patterns[:5], 1):  # 最多显示5个
                details.append(f"  {i}. {pattern.get('pattern_type', 'unknown')} "
                             f"(严重程度: {pattern.get('severity', 'unknown')})")
                details.append(f"     {pattern.get('details', '')}")
            if len(patterns) > 5:
                details.append(f"  ... 还有 {len(patterns) - 5} 个模式")
        
        # 显示建议
        recommendations = path_analysis.get('recommendations', [])
        if recommendations:
            details.append("\n💡 改进建议:")
            for i, rec in enumerate(recommendations[:3], 1):  # 最多显示3个
                details.append(f"  {i}. {rec}")
            if len(recommendations) > 3:
                details.append(f"  ... 还有 {len(recommendations) - 3} 个建议")
    
    return "\n".join(details)


def format_log_summary(analysis_result):
    """格式化日志分析摘要"""
    stats = analysis_result.statistics
    return f"""📊 日志分析摘要:
  🛣️  执行路径: {len(analysis_result.execution_paths)}
  ❌ 错误数量: {len(analysis_result.errors)}
  ⚠️  警告数量: {len(analysis_result.warnings)}
  📝 日志条目: {stats.get('total_entries', 0)}
  🤖 活跃Agents: {stats.get('active_agents', 0)}
  ⏱️  执行时长: {stats.get('total_duration', 'N/A')}"""


def format_log_details(analysis_result, verbose=False):
    """格式化日志分析详细信息"""
    details = []
    
    if verbose and analysis_result.errors:
        details.append("\n❌ 发现的错误:")
        for i, error in enumerate(analysis_result.errors[:10], 1):  # 最多显示10个
            details.append(f"  {i}. {error.error_type} ({error.severity.value.upper()})")
            details.append(f"     节点: {error.node_or_edge}")
            details.append(f"     描述: {error.description}")
            if error.suggested_fix:
                details.append(f"     建议: {error.suggested_fix}")
    
    if verbose and analysis_result.warnings:
        details.append("\n⚠️  警告信息:")
        for i, warning in enumerate(analysis_result.warnings[:5], 1):  # 最多显示5个
            details.append(f"  {i}. {warning}")
    
    if verbose and analysis_result.recommendations:
        details.append("\n💡 改进建议:")
        for i, rec in enumerate(analysis_result.recommendations[:5], 1):  # 最多显示5个
            details.append(f"  {i}. {rec}")
    
    return "\n".join(details)


def main():
    """主函数"""
    args = sys.argv[1:]
    
    # 解析参数
    if not args or '--help' in args or '-h' in args:
        print_usage()
        return
    
    # 检查是否是分析图文件模式
    if '--analyze-graph' in args:
        return analyze_graph_mode(args)
    
    # 检查是否是分析日志文件模式
    if '--analyze-logs' in args:
        return analyze_logs_mode(args)
    
    # 检查是否是分析日志文件模式
    if '--analyze-logs' in args:
        return analyze_logs_mode(args)
    
    target_path = args[0]
    output_file = "scan_result.json"
    graph_file = None
    paths_file = None
    verbose = False
    full_analysis = False
    
    # 解析选项
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
    
    # 如果启用完整分析，自动设置输出文件名
    if full_analysis:
        base_name = Path(target_path).name
        if not graph_file:
            graph_file = f"graph_{base_name}.json"
        if not paths_file:
            paths_file = f"paths_{base_name}.json"
     # 检查目标路径 - 支持路径解析
    original_path = target_path
    resolved_path = resolve_path(target_path)
    path = Path(resolved_path)
    
    if not path.exists():
        print(f"❌ 错误: 路径不存在 '{original_path}' (解析为: {resolved_path})")
        return

    # 执行扫描
    print(f"🔍 正在扫描: {original_path}")
    if original_path != resolved_path:
        print(f"    解析路径: {resolved_path}")
    print("-" * 50)

    try:
        if path.is_dir():
            result = scan_directory(resolved_path)
            scan_type = "目录"
        else:
            result = scan_file(resolved_path)
            scan_type = "文件"
        
        # 显示扫描结果
        print(f"✅ {scan_type}扫描完成!")
        print(format_summary(result['scan_summary']))
        
        if verbose:
            print(format_details(result, verbose=True))
        
        # 保存扫描结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 扫描结果已保存到: {output_file}")
        
        # 构建并保存图（如果指定了图输出文件）
        graph_data = None
        if graph_file or paths_file:
            print(f"\n🔗 正在构建关系图...")
            graph_data = build_and_save_graph(result, graph_file or "temp_graph.json")
            print(f"✅ 关系图构建完成!")
            print(f"📊 图统计: {graph_data['graph_summary']['total_nodes']} 个节点, "
                  f"{graph_data['graph_summary']['total_edges']} 条边")
            if graph_file:
                print(f"💾 关系图已保存到: {graph_file}")
        
        # 路径分析（如果指定了路径输出文件或启用了完整分析）
        if paths_file:
            print(f"\n🛣️  正在分析路径...")
            if graph_data is None:
                # 如果还没有构建图，先构建
                graph_data = build_graph_from_scan(result)
            
            path_analysis = analyze_and_save_paths(graph_data, paths_file)
            print(f"✅ 路径分析完成!")
            print(format_path_summary(path_analysis))
            
            if verbose:
                print(format_path_details(path_analysis, verbose=True))
            
            print(f"💾 路径分析已保存到: {paths_file}")
        
        # 提示信息
        if not verbose and (result['agents'] or result['tools']):
            print("💡 使用 --verbose 选项查看详细信息")
        
        if not graph_file and result['scan_summary']['total_agents'] > 0:
            print("💡 使用 --graph 选项构建组件关系图")
        
        if not paths_file and result['scan_summary']['total_agents'] > 0:
            print("💡 使用 --paths 选项进行路径分析")
        
        if not full_analysis and result['scan_summary']['total_agents'] > 0:
            print("💡 使用 --all 选项执行完整分析")
    
    except Exception as e:
        print(f"❌ 扫描失败: {e}")
        return 1


def analyze_graph_mode(args):
    """分析图文件模式"""
    graph_file = None
    paths_file = None
    verbose = False
    
    # 查找图文件参数
    try:
        graph_idx = args.index('--analyze-graph')
        if graph_idx + 1 < len(args):
            graph_file = args[graph_idx + 1]
    except (ValueError, IndexError):
        print("❌ 错误: --analyze-graph 需要指定图文件路径")
        return 1
    
    # 解析其他选项
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
    
    # 设置默认输出文件名
    if not paths_file:
        graph_path = Path(graph_file)
        paths_file = f"paths_{graph_path.stem}.json"
    
    # 检查图文件是否存在
    if not Path(graph_file).exists():
        print(f"❌ 错误: 图文件不存在 '{graph_file}'")
        return 1
    
    print(f"🛣️  正在分析图文件: {graph_file}")
    print("-" * 50)
    
    try:
        # 读取图数据并分析路径
        path_analysis = analyze_paths_from_file(graph_file, paths_file)
        
        print(f"✅ 路径分析完成!")
        print(format_path_summary(path_analysis))
        
        if verbose:
            print(format_path_details(path_analysis, verbose=True))
        
        print(f"💾 路径分析已保存到: {paths_file}")
        
        # 提示信息
        if not verbose:
            print("💡 使用 --verbose 选项查看详细信息")
    
    except Exception as e:
        print(f"❌ 路径分析失败: {e}")
        return 1


def analyze_logs_mode(args):
    """分析日志文件模式"""
    log_file = None
    log_format = "auto"
    output_file = None
    verbose = False
    
    # 查找日志文件参数
    try:
        log_idx = args.index('--analyze-logs')
        if log_idx + 1 < len(args):
            log_file = args[log_idx + 1]
    except (ValueError, IndexError):
        print("❌ 错误: --analyze-logs 需要指定日志文件路径")
        return 1
    
    # 解析其他选项
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
    
    # 设置默认输出文件名
    if not output_file:
        log_path = Path(log_file)
        output_file = f"analysis_{log_path.stem}.json"
    
    # 检查日志文件是否存在
    if not Path(log_file).exists():
        print(f"❌ 错误: 日志文件不存在 '{log_file}'")
        return 1
    
    print(f"📊 正在分析日志文件: {log_file}")
    print(f"📝 日志格式: {log_format}")
    print("-" * 50)
    
    try:
        # 创建分析器并分析日志
        analyzer = ExecutionLogAnalyzer()
        analysis_result = analyzer.analyze_log_file(log_file, log_format)
        
        print(f"✅ 日志分析完成!")
        print(format_log_summary(analysis_result))
        
        if verbose:
            print(format_log_details(analysis_result, verbose=True))
        
        # 保存分析结果
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
        
        print(f"💾 分析结果已保存到: {output_file}")
        
        # 提示信息
        if not verbose and (analysis_result.errors or analysis_result.warnings):
            print("💡 使用 --verbose 选项查看详细信息")
    
    except Exception as e:
        print(f"❌ 日志分析失败: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main() or 0)
