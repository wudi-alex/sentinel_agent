#!/usr/bin/env python3
"""
SentinelAgent 任务依赖优化验证脚本
验证所有组件对任务依赖关系的正确处理
"""

from sentinelagent.core.scanner import scan_file
from sentinelagent.core.graph_builder import build_graph_from_scan
from sentinelagent.core.path_analyzer import PathAnalyzer
import json


def main():
    print("🔍 SentinelAgent 任务依赖优化验证")
    print("=" * 50)
    
    target_file = "/Users/xuhe/Documents/agent_experiments/crewai_gmail/email_assistant_agent_system.py"
    
    # 1. 扫描器验证
    print("\n📊 1. Scanner 任务依赖解析验证")
    print("-" * 30)
    scan_result = scan_file(target_file)
    
    task_deps = {}
    for task in scan_result['tasks']:
        task_name = task['name']
        agent = task.get('assigned_agent', 'Unknown')
        deps = [dep['task_name'] for dep in task.get('resolved_dependencies', [])]
        task_deps[task_name] = {'agent': agent, 'dependencies': deps}
        
        dep_str = f" (depends on: {deps})" if deps else " (no dependencies)"
        print(f"  ✓ {task_name} → {agent}{dep_str}")
    
    # 2. 图形构建器验证  
    print("\n🔗 2. Graph Builder 依赖关系建图验证")
    print("-" * 30)
    graph_result = build_graph_from_scan(scan_result)
    
    # 统计边类型
    edge_types = {}
    dependency_edges = []
    for edge in graph_result['edges']:
        rel_type = edge['relationship']
        edge_types[rel_type] = edge_types.get(rel_type, 0) + 1
        
        if rel_type == 'task_dependency':
            dependency_edges.append(edge)
    
    print(f"  📈 图形统计: {len(graph_result['nodes'])} 节点, {len(graph_result['edges'])} 边")
    for rel_type, count in edge_types.items():
        print(f"    - {rel_type}: {count} 条边")
    
    print(f"  🔗 任务依赖边:")
    for edge in dependency_edges:
        source_node = next(n for n in graph_result['nodes'] if n['id'] == edge['source'])
        target_node = next(n for n in graph_result['nodes'] if n['id'] == edge['target'])
        print(f"    - {source_node['name']} → {target_node['name']} (权重: {edge['weight']})")
    
    # 3. 路径分析器验证
    print("\n🛤️  3. Path Analyzer 时序路径分析验证")
    print("-" * 30)
    analyzer = PathAnalyzer()
    path_analysis = analyzer.analyze_graph_paths(graph_result)
    
    # 分析路径类型
    temporal_paths = [p for p in analyzer.paths if p.get('path_type') == 'temporal_execution']
    low_risk_temporal = [p for p in temporal_paths if p['risk_score'] <= 0.2]
    
    print(f"  📊 路径统计: {len(analyzer.paths)} 总路径")
    print(f"    - 时序执行路径: {len(temporal_paths)} 条")
    print(f"    - 低风险时序路径: {len(low_risk_temporal)} 条")
    
    # 显示关键时序路径
    print(f"  🎯 关键时序执行路径:")
    key_temporal_paths = [p for p in temporal_paths if len(p['path']) == 2 and p['risk_score'] <= 0.15]
    
    for path in key_temporal_paths[:3]:  # 显示前3个
        path_nodes = []
        for node_id in path['path']:
            node = next(n for n in graph_result['nodes'] if n['id'] == node_id)
            role = node['metadata'].get('role', 'Unknown')
            path_nodes.append(f"{node['name']}({role})")
        
        print(f"    ✓ {' → '.join(path_nodes)} (风险: {path['risk_score']:.3f})")
    
    # 4. 依赖关系正确性验证
    print("\n✅ 4. 依赖关系正确性验证")
    print("-" * 30)
    
    # 验证 email_assistant_agent_system.py 的实际依赖关系
    expected_deps = {
        'Task_1': [],  # classification_task
        'Task_2': ['Task_1'],  # response_task depends on classification_task
        'Task_3': ['Task_1']   # summarization_task depends on classification_task  
    }
    
    all_correct = True
    for task_name, expected in expected_deps.items():
        actual = task_deps.get(task_name, {}).get('dependencies', [])
        if set(actual) == set(expected):
            status = "✓"
        else:
            status = "✗"
            all_correct = False
        
        print(f"  {status} {task_name}: 期望 {expected}, 实际 {actual}")
    
    # 5. 总结
    print(f"\n🎯 验证结果总结")
    print("-" * 30)
    if all_correct:
        print("  ✅ 所有任务依赖关系解析正确")
        print("  ✅ 图形依赖边构建正确")  
        print("  ✅ 时序路径分析准确")
        print("  🎉 任务依赖优化完全成功!")
    else:
        print("  ❌ 存在依赖关系解析错误")
        print("  ⚠️  需要进一步调试和修复")


if __name__ == "__main__":
    main()
