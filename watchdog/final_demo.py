#!/usr/bin/env python3
"""
Inspector Agent - 最终综合演示
展示Inspector Agent的完整功能和实际应用价值
"""

import json
import os
from pathlib import Path
from scanner import AgentSystemScanner
from tools import DirectoryScanTool, FileScanTool, ReportAnalysisTool


def comprehensive_demo():
    """综合功能演示"""
    print("🔍 Inspector Agent - 综合功能演示")
    print("=" * 60)
    print("版本: v1.1 | 日期: 2025-05-28")
    print("=" * 60)
    
    # 1. 创建增强版扫描器
    print("\n🚀 初始化增强版扫描器...")
    scanner = AgentSystemScanner(verbose=False)
    
    # 2. 多项目扫描对比
    print("\n📊 多项目扫描对比分析")
    print("-" * 40)
    
    projects = {
        'Inspector Watchdog': '.',
        'CrewAI Gmail': '../crewai_gmail',
        'AutoGen MagneticOne': '../autogen_magneticone'
    }
    
    scan_results = {}
    
    for project_name, path in projects.items():
        if os.path.exists(path):
            print(f"   🔍 扫描 {project_name}...")
            try:
                result = scanner.scan_directory(path)
                scan_results[project_name] = result
                summary = result['scan_summary']
                status = "✅" if summary['scan_status'] == 'completed_successfully' else "⚠️"
                print(f"   {status} {summary['total_agents']} agents, {summary['total_tools']} tools, {summary['total_crews']} crews")
            except Exception as e:
                print(f"   ❌ 扫描失败: {e}")
        else:
            print(f"   ⚠️  路径不存在: {path}")
    
    # 3. 详细分析展示
    print(f"\n🔬 详细组件分析")
    print("-" * 40)
    
    for project_name, result in scan_results.items():
        print(f"\n📁 {project_name}:")
        
        # 显示Agents
        if result['agents']:
            print(f"   🤖 Agents ({len(result['agents'])}):")
            for i, agent in enumerate(result['agents'][:3], 1):
                agent_type = agent.get('type', 'unknown')
                file_name = Path(agent['file']).name
                print(f"      {i}. {agent['name']} ({agent_type}) - {file_name}")
            if len(result['agents']) > 3:
                print(f"      ... 和其他 {len(result['agents']) - 3} 个agents")
        
        # 显示Tools
        if result['tools']:
            print(f"   🔧 Tools ({len(result['tools'])}):")
            for i, tool in enumerate(result['tools'][:3], 1):
                tool_type = tool.get('type', 'unknown')
                file_name = Path(tool['file']).name
                print(f"      {i}. {tool['name']} ({tool_type}) - {file_name}")
            if len(result['tools']) > 3:
                print(f"      ... 和其他 {len(result['tools']) - 3} 个tools")
    
    # 4. CrewAI工具演示
    print(f"\n🛠️ CrewAI工具集成演示")
    print("-" * 40)
    
    print("   📂 测试DirectoryScanTool...")
    dir_tool = DirectoryScanTool()
    tool_result = dir_tool._run('.', 'comprehensive_demo_scan.json')
    print("   ✅ 目录扫描工具正常")
    
    print("   📋 测试ReportAnalysisTool...")
    report_tool = ReportAnalysisTool()
    if os.path.exists('comprehensive_demo_scan.json'):
        analysis = report_tool._run('comprehensive_demo_scan.json')
        print("   ✅ 报告分析工具正常")
    
    # 5. 架构模式分析
    print(f"\n🏗️ 架构模式识别")
    print("-" * 40)
    
    for project_name, result in scan_results.items():
        patterns = analyze_project_patterns(result)
        if patterns:
            print(f"   {project_name}:")
            for pattern in patterns:
                print(f"      • {pattern}")
    
    # 6. 生成综合报告
    print(f"\n📈 生成综合分析报告")
    print("-" * 40)
    
    comprehensive_report = {
        'demo_info': {
            'version': 'v1.1',
            'timestamp': '2025-05-28',
            'projects_scanned': len(scan_results)
        },
        'project_results': scan_results,
        'comparison_summary': generate_comparison_summary(scan_results),
        'architecture_analysis': {
            project: analyze_project_patterns(result) 
            for project, result in scan_results.items()
        },
        'capabilities_demonstrated': [
            'Multi-project scanning',
            'Component identification', 
            'Architecture pattern recognition',
            'Error handling and recovery',
            'CrewAI tool integration',
            'Comprehensive reporting'
        ]
    }
    
    # 保存报告
    with open('comprehensive_demo_report.json', 'w', encoding='utf-8') as f:
        json.dump(comprehensive_report, f, indent=2, ensure_ascii=False)
    
    print("   💾 综合报告已保存: comprehensive_demo_report.json")
    
    # 7. 性能和能力总结
    print(f"\n🎯 Inspector Agent 能力总结")
    print("=" * 60)
    
    total_components = sum(
        result['scan_summary']['total_agents'] + 
        result['scan_summary']['total_tools'] +
        result['scan_summary']['total_crews'] +
        result['scan_summary']['total_tasks']
        for result in scan_results.values()
    )
    
    print(f"✅ 已识别组件总数: {total_components}")
    print(f"✅ 支持的框架: CrewAI, AutoGen, 自定义Agent")
    print(f"✅ 分析方法: AST解析 + 正则表达式回退")
    print(f"✅ 输出格式: JSON, 命令行, 交互式")
    print(f"✅ 错误处理: 自动恢复和日志记录")
    
    print(f"\n🚀 核心优势:")
    print(f"   • 高准确性: 基于AST的精确分析")
    print(f"   • 强容错性: 多重分析方法确保可靠性")
    print(f"   • 易扩展性: 模块化设计支持新框架")
    print(f"   • 多接口: CLI、API、交互式界面")
    print(f"   • 实时分析: 快速扫描大型项目")
    
    print("\n" + "=" * 60)
    print("🎉 Inspector Agent 综合演示完成!")
    print("📁 生成的文件:")
    print("   - comprehensive_demo_report.json (综合分析报告)")
    print("   - comprehensive_demo_scan.json (扫描结果)")
    print("💡 Inspector Agent 已准备好为您的Agent项目提供深度洞察!")
    print("=" * 60)


