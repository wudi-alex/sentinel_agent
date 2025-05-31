#!/usr/bin/env python3
"""
Inspector Agent 使用示例
展示如何使用扫描功能
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from scanner import scan_directory, scan_file


def example_scan_crewai_project():
    """示例：扫描CrewAI项目"""
    print("🔍 示例1: 扫描CrewAI Gmail项目")
    print("-" * 50)
    
    # 扫描crewai_gmail目录
    target_dir = "../crewai_gmail"
    if Path(target_dir).exists():
        result = scan_directory(target_dir)
        print("✅ 扫描完成")
        print(f"📊 发现: {result['scan_summary']['total_agents']} agents, {result['scan_summary']['total_tools']} tools")
    else:
        print(f"❌ 目录不存在: {target_dir}")


def example_scan_autogen_project():
    """示例：扫描AutoGen项目文件"""
    print("\n🔍 示例2: 扫描AutoGen文件")
    print("-" * 50)
    
    # 扫描autogen文件
    target_file = "../autogen_magneticone/autogen_remote_server_upload_file.py"
    if Path(target_file).exists():
        result = scan_file(target_file)
        print("✅ 扫描完成")
        print(f"📊 发现: {len(result.get('agents', []))} agents, {len(result.get('tools', []))} tools")
    else:
        print(f"❌ 文件不存在: {target_file}")


def demo_scan_current_project():
    """示例：扫描当前项目（watchdog）"""
    print("\n🔍 示例3: 扫描当前Inspector项目")
    print("-" * 50)
    
    # 扫描当前目录
    current_dir = "."
    result = scan_directory(current_dir)
    print("✅ 自我扫描完成")
    print(f"📊 发现: {result['scan_summary']['total_agents']} agents, {result['scan_summary']['total_tools']} tools")


if __name__ == "__main__":
    print("🚀 Inspector Agent 示例演示")
    print("=" * 50)
    
    try:
        # 运行示例
        example_scan_crewai_project()
        example_scan_autogen_project()
        demo_scan_current_project()
        
        print("\n" + "=" * 50)
        print("🎉 所有示例运行完成!")
        
    except Exception as e:
        print(f"❌ 运行示例时出错: {e}")
        print("💡 请确保安装了所需依赖: pip install -r requirements.txt")
