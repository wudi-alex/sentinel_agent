#!/usr/bin/env python3
"""
Inspector Agent Demo - 增强版本
展示扫描和图构建功能
"""

import sys
import json
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
# removed src_path
# removed src_path insert

from scanner import scan_directory, scan_file
from graph_builder import build_graph_from_scan, scan_and_build_graph


def demo_basic_scanning():
    """基础扫描演示"""
    print("=== 基础扫描演示 ===\n")
    
    # 扫描当前目录
    print("正在扫描当前目录...")
    result = scan_directory('.')
    
    # 显示结果
    summary = result['scan_summary']
    print(f"扫描完成! 发现:")
    print(f"  🤖 Agents: {summary['total_agents']}")
    print(f"  🔧 Tools: {summary['total_tools']}")
    print(f"  👥 Crews: {summary['total_crews']}")
    print(f"  📋 Tasks: {summary['total_tasks']}")
    print(f"  📄 Python文件: {summary['python_files']}")
    
    return result


def demo_graph_building(scan_result):
    """图构建演示"""
    print("\n=== 图构建演示 ===\n")
    
    print("正在构建关系图...")
    graph_data = build_graph_from_scan(scan_result)
    
    summary = graph_data['graph_summary']
    print(f"图构建完成!")
    print(f"  📊 节点总数: {summary['total_nodes']}")
    print(f"  🔗 边总数: {summary['total_edges']}")
    print(f"  📈 平均度数: {summary['average_degree']:.2f}")
    
    print(f"\n节点类型分布:")
    for node_type, count in summary['node_types'].items():
        print(f"  {node_type}: {count}")
    
    print(f"\n关系类型分布:")
    for rel_type, count in summary['relationship_types'].items():
        print(f"  {rel_type}: {count}")
    
    return graph_data


def demo_file_scanning():
    """文件扫描演示"""
    print("\n=== 文件扫描演示 ===\n")
    
    print("正在扫描 scanner.py 文件...")
    result = scan_file('scanner.py')
    
    summary = result['scan_summary']
    print(f"文件扫描完成! 发现:")
    print(f"  🤖 Agents: {summary['total_agents']}")
    print(f"  🔧 Tools: {summary['total_tools']}")
    print(f"  👥 Crews: {summary['total_crews']}")
    print(f"  📋 Tasks: {summary['total_tasks']}")


def demo_integrated_workflow():
    """一体化工作流演示"""
    print("\n=== 一体化工作流演示 ===\n")
    
    print("执行一体化扫描和图构建...")
    graph_data = scan_and_build_graph('.', 'demo_complete_graph.json')
    
    print(f"✅ 完成! 生成了包含 {graph_data['graph_summary']['total_nodes']} 个节点的图")
    print("📁 结果已保存到: demo_complete_graph.json")


def interactive_demo():
    """交互式演示"""
    print("🔍 Inspector Agent - 交互式演示")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 基础目录扫描")
        print("2. 图构建演示")
        print("3. 文件扫描演示")
        print("4. 一体化工作流")
        print("5. 查看生成的文件")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == '0':
            print("感谢使用 Inspector Agent!")
            break
        elif choice == '1':
            scan_result = demo_basic_scanning()
            
            # 询问是否构建图
            if input("\n是否构建关系图? (y/n): ").lower().startswith('y'):
                demo_graph_building(scan_result)
                
        elif choice == '2':
            print("首先需要执行扫描...")
            scan_result = demo_basic_scanning()
            demo_graph_building(scan_result)
            
        elif choice == '3':
            demo_file_scanning()
            
        elif choice == '4':
            demo_integrated_workflow()
            
        elif choice == '5':
            import os
            json_files = [f for f in os.listdir('.') if f.endswith('.json')]
            if json_files:
                print(f"\n生成的JSON文件:")
                for i, file in enumerate(json_files, 1):
                    size = os.path.getsize(file) / 1024  # KB
                    print(f"  {i}. {file} ({size:.1f} KB)")
            else:
                print("\n暂无生成的JSON文件")
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    interactive_demo()