def analyze_project_patterns(result):
    """分析项目架构模式"""
    patterns = []
    summary = result['scan_summary']
    
    # 基于组件数量的模式识别
    if summary['total_crews'] > 0:
        patterns.append("团队协作模式 (Team-based Architecture)")
    
    if summary['total_tools'] > summary['total_agents']:
        patterns.append("工具驱动模式 (Tool-rich Environment)")
    
    if summary['total_agents'] > 5:
        patterns.append("多智能体系统 (Multi-Agent System)")
    
    if summary['total_tasks'] > summary['total_agents'] * 2:
        patterns.append("任务密集型 (Task-intensive Design)")
    
    # 基于Agent类型的模式
    agent_types = {}
    for agent in result['agents']:
        agent_type = agent.get('type', 'unknown')
        agent_types[agent_type] = agent_types.get(agent_type, 0) + 1
    
    if agent_types.get('custom_class', 0) > 0:
        patterns.append("自定义扩展模式 (Custom Extension Pattern)")
    
    if agent_types.get('instance', 0) > agent_types.get('direct_call', 0):
        patterns.append("实例化优先模式 (Instance-first Pattern)")
    
    return patterns


def generate_comparison_summary(scan_results):
    """生成项目对比摘要"""
    summary = {}
    
    for project_name, result in scan_results.items():
        project_summary = result['scan_summary']
        summary[project_name] = {
            'total_components': (
                project_summary['total_agents'] +
                project_summary['total_tools'] +
                project_summary['total_crews'] +
                project_summary['total_tasks']
            ),
            'complexity_score': calculate_complexity_score(project_summary),
            'status': project_summary['scan_status']
        }
    
    return summary


def calculate_complexity_score(summary):
    """计算项目复杂度评分"""
    score = (
        summary['total_agents'] * 2.0 +
        summary['total_tools'] * 1.5 +
        summary['total_crews'] * 3.0 +
        summary['total_tasks'] * 1.0
    )
    return round(score, 2)


if __name__ == "__main__":
    comprehensive_demo()
