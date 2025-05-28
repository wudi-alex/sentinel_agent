#!/usr/bin/env python3
"""
Inspector Agent - 实时演示脚本
展示Inspector Agent的核心功能
"""

import json
import os
from pathlib import Path
from scanner import AgentSystemScanner


def main():
    """主演示函数"""
    print("🔍 Inspector Agent - 实时功能演示")
    print("=" * 50)
    
    scanner = AgentSystemScanner()
    
    # 演示1: 扫描当前项目
    print("\n1️⃣ 扫描当前Inspector项目:")
    print("-" * 30)
    
    result = scanner.scan_directory('.')
    summary = result['scan_summary']
    
    print(f"📊 发现组件:")
    print(f"   🤖 Agents: {summary['total_agents']}")
    print(f"   🔧 Tools: {summary['total_tools']}")
    print(f"   👥 Crews: {summary['total_crews']}")
    print(f"   📋 Tasks: {summary['total_tasks']}")
    print(f"   📄 Files: {summary['total_files']}")
    
    # 显示发现的组件详情
    if result['agents']:
        print(f"\n🤖 发现的Agents ({len(result['agents'])}):")
        for i, agent in enumerate(result['agents'][:5], 1):
            print(f"   {i}. {agent['name']} ({agent['type']}) - {Path(agent['file']).name}")
    
    if result['tools']:
        print(f"\n🔧 发现的Tools ({len(result['tools'])}):")
        for i, tool in enumerate(result['tools'][:5], 1):
            print(f"   {i}. {tool['name']} ({tool['type']}) - {Path(tool['file']).name}")
    
    # 演示2: 扫描CrewAI项目（如果存在）
    crewai_path = '../crewai_gmail'
    if os.path.exists(crewai_path):
        print(f"\n2️⃣ 扫描CrewAI Gmail项目:")
        print("-" * 30)
        
        crewai_result = scanner.scan_directory(crewai_path)
        crewai_summary = crewai_result['scan_summary']
        
        print(f"📊 发现组件:")
        print(f"   🤖 Agents: {crewai_summary['total_agents']}")
        print(f"   🔧 Tools: {crewai_summary['total_tools']}")
        print(f"   👥 Crews: {crewai_summary['total_crews']}")
        print(f"   📋 Tasks: {crewai_summary['total_tasks']}")
        
        # 显示Agent详情
        if crewai_result['agents']:
            print(f"\n🤖 CrewAI Agents:")
            for agent in crewai_result['agents'][:3]:
                args = agent.get('arguments', {})
                role = args.get('role', 'Unknown Role')
                print(f"   - {agent['name']}: {role}")
    
    # 演示3: 文件级分析
    print(f"\n3️⃣ 单文件分析演示:")
    print("-" * 30)
    
    files_to_analyze = ['scanner.py', 'inspector.py', 'tools.py']
    for filename in files_to_analyze:
        if os.path.exists(filename):
            file_result = scanner.scan_file(filename)
            file_summary = file_result['scan_summary']
            total_components = (file_summary['total_agents'] + 
                              file_summary['total_tools'] + 
                              file_summary['total_crews'] + 
                              file_summary['total_tasks'])
            print(f"   📄 {filename}: {total_components} 个组件")
    
    # 演示4: 项目对比
    print(f"\n4️⃣ 项目对比分析:")
    print("-" * 30)
    
    projects = {
        'Inspector': '.',
        'CrewAI Gmail': '../crewai_gmail',
        'AutoGen': '../autogen_magneticone'
    }
    
    comparison_data = []
    for name, path in projects.items():
        if os.path.exists(path):
            proj_result = scanner.scan_directory(path)
            proj_summary = proj_result['scan_summary']
            comparison_data.append({
                'name': name,
                'agents': proj_summary['total_agents'],
                'tools': proj_summary['total_tools'],
                'total': proj_summary['total_agents'] + proj_summary['total_tools']
            })
    
    # 显示对比表格
    print("项目名称".ljust(15) + "Agents".ljust(8) + "Tools".ljust(8) + "总计")
    print("-" * 40)
    for proj in comparison_data:
        print(f"{proj['name'][:14].ljust(15)}{str(proj['agents']).ljust(8)}{str(proj['tools']).ljust(8)}{proj['total']}")
    
    # 保存演示结果
    demo_result = {
        'timestamp': str(Path.cwd()),
        'inspector_scan': result,
        'comparison': comparison_data
    }
    
    with open('live_demo_result.json', 'w', encoding='utf-8') as f:
        json.dump(demo_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 演示完成!")
    print(f"💾 详细结果已保存到: live_demo_result.json")
    print("=" * 50)


if __name__ == "__main__":
    main()
