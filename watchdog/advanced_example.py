#!/usr/bin/env python3
"""
Inspector Agent - 高级使用示例
展示Inspector Agent的强大功能和实际应用场景
"""

import json
import os
from pathlib import Path
from scanner import AgentSystemScanner
from tools import DirectoryScanTool, FileScanTool, ReportAnalysisTool


def advanced_comparison_analysis():
    """高级功能：多项目对比分析"""
    print("🔬 Inspector Agent - 高级对比分析")
    print("=" * 60)
    
    scanner = AgentSystemScanner()
    projects = {
        'CrewAI Gmail': '../crewai_gmail',
        'AutoGen MagneticOne': '../autogen_magneticone',
        'Inspector Watchdog': '.'
    }
    
    results = {}
    
    # 扫描所有项目
    print("\n📊 正在扫描多个项目...")
    for name, path in projects.items():
        if os.path.exists(path):
            print(f"   🔍 扫描 {name}...")
            results[name] = scanner.scan_directory(path)
        else:
            print(f"   ⚠️  路径不存在: {path}")
    
    # 生成对比报告
    print("\n📋 生成对比分析报告...")
    comparison_report = generate_comparison_report(results)
    
    # 保存对比报告
    with open('advanced_comparison_report.json', 'w', encoding='utf-8') as f:
        json.dump(comparison_report, f, indent=2, ensure_ascii=False)
    
    # 显示结果
    display_comparison_results(comparison_report)


def generate_comparison_report(results):
    """生成项目对比报告"""
    report = {
        'comparison_summary': {},
        'detailed_analysis': {},
        'architecture_patterns': {},
        'recommendations': []
    }
    
    # 基础统计对比
    for project_name, data in results.items():
        summary = data['scan_summary']
        report['comparison_summary'][project_name] = {
            'agents': summary['total_agents'],
            'tools': summary['total_tools'],
            'crews': summary['total_crews'],
            'tasks': summary['total_tasks'],
            'files': summary['total_files'],
            'complexity_score': calculate_complexity_score(data)
        }
    
    # 架构模式分析
    for project_name, data in results.items():
        patterns = analyze_architecture_patterns(data)
        report['architecture_patterns'][project_name] = patterns
    
    # 生成建议
    report['recommendations'] = generate_recommendations(results)
    
    return report


def calculate_complexity_score(data):
    """计算项目复杂度评分"""
    summary = data['scan_summary']
    # 简单的复杂度评分算法
    score = (summary['total_agents'] * 2 + 
             summary['total_tools'] * 1.5 + 
             summary['total_crews'] * 3 + 
             summary['total_tasks'] * 1)
    return round(score, 2)


def analyze_architecture_patterns(data):
    """分析架构模式"""
    patterns = {
        'agent_types': {},
        'tool_usage': {},
        'crew_organization': {},
        'design_patterns': []
    }
    
    # 分析Agent类型
    for agent in data['agents']:
        agent_type = agent.get('type', 'unknown')
        patterns['agent_types'][agent_type] = patterns['agent_types'].get(agent_type, 0) + 1
    
    # 分析Tool使用
    for tool in data['tools']:
        tool_type = tool.get('type', 'unknown')
        patterns['tool_usage'][tool_type] = patterns['tool_usage'].get(tool_type, 0) + 1
    
    # 识别设计模式
    if data['scan_summary']['total_crews'] > 0:
        patterns['design_patterns'].append('Team-based Organization')
    
    if data['scan_summary']['total_tools'] > data['scan_summary']['total_agents']:
        patterns['design_patterns'].append('Tool-Rich Environment')
    
    if data['scan_summary']['total_agents'] > 5:
        patterns['design_patterns'].append('Multi-Agent System')
    
    return patterns


def generate_recommendations(results):
    """生成优化建议"""
    recommendations = []
    
    for project_name, data in results.items():
        summary = data['scan_summary']
        
        # 基于统计的建议
        if summary['total_tools'] == 0:
            recommendations.append({
                'project': project_name,
                'type': 'enhancement',
                'message': '建议增加工具来提高Agent能力'
            })
        
        if summary['total_crews'] == 0 and summary['total_agents'] > 2:
            recommendations.append({
                'project': project_name,
                'type': 'organization',
                'message': '建议使用Crew来组织多个Agent'
            })
        
        if summary['total_agents'] > 10:
            recommendations.append({
                'project': project_name,
                'type': 'optimization',
                'message': '大量Agent可能需要考虑性能优化'
            })
    
    return recommendations


