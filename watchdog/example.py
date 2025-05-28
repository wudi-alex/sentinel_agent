#!/usr/bin/env python3
"""
Inspector Agent 使用示例
展示如何使用Inspector Agent扫描不同类型的agent系统
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from inspector import InspectorAgent


def example_scan_crewai_project():
    """示例：扫描CrewAI项目"""
    print("🔍 示例1: 扫描CrewAI Gmail项目")
    print("-" * 50)
    
    inspector = InspectorAgent()
    
    # 扫描crewai_gmail目录
    target_dir = "../crewai_gmail"
    if Path(target_dir).exists():
        result = inspector.scan_directory(target_dir, "crewai_gmail_scan.json")
        print("✅ 扫描完成，结果保存到 crewai_gmail_scan.json")
        print(result)
    else:
        print(f"❌ 目录不存在: {target_dir}")


def example_scan_autogen_project():
    """示例：扫描AutoGen项目文件"""
    print("\n🔍 示例2: 扫描AutoGen文件")
    print("-" * 50)
    
    inspector = InspectorAgent()
    
    # 扫描autogen文件
    target_file = "../autogen_magneticone/autogen_remote_server_upload_file.py"
    if Path(target_file).exists():
        result = inspector.scan_file(target_file, "autogen_scan.json")
        print("✅ 扫描完成，结果保存到 autogen_scan.json")
        print(result)
    else:
        print(f"❌ 文件不存在: {target_file}")


def example_direct_tool_usage():
    """示例：直接使用扫描工具"""
    print("\n🔧 示例3: 直接使用扫描工具")
    print("-" * 50)
    
    from tools import DirectoryScanTool, ReportAnalysisTool
    
    # 直接使用目录扫描工具
    directory_scanner = DirectoryScanTool()
    
    target_dir = "../crewai_gmail"
    if Path(target_dir).exists():
        scan_result = directory_scanner._run(target_dir, "direct_scan.json")
        print("📊 直接扫描结果:")
        print(scan_result)
        
        # 使用报告分析工具
        report_analyzer = ReportAnalysisTool()
        analysis_result = report_analyzer._run("direct_scan.json")
        print("\n📋 分析结果:")
        print(analysis_result)
    else:
        print(f"❌ 目录不存在: {target_dir}")


def demo_scan_current_project():
    """示例：扫描当前项目（watchdog）"""
    print("\n🔍 示例4: 扫描当前Inspector项目")
    print("-" * 50)
    
    inspector = InspectorAgent()
    
    # 扫描当前目录
    current_dir = "."
    result = inspector.scan_directory(current_dir, "inspector_self_scan.json")
    print("✅ 自我扫描完成，结果保存到 inspector_self_scan.json")
    print(result)


if __name__ == "__main__":
    print("🚀 Inspector Agent 示例演示")
    print("=" * 60)
    
    # 如果没有设置OPENAI_API_KEY，使用本地模式
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  未检测到OPENAI_API_KEY，某些功能可能受限")
        print("💡 建议设置API key以获得完整功能")
        print("-" * 60)
    
    try:
        # 运行示例
        example_scan_crewai_project()
        example_scan_autogen_project()
        example_direct_tool_usage()
        demo_scan_current_project()
        
        print("\n" + "=" * 60)
        print("🎉 所有示例运行完成!")
        print("📁 检查生成的JSON文件以查看详细结果")
        
    except Exception as e:
        print(f"❌ 运行示例时出错: {e}")
        print("💡 请确保安装了所需依赖: pip install -r requirements.txt")
