#!/usr/bin/env python3
"""
Inspector Agent - 简化演示脚本
展示核心扫描功能
"""

import sys
import json
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
# removed src_path
# removed src_path insert

from scanner import scan_directory


def print_banner():
    """打印banner"""
    print("=" * 50)
    print("🔍 Inspector Agent - 系统结构扫描器")
    print("=" * 50)


def demo_scan_directory(target_dir):
    """演示目录扫描"""
    print(f"\n📂 正在扫描目录: {target_dir}")
    print("-" * 50)
    
    if not Path(target_dir).exists():
        print(f"❌ 目录不存在: {target_dir}")
        return
    
    # 使用简化的扫描函数
    result = scan_directory(target_dir)
    
    # 显示扫描结果
    summary = result['scan_summary']
    print(f"✅ 扫描完成!")
    print(f"📊 发现: {summary['total_agents']} agents, {summary['total_tools']} tools, {summary['total_files']} files")
    
    # 详细信息
    if result['agents']:
        print(f"\n🤖 发现的Agents (前3个):")
        for agent in result['agents'][:3]:  # 显示前3个
            print(f"   - {agent['name']} ({agent['type']})")
    
    if result['tools']:
        print(f"\n🔧 发现的Tools (前3个):")
        for tool in result['tools'][:3]:  # 显示前3个
            print(f"   - {tool['name']} ({tool['type']})")
    
    # 保存结果
    output_file = f"scan_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 详细结果已保存到: {output_file}")
    return output_file


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
        print(f"\n🎉 演示完成!")
        print(f"💡 提示: 查看生成的JSON文件获取完整扫描结果")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print(f"💡 请检查目标路径是否正确")