def display_comparison_results(report):
    """显示对比分析结果"""
    print("\n" + "=" * 60)
    print("📈 项目对比分析结果")
    print("=" * 60)
    
    # 显示统计对比
    print("\n📊 基础统计对比:")
    print("项目名称".ljust(20) + "Agents".ljust(8) + "Tools".ljust(8) + "Crews".ljust(8) + "Tasks".ljust(8) + "复杂度")
    print("-" * 60)
    
    for project, stats in report['comparison_summary'].items():
        print(f"{project[:19].ljust(20)}{str(stats['agents']).ljust(8)}{str(stats['tools']).ljust(8)}{str(stats['crews']).ljust(8)}{str(stats['tasks']).ljust(8)}{stats['complexity_score']}")
    
    # 显示架构模式
    print("\n🏗️ 架构模式分析:")
    for project, patterns in report['architecture_patterns'].items():
        print(f"\n{project}:")
        if patterns['design_patterns']:
            print(f"  设计模式: {', '.join(patterns['design_patterns'])}")
        print(f"  Agent类型分布: {patterns['agent_types']}")
        print(f"  Tool类型分布: {patterns['tool_usage']}")
    
    # 显示建议
    if report['recommendations']:
        print("\n💡 优化建议:")
        for rec in report['recommendations']:
            print(f"  🎯 {rec['project']}: {rec['message']}")


def demonstrate_file_analysis():
    """演示单文件深度分析"""
    print("\n" + "=" * 60)
    print("🔍 单文件深度分析演示")
    print("=" * 60)
    
    # 分析核心文件
    scanner = AgentSystemScanner()
    files_to_analyze = [
        ('scanner.py', '核心扫描引擎'),
        ('inspector.py', 'Inspector Agent主类'),
        ('tools.py', 'CrewAI工具集')
    ]
    
    for filename, description in files_to_analyze:
        if os.path.exists(filename):
            print(f"\n📄 分析 {filename} ({description}):")
            result = scanner.scan_file(filename)
            summary = result['scan_summary']
            
            print(f"  发现组件: {summary['total_agents']} agents, {summary['total_tools']} tools")
            
            # 显示详细信息
            if result['agents']:
                print("  🤖 Agents:")
                for agent in result['agents'][:3]:  # 只显示前3个
                    print(f"    - {agent['name']} ({agent['type']})")
            
            if result['tools']:
                print("  🔧 Tools:")
                for tool in result['tools'][:3]:  # 只显示前3个
                    print(f"    - {tool['name']} ({tool['type']})")


def performance_benchmark():
    """性能基准测试"""
    print("\n" + "=" * 60)
    print("⚡ 性能基准测试")
    print("=" * 60)
    
    import time
    
    scanner = AgentSystemScanner()
    test_paths = [
        ('../crewai_gmail', 'CrewAI Gmail'),
        ('.', 'Inspector Watchdog')
    ]
    
    for path, name in test_paths:
        if os.path.exists(path):
            print(f"\n🏃‍♂️ 测试 {name}...")
            
            start_time = time.time()
            result = scanner.scan_directory(path)
            end_time = time.time()
            
            duration = end_time - start_time
            summary = result['scan_summary']
            
            print(f"  ⏱️  扫描时间: {duration:.2f}秒")
            print(f"  📊 发现组件: {summary['total_agents'] + summary['total_tools'] + summary['total_crews'] + summary['total_tasks']} 个")
            print(f"  🚀 扫描速度: {(summary['total_agents'] + summary['total_tools'] + summary['total_crews'] + summary['total_tasks']) / duration:.1f} 组件/秒")


def main():
    """主函数"""
    print("🚀 Inspector Agent - 高级功能演示")
    print("=" * 60)
    
    try:
        # 1. 多项目对比分析
        advanced_comparison_analysis()
        
        # 2. 单文件深度分析
        demonstrate_file_analysis()
        
        # 3. 性能基准测试
        performance_benchmark()
        
        print("\n" + "=" * 60)
        print("✅ 高级功能演示完成!")
        print("📁 生成的文件:")
        print("  - advanced_comparison_report.json")
        print("💡 提示: 查看JSON文件获取完整分析数据")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")


if __name__ == "__main__":
    main()
