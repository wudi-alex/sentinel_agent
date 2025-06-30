#!/usr/bin/env python3
"""
图关系可视化工具
将SentinelAgent生成的关系图进行可视化展示
"""

import json
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import matplotlib.patches as mpatches

def visualize_agent_graph(graph_file: str, output_file: str = None):
    """可视化agent系统关系图"""
    
    # 读取图数据
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    # 创建NetworkX图
    G = nx.DiGraph()
    
    # 添加节点
    node_colors = []
    node_labels = {}
    
    for node in graph_data['nodes']:
        node_id = node['id']
        node_type = node['type']
        node_name = node['name']
        
        G.add_node(node_id)
        node_labels[node_id] = node_name
        
        # 根据节点类型设置颜色
        if node_type == 'agent':
            node_colors.append('lightblue')
        elif node_type == 'tool':
            node_colors.append('lightgreen')
        else:
            node_colors.append('lightgray')
    
    # 添加边
    edge_colors = []
    edge_weights = []
    
    for edge in graph_data['edges']:
        source = edge['source']
        target = edge['target']
        relationship = edge['relationship']
        weight = edge.get('weight', 0.5)
        
        G.add_edge(source, target, relationship=relationship, weight=weight)
        
        # 根据关系类型设置边的颜色
        if relationship == 'explicit_usage':
            edge_colors.append('red')
            edge_weights.append(3.0)  # 粗线
        elif relationship == 'same_crew_collaboration':
            edge_colors.append('blue')
            edge_weights.append(2.0)  # 中等粗细
        else:
            edge_colors.append('gray')
            edge_weights.append(1.0)  # 细线
    
    # 创建图形
    plt.figure(figsize=(14, 10))
    
    # 使用spring layout布局
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors, 
                          node_size=2000,
                          alpha=0.8)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos,
                          edge_color=edge_colors,
                          width=edge_weights,
                          alpha=0.6,
                          arrows=True,
                          arrowsize=20)
    
    # 绘制标签
    nx.draw_networkx_labels(G, pos, node_labels, font_size=10, font_weight='bold')
    
    # 创建图例
    agent_patch = mpatches.Patch(color='lightblue', label='Agent')
    tool_patch = mpatches.Patch(color='lightgreen', label='Tool')
    
    explicit_line = mpatches.Patch(color='red', label='Explicit Usage')
    collab_line = mpatches.Patch(color='blue', label='Crew Collaboration')
    proximity_line = mpatches.Patch(color='gray', label='File Proximity')
    
    plt.legend(handles=[agent_patch, tool_patch, explicit_line, collab_line, proximity_line],
              loc='upper left', bbox_to_anchor=(0, 1))
    
    # 设置标题和布局
    plt.title("Agent System Relationship Graph\n" + 
             f"Nodes: {graph_data['graph_summary']['total_nodes']}, " +
             f"Edges: {graph_data['graph_summary']['total_edges']}", 
             fontsize=16, fontweight='bold')
    
    plt.axis('off')
    plt.tight_layout()
    
    # 保存图像
    if output_file is None:
        output_file = f"graph_visualization_{Path(graph_file).stem}.png"
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✅ 图形已保存到: {output_file}")
    
    # 打印图统计信息
    print_graph_statistics(graph_data)

def print_graph_statistics(graph_data):
    """打印图统计信息"""
    print("\n📊 图统计信息:")
    print("=" * 40)
    
    summary = graph_data['graph_summary']
    print(f"总节点数: {summary['total_nodes']}")
    print(f"总边数: {summary['total_edges']}")
    print(f"平均度: {summary.get('average_degree', 'N/A')}")
    
    print(f"\n节点类型分布:")
    for node_type, count in summary['node_types'].items():
        print(f"  {node_type}: {count}")
    
    print(f"\n关系类型分布:")
    for rel_type, count in summary['relationship_types'].items():
        print(f"  {rel_type}: {count}")
    
    print(f"\n🔍 关键关系:")
    # 分析explicit usage关系
    explicit_usage_count = summary['relationship_types'].get('explicit_usage', 0)
    if explicit_usage_count > 0:
        print(f"  ✅ 发现 {explicit_usage_count} 个明确的工具使用关系")
        
        # 查找具体的explicit usage关系
        for edge in graph_data['edges']:
            if edge['relationship'] == 'explicit_usage':
                source_node = next(n for n in graph_data['nodes'] if n['id'] == edge['source'])
                target_node = next(n for n in graph_data['nodes'] if n['id'] == edge['target'])
                print(f"    {source_node['name']} → {target_node['name']}")
    
    print(f"\n🏗️ 架构特征:")
    agent_count = summary['node_types'].get('agent', 0)
    tool_count = summary['node_types'].get('tool', 0)
    
    if tool_count > 0 and agent_count > 0:
        tool_usage_ratio = explicit_usage_count / (agent_count * tool_count)
        print(f"  工具使用率: {tool_usage_ratio:.1%}")
        
        if tool_usage_ratio > 0.5:
            print(f"  🎯 高工具整合度系统")
        elif tool_usage_ratio > 0.2:
            print(f"  🔧 中等工具整合度系统")
        else:
            print(f"  📋 低工具整合度系统")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python graph_visualizer.py <graph_file.json>")
        print("示例: python graph_visualizer.py enhanced_graph.json")
        sys.exit(1)
    
    graph_file = sys.argv[1]
    
    if not Path(graph_file).exists():
        print(f"❌ 文件不存在: {graph_file}")
        sys.exit(1)
    
    print(f"🎨 开始可视化图形: {graph_file}")
    visualize_agent_graph(graph_file)
