#!/usr/bin/env python3
"""
测试优化后的 Scanner 和 Graph Builder
验证任务分配关系的正确性
"""

from sentinelagent.core.scanner import scan_file
from sentinelagent.core.graph_builder import build_graph_from_scan
import json


def main():
    """测试优化效果"""
    
    print("🔍 SentinelAgent Scanner & Graph Builder 优化验证")
    print("=" * 60)
    
    # 1. 扫描目标文件
    target_file = "/Users/xuhe/Documents/agent_experiments/crewai_gmail/email_assistant_agent_system.py"
    
    print(f"📁 扫描目标: {target_file}")
    scan_result = scan_file(target_file)
    
    # 2. 验证智能体信息
    print(f"\n📊 扫描结果统计:")
    print(f"   智能体数量: {len(scan_result['agents'])}")
    print(f"   工具数量: {len(scan_result['tools'])}")
    print(f"   任务数量: {len(scan_result['tasks'])}")
    print(f"   团队数量: {len(scan_result['crews'])}")
    
    # 3. 验证任务分配关系
    print(f"\n🤖 智能体与任务分配关系:")
    agent_task_mapping = {}
    
    for task in scan_result['tasks']:
        assigned_agent = task.get('assigned_agent')
        if assigned_agent:
            if assigned_agent not in agent_task_mapping:
                agent_task_mapping[assigned_agent] = []
            agent_task_mapping[assigned_agent].append(task['name'])
    
    for agent in scan_result['agents']:
        agent_name = agent['name']
        role = agent.get('arguments', {}).get('role', 'Unknown')
        tasks = agent_task_mapping.get(agent_name, ['无任务分配'])
        
        print(f"   {agent_name} ({role}):")
        for task in tasks:
            print(f"     ✓ {task}")
    
    # 4. 构建图形关系
    print(f"\n🔗 构建关系图...")
    graph_result = build_graph_from_scan(scan_result)
    
    # 5. 验证图形中的任务分配
    print(f"\n📈 图形中的任务分配验证:")
    for node in graph_result['nodes']:
        if node['type'] == 'agent':
            agent_name = node['name']
            role = node['metadata']['role']
            tasks = node['metadata'].get('tasks', [])
            
            print(f"   {agent_name} ({role}):")
            if tasks:
                for task in tasks:
                    task_name = task.get('name', 'Unknown')
                    desc = task.get('description', '')[:50] + '...' if task.get('description') else 'No description'
                    print(f"     ✓ {task_name}: {desc}")
            else:
                print(f"     ❌ 无任务分配")
    
    # 6. 验证工具使用关系
    print(f"\n🛠️  工具使用关系:")
    tool_usage = {}
    
    for edge in graph_result['edges']:
        if edge['relationship'] == 'explicit_usage':
            source_node = next((n for n in graph_result['nodes'] if n['id'] == edge['source']), None)
            target_node = next((n for n in graph_result['nodes'] if n['id'] == edge['target']), None)
            
            if source_node and target_node:
                agent_name = source_node['name']
                tool_name = target_node['name']
                
                if agent_name not in tool_usage:
                    tool_usage[agent_name] = []
                tool_usage[agent_name].append(tool_name)
    
    for agent_name, tools in tool_usage.items():
        print(f"   {agent_name}:")
        for tool in tools:
            print(f"     🔧 {tool}")
    
    print(f"\n✅ 优化验证完成!")
    
    # 7. 保存验证结果
    verification_result = {
        'scan_summary': scan_result['scan_summary'],
        'agent_task_mapping': agent_task_mapping,
        'tool_usage': tool_usage,
        'graph_summary': graph_result['graph_summary'],
        'verification_passed': len(agent_task_mapping) == len(scan_result['agents'])
    }
    
    with open('optimization_verification.json', 'w', encoding='utf-8') as f:
        json.dump(verification_result, f, ensure_ascii=False, indent=2)
    
    print(f"📄 验证报告已保存至: optimization_verification.json")


if __name__ == "__main__":
    main()
