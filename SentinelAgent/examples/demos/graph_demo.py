#!/usr/bin/env python3
"""
Graph Building Demo
演示如何从扫描结果构建agent系统关系图
"""

import sys
import json
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
# removed src_path
# removed src_path insert

from scanner import scan_directory
from graph_builder import build_graph_from_scan, build_and_save_graph, scan_and_build_graph


def demo_graph_building():
    """演示图构建功能"""
    print("=== Agent System Graph Builder Demo ===\n")
    
    # 1. 扫描当前目录
    print("1. 扫描当前目录...")
    scan_result = scan_directory('.')
    print(f"   扫描完成: 发现 {scan_result['scan_summary']['total_agents']} 个agents, "
          f"{scan_result['scan_summary']['total_tools']} 个tools, "
          f"{scan_result['scan_summary']['total_crews']} 个crews, "
          f"{scan_result['scan_summary']['total_tasks']} 个tasks")
    
    # 2. 构建图
    print("\n2. 构建关系图...")
    graph_data = build_graph_from_scan(scan_result)
    print(f"   图构建完成: {graph_data['graph_summary']['total_nodes']} 个节点, "
          f"{graph_data['graph_summary']['total_edges']} 条边")
    
    # 3. 显示图统计信息
    print("\n3. 图统计信息:")
    summary = graph_data['graph_summary']
    print(f"   - 节点类型分布: {summary['node_types']}")
    print(f"   - 关系类型分布: {summary['relationship_types']}")
    print(f"   - 平均度数: {summary['average_degree']:.2f}")
    
    # 4. 显示一些具体的节点和边
    print("\n4. 图结构预览:")
    print("   节点示例:")
    for i, node in enumerate(graph_data['nodes'][:3]):  # 显示前3个节点
        print(f"     [{i+1}] {node['type']}: {node['name']} (在 {node['file']})")
        if node['type'] == 'agent':
            crews = node['metadata'].get('crews', [])
            tasks = node['metadata'].get('tasks', [])
            if crews:
                print(f"         所属Crew: {[c['name'] for c in crews]}")
            if tasks:
                print(f"         执行Task: {[t['name'] for t in tasks]}")
    
    if len(graph_data['nodes']) > 3:
        print(f"     ... 还有 {len(graph_data['nodes']) - 3} 个节点")
    
    print("\n   边示例:")
    for i, edge in enumerate(graph_data['edges'][:5]):  # 显示前5条边
        source_node = next(n for n in graph_data['nodes'] if n['id'] == edge['source'])
        target_node = next(n for n in graph_data['nodes'] if n['id'] == edge['target'])
        print(f"     [{i+1}] {source_node['name']} -> {target_node['name']} "
              f"({edge['relationship']}, 权重: {edge['weight']})")
    
    if len(graph_data['edges']) > 5:
        print(f"     ... 还有 {len(graph_data['edges']) - 5} 条边")
    
    # 5. 保存图到文件
    print("\n5. 保存图到文件...")
    output_file = "agent_system_graph.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    print(f"   图已保存到: {output_file}")
    
    return graph_data


def demo_direct_scan_and_build():
    """演示一体化扫描和构建功能"""
    print("\n=== 一体化扫描和构建演示 ===\n")
    
    print("执行一体化扫描和图构建...")
    graph_data = scan_and_build_graph('.', 'complete_agent_graph.json')
    
    print(f"完成! 构建了包含 {graph_data['graph_summary']['total_nodes']} 个节点和 "
          f"{graph_data['graph_summary']['total_edges']} 条边的图")
    print("图已保存到: complete_agent_graph.json")
    
    return graph_data


def analyze_graph_structure(graph_data):
    """分析图结构"""
    print("\n=== 图结构分析 ===\n")
    
    # 计算入度和出度
    in_degree = {}
    out_degree = {}
    
    # 初始化度数
    for node in graph_data['nodes']:
        node_id = node['id']
        in_degree[node_id] = 0
        out_degree[node_id] = 0
    
    # 计算度数
    for edge in graph_data['edges']:
        out_degree[edge['source']] += 1
        in_degree[edge['target']] += 1
    
    # 找出重要节点
    print("最重要的节点 (按出度):")
    sorted_by_out = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)
    for i, (node_id, degree) in enumerate(sorted_by_out[:3]):
        node = next(n for n in graph_data['nodes'] if n['id'] == node_id)
        print(f"  {i+1}. {node['name']} ({node['type']}) - 出度: {degree}")
    
    print("\n最重要的节点 (按入度):")
    sorted_by_in = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)
    for i, (node_id, degree) in enumerate(sorted_by_in[:3]):
        node = next(n for n in graph_data['nodes'] if n['id'] == node_id)
        print(f"  {i+1}. {node['name']} ({node['type']}) - 入度: {degree}")


if __name__ == "__main__":
    # 运行基本演示
    graph_data = demo_graph_building()
    
    # 分析图结构
    analyze_graph_structure(graph_data)
    
    # 运行一体化演示
    demo_direct_scan_and_build()
    
    print("\n=== Demo 完成 ===")
    print("生成的文件:")
    print("- agent_system_graph.json: 基本图构建结果")
    print("- complete_agent_graph.json: 一体化扫描和构建结果")
