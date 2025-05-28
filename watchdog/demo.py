#!/usr/bin/env python3
"""
Inspector Agent - 简单演示脚本
不依赖于完整的CrewAI功能，展示核心扫描能力
"""

import sys
import json
from pathlib import Path
from scanner import AgentSystemScanner
from tools import DirectoryScanTool, FileScanTool, ReportAnalysisTool


def print_banner():
    """打印banner"""
    print("=" * 60)
    print("🔍 Inspector Agent - Agent系统结构扫描器")
    print("   基于CrewAI架构，智能分析agent系统")
    print("=" * 60)


def demo_scan_directory(target_dir):
    """演示目录扫描"""
    print(f"\n📂 正在扫描目录: {target_dir}")
    print("-" * 50)
    
    if not Path(target_dir).exists():
        print(f"❌ 目录不存在: {target_dir}")
        return
    
    # 使用核心扫描器
    scanner = AgentSystemScanner()
    result = scanner.scan_directory(target_dir)
    
    # 显示扫描结果
    summary = result['scan_summary']
    print(f"✅ 扫描完成!")
    print(f"📊 发现:")
    print(f"   🤖 Agents: {summary['total_agents']}")
    print(f"   🔧 Tools: {summary['total_tools']}")
    print(f"   👥 Crews: {summary['total_crews']}")
    print(f"   📋 Tasks: {summary['total_tasks']}")
    print(f"   📄 Files: {summary['total_files']}")
    
    # 详细信息
    if result['agents']:
        print(f"\n🤖 发现的Agents:")
        for agent in result['agents'][:5]:  # 显示前5个
            print(f"   - {agent['name']} ({agent['type']})")
            if 'role' in agent.get('arguments', {}):
                print(f"     角色: {agent['arguments']['role']}")
    
    if result['tools']:
        print(f"\n🔧 发现的Tools:")
        for tool in result['tools'][:5]:  # 显示前5个
            print(f"   - {tool['name']} ({tool['type']})")
    
    # 保存结果
    output_file = f"scan_{Path(target_dir).name}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 详细结果已保存到: {output_file}")
    return output_file


def demo_analysis(scan_file):
    """演示分析功能"""
    print(f"\n📋 正在分析扫描结果...")
    print("-" * 50)
    
    analyzer = ReportAnalysisTool()
    analysis = analyzer._run(scan_file)
    
    # 显示分析结果的前500字符
    print(analysis[:800] + "\n...(更多内容请查看完整分析)" if len(analysis) > 800 else analysis)


def main():
    """主函数"""
    print_banner()
    
    # 可用的演示目标
    demo_targets = {
        '1': '../crewai_gmail',
        '2': '../autogen_magneticone', 
        '3': '.',  # 当前目录
    }
    
    print("\n🎯 请选择要扫描的目标:")
    print("1. CrewAI Gmail项目")
    print("2. AutoGen MagneticOne项目")
    print("3. Inspector项目自身")
    print("4. 自定义路径")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice in demo_targets:
        target = demo_targets[choice]
    elif choice == '4':
        target = input("请输入目标路径: ").strip()
    else:
        print("❌ 无效选择")
        return
    
    # 执行扫描
    output_file = demo_scan_directory(target)
    
    if output_file:
        # 询问是否进行分析
        if input("\n🤔 是否进行详细分析? (y/n): ").lower().startswith('y'):
            demo_analysis(output_file)
    
    print(f"\n🎉 演示完成!")
    print(f"💡 提示: 查看生成的JSON文件获取完整扫描结果")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 用户中断，再见!")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print(f"💡 请检查目标路径是否正确")
