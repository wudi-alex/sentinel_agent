#!/usr/bin/env python3
"""
路径分析演示
展示agent系统路径分析功能
"""

import sys
import json
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from inspector import InspectorAgent
from graph_builder import scan_and_build_graph
from path_analyzer import analyze_paths_from_file, analyze_graph_paths


def demo_complete_analysis():
    """演示完整的分析流程"""
    print("=" * 60)
    print("路径分析演示 - 完整分析流程")
    print("=" * 60)
    
    # 创建Inspector
    inspector = InspectorAgent()
    
    # 分析当前目录
    current_dir = str(Path.cwd())
    print(f"分析目录: {current_dir}")
    
    # 执行完整分析
    result = inspector.comprehensive_analysis(
        target_path=current_dir,
        scan_output="demo_scan.json",
        graph_output="demo_graph.json", 
        path_output="demo_paths.json"
    )
    
    # 显示路径分析结果摘要
    path_analysis = result['path_analysis']
    overall = path_analysis.get('overall_assessment', {})
    
    print("\n" + "=" * 40)
    print("路径分析结果摘要")
    print("=" * 40)
    print(f"总体风险评分: {overall.get('total_risk_score', 0)}")
    print(f"风险等级: {overall.get('risk_level', 'unknown')}")
    print(f"分析路径数: {overall.get('total_paths_analyzed', 0)}")
    print(f"发现可疑模式: {overall.get('suspicious_patterns_found', 0)}")
    
    # 显示节点状态分布
    node_analysis = path_analysis.get('node_analysis', {})
    node_states = node_analysis.get('node_state_distribution', {})
    print(f"\n节点状态分布:")
    for state, count in node_states.items():
        print(f"  {state}: {count}")
    
    # 显示可疑模式
    patterns = path_analysis.get('suspicious_patterns', [])
    if patterns:
        print(f"\n发现的可疑模式:")
        for i, pattern in enumerate(patterns, 1):
            print(f"  {i}. {pattern.get('pattern_type', 'unknown')} "
                  f"(严重程度: {pattern.get('severity', 'unknown')})")
            print(f"     {pattern.get('details', '')}")
    
    # 显示建议
    recommendations = path_analysis.get('recommendations', [])
    if recommendations:
        print(f"\n改进建议:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    return result


def demo_path_types_analysis():
    """演示路径类型分析"""
    print("\n" + "=" * 60)
    print("路径类型分析演示")
    print("=" * 60)
    
    # 检查是否有现有的图文件
    graph_file = "demo_graph.json"
    if not Path(graph_file).exists():
        print(f"图文件 {graph_file} 不存在，先执行完整分析...")
        demo_complete_analysis()
    
    # 读取图数据
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    # 执行路径分析
    path_analysis = analyze_graph_paths(graph_data)
    
    # 显示路径类型分布
    path_types = path_analysis.get('path_analysis', {}).get('path_type_distribution', {})
    print("路径类型分布:")
    for path_type, count in path_types.items():
        print(f"  {path_type}: {count}")
    
    # 显示详细路径信息
    detailed_paths = path_analysis.get('path_analysis', {}).get('detailed_paths', [])
    print(f"\n详细路径信息 (共 {len(detailed_paths)} 条):")
    
    for i, path_info in enumerate(detailed_paths[:5], 1):  # 只显示前5条
        print(f"\n路径 {i}:")
        print(f"  路径: {' -> '.join(path_info['path'])}")
        print(f"  类型: {path_info['path_type']}")
        print(f"  长度: {path_info['length']}")
        print(f"  风险评分: {path_info['risk_score']:.3f}")
    
    if len(detailed_paths) > 5:
        print(f"\n... 还有 {len(detailed_paths) - 5} 条路径")


def demo_anomaly_detection():
    """演示异常检测功能"""
    print("\n" + "=" * 60)
    print("异常检测演示")
    print("=" * 60)
    
    # 检查是否有路径分析文件
    paths_file = "demo_paths.json"
    if not Path(paths_file).exists():
        print(f"路径分析文件 {paths_file} 不存在，先执行完整分析...")
        demo_complete_analysis()
    
    # 读取路径分析数据
    with open(paths_file, 'r', encoding='utf-8') as f:
        path_analysis = json.load(f)
    
    # 分析异常模式
    patterns = path_analysis.get('suspicious_patterns', [])
    
    print(f"检测到 {len(patterns)} 个可疑模式:")
    
    for i, pattern in enumerate(patterns, 1):
        print(f"\n异常模式 {i}:")
        print(f"  类型: {pattern.get('pattern_type', 'unknown')}")
        print(f"  严重程度: {pattern.get('severity', 'unknown')}")
        print(f"  描述: {pattern.get('description', '')}")
        print(f"  详情: {pattern.get('details', '')}")
        
        # 显示受影响的节点/边
        if 'affected_nodes' in pattern:
            print(f"  受影响节点: {', '.join(pattern['affected_nodes'])}")
        if 'affected_edges' in pattern:
            print(f"  受影响边数量: {len(pattern['affected_edges'])}")
        if 'affected_paths' in pattern:
            print(f"  受影响路径数量: {len(pattern['affected_paths'])}")
    
    # 分析风险分布
    risk_dist = path_analysis.get('path_analysis', {}).get('risk_score_distribution', {})
    total_paths = sum(risk_dist.values())
    
    if total_paths > 0:
        print(f"\n风险评分分布:")
        print(f"  低风险 (<0.3): {risk_dist.get('low', 0)} ({risk_dist.get('low', 0)/total_paths*100:.1f}%)")
        print(f"  中风险 (0.3-0.7): {risk_dist.get('medium', 0)} ({risk_dist.get('medium', 0)/total_paths*100:.1f}%)")
        print(f"  高风险 (>0.7): {risk_dist.get('high', 0)} ({risk_dist.get('high', 0)/total_paths*100:.1f}%)")


def demo_security_insights():
    """演示安全洞察功能"""
    print("\n" + "=" * 60)
    print("安全洞察演示")
    print("=" * 60)
    
    # 检查是否有路径分析文件
    paths_file = "demo_paths.json"
    if not Path(paths_file).exists():
        print(f"路径分析文件 {paths_file} 不存在，先执行完整分析...")
        demo_complete_analysis()
    
    # 读取路径分析数据
    with open(paths_file, 'r', encoding='utf-8') as f:
        path_analysis = json.load(f)
    
    overall = path_analysis.get('overall_assessment', {})
    
    print("安全评估摘要:")
    print(f"  总体风险评分: {overall.get('total_risk_score', 0):.3f}")
    print(f"  风险等级: {overall.get('risk_level', 'unknown').upper()}")
    
    # 安全建议
    recommendations = path_analysis.get('recommendations', [])
    if recommendations:
        print(f"\n安全建议:")
        for i, rec in enumerate(recommendations, 1):
            # 根据建议内容确定优先级
            priority = "HIGH" if "CRITICAL" in rec else "MEDIUM" if "Review" in rec else "LOW"
            print(f"  [{priority}] {rec}")
    
    # 节点安全状态
    node_analysis = path_analysis.get('node_analysis', {})
    nodes_with_states = node_analysis.get('nodes_with_states', {})
    suspicious_nodes = [nid for nid, state in nodes_with_states.items() if state == 'suspicious']
    
    if suspicious_nodes:
        print(f"\n需要关注的可疑节点:")
        for node_id in suspicious_nodes[:5]:  # 只显示前5个
            print(f"  - {node_id}")
        if len(suspicious_nodes) > 5:
            print(f"  ... 还有 {len(suspicious_nodes) - 5} 个")
    
    # 边安全状态
    edge_analysis = path_analysis.get('edge_analysis', {})
    edge_dist = edge_analysis.get('edge_state_distribution', {})
    
    print(f"\n连接安全状态:")
    for state, count in edge_dist.items():
        print(f"  {state}: {count}")


def interactive_demo():
    """交互式演示"""
    print("\n" + "=" * 60)
    print("交互式路径分析演示")
    print("=" * 60)
    
    while True:
        print("\n选择演示选项:")
        print("1. 完整分析流程")
        print("2. 路径类型分析")
        print("3. 异常检测演示")
        print("4. 安全洞察演示")
        print("5. 分析自定义目录")
        print("0. 退出")
        
        choice = input("\n请选择 (0-5): ").strip()
        
        if choice == '0':
            print("演示结束！")
            break
        elif choice == '1':
            demo_complete_analysis()
        elif choice == '2':
            demo_path_types_analysis()
        elif choice == '3':
            demo_anomaly_detection()
        elif choice == '4':
            demo_security_insights()
        elif choice == '5':
            target_dir = input("请输入要分析的目录路径: ").strip()
            if target_dir and Path(target_dir).exists():
                inspector = InspectorAgent()
                inspector.comprehensive_analysis(target_dir)
            else:
                print("目录不存在！")
        else:
            print("无效选择，请重试。")


if __name__ == "__main__":
    # 运行所有演示
    print("路径分析系统演示")
    print("这个演示将展示agent系统路径分析的各项功能")
    
    try:
        # 1. 完整分析
        demo_complete_analysis()
        
        # 2. 路径类型分析
        demo_path_types_analysis()
        
        # 3. 异常检测
        demo_anomaly_detection()
        
        # 4. 安全洞察
        demo_security_insights()
        
        # 5. 交互式演示
        interactive_demo()
        
    except KeyboardInterrupt:
        print("\n\n演示被用户中断。")
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
