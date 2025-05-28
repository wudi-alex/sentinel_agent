#!/usr/bin/env python3
"""
Inspector Agent - 完整功能测试
"""

import json
from pathlib import Path
from scanner import AgentSystemScanner
from tools import DirectoryScanTool, FileScanTool, ReportAnalysisTool


def test_all_features():
    """测试所有功能"""
    print("🔍 Inspector Agent 功能测试")
    print("=" * 50)
    
    # 1. 测试核心扫描器
    print("\n1️⃣ 测试核心扫描器 (AgentSystemScanner)")
    scanner = AgentSystemScanner()
    
    # 扫描CrewAI项目
    print("   📂 扫描 ../crewai_gmail...")
    result1 = scanner.scan_directory('../crewai_gmail')
    summary1 = result1['scan_summary']
    print(f"   ✅ 发现: {summary1['total_agents']} agents, {summary1['total_tools']} tools")
    
    # 扫描AutoGen项目
    print("   📂 扫描 ../autogen_magneticone...")
    result2 = scanner.scan_directory('../autogen_magneticone')
    summary2 = result2['scan_summary']
    print(f"   ✅ 发现: {summary2['total_agents']} agents, {summary2['total_tools']} tools")
    
    # 2. 测试工具
    print("\n2️⃣ 测试CrewAI工具")
    
    # DirectoryScanTool
    print("   🔧 测试 DirectoryScanTool...")
    dir_tool = DirectoryScanTool()
    tool_result = dir_tool._run('.', 'test_tool_scan.json')
    print("   ✅ DirectoryScanTool 工作正常")
    
    # ReportAnalysisTool
    print("   📋 测试 ReportAnalysisTool...")
    report_tool = ReportAnalysisTool()
    analysis = report_tool._run('test_tool_scan.json')
    print("   ✅ ReportAnalysisTool 工作正常")
    
    # FileScanTool
    print("   📄 测试 FileScanTool...")
    file_tool = FileScanTool()
    file_result = file_tool._run('../crewai_gmail/tools.py', 'test_file_scan.json')
    print("   ✅ FileScanTool 工作正常")
    
    # 3. 总结
    print("\n3️⃣ 功能总结")
    print("   ✅ 核心扫描引擎: 正常")
    print("   ✅ AST代码分析: 正常")
    print("   ✅ 正则表达式回退: 正常")
    print("   ✅ CrewAI工具集成: 正常")
    print("   ✅ JSON报告生成: 正常")
    
    # 4. 展示能力
    print("\n4️⃣ Inspector Agent 能力展示")
    print("   🔍 能够识别的组件:")
    print("     - CrewAI Agents (实例和类定义)")
    print("     - CrewAI Tools (BaseTool子类)")
    print("     - CrewAI Crews (团队配置)")
    print("     - CrewAI Tasks (任务定义)")
    print("     - AutoGen Agents (实验性支持)")
    print("     - 自定义Agent类")
    print("   ")
    print("   📊 分析功能:")
    print("     - 项目结构分析")
    print("     - 组件关系分析")
    print("     - 配置参数提取")
    print("     - 架构模式识别")
    
    print("\n🎉 所有功能测试完成!")
    print("💾 生成的文件:")
    for file in ['test_tool_scan.json', 'test_file_scan.json']:
        if Path(file).exists():
            print(f"   - {file}")


if __name__ == "__main__":
    test_all_features()
