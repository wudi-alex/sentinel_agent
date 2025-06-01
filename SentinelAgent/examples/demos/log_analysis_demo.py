#!/usr/bin/env python3
"""
日志分析工具演示

展示如何使用ExecutionLogAnalyzer和LogAnalysisTool进行日志分析
"""

import sys
import os
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from log_analyzer import ExecutionLogAnalyzer
from tools import LogAnalysisTool

def demo_direct_analysis():
    """直接使用ExecutionLogAnalyzer进行分析"""
    print("=== 直接分析演示 ===")
    
    # 创建分析器
    analyzer = ExecutionLogAnalyzer()
    
    # 分析TXT格式日志
    txt_log = "../../autogen_magneticone/logs/log_2025-05-17_17-47-03.txt"
    if Path(txt_log).exists():
        print(f"\n📊 分析TXT日志: {txt_log}")
        result = analyzer.analyze_log_file(txt_log)
        
        print(f"✅ 分析完成:")
        print(f"  - 执行路径: {len(result.execution_paths)}")
        print(f"  - 错误数量: {len(result.errors)}")
        print(f"  - 警告数量: {len(result.warnings)}")
        
        if result.errors:
            print("\n❌ 主要错误:")
            for i, error in enumerate(result.errors[:3], 1):
                print(f"  {i}. {error.error_type} ({error.severity.value}): {error.description}")
        
        # 生成报告
        report = analyzer.generate_report(result, "txt_analysis_report.md")
        print(f"\n📄 详细报告已生成: txt_analysis_report.md")
    
    # 分析CSV格式日志
    csv_log = "../../magentic-one-file-code-execution.csv"
    if Path(csv_log).exists():
        print(f"\n📊 分析CSV日志: {csv_log}")
        result = analyzer.analyze_log_file(csv_log)
        
        print(f"✅ 分析完成:")
        print(f"  - 执行路径: {len(result.execution_paths)}")
        print(f"  - 错误数量: {len(result.errors)}")
        print(f"  - 警告数量: {len(result.warnings)}")
        
        if result.execution_paths:
            print("\n🛣️  执行路径:")
            for i, path in enumerate(result.execution_paths[:3], 1):
                print(f"  路径 {i}: {len(path.nodes)} 个节点, {len(path.log_entries)} 个条目")


def demo_crewai_tool():
    """演示CrewAI工具的使用"""
    print("\n\n=== CrewAI工具演示 ===")
    
    # 创建工具实例
    tool = LogAnalysisTool()
    
    # 使用工具分析日志
    txt_log = "../../autogen_magneticone/logs/log_2025-05-17_17-47-03.txt"
    if Path(txt_log).exists():
        print(f"\n🔧 使用CrewAI工具分析: {txt_log}")
        result = tool._run(
            log_file_path=txt_log,
            log_format="auto",
            output_file="crewai_analysis_result.json"
        )
        
        print("📋 工具分析结果:")
        print(result)


def demo_batch_analysis():
    """批量分析演示"""
    print("\n\n=== 批量分析演示 ===")
    
    analyzer = ExecutionLogAnalyzer()
    
    # 查找所有日志文件
    log_dir = Path("../../autogen_magneticone/logs")
    if log_dir.exists():
        log_files = list(log_dir.glob("*.txt"))
        print(f"📁 发现 {len(log_files)} 个日志文件")
        
        total_errors = 0
        total_warnings = 0
        total_paths = 0
        
        for log_file in log_files[:3]:  # 分析前3个文件
            try:
                print(f"\n📊 分析: {log_file.name}")
                result = analyzer.analyze_log_file(str(log_file))
                
                total_errors += len(result.errors)
                total_warnings += len(result.warnings)
                total_paths += len(result.execution_paths)
                
                print(f"  - 路径: {len(result.execution_paths)}, 错误: {len(result.errors)}, 警告: {len(result.warnings)}")
                
            except Exception as e:
                print(f"  ❌ 分析失败: {e}")
        
        print(f"\n📈 总计:")
        print(f"  - 执行路径: {total_paths}")
        print(f"  - 错误数量: {total_errors}")
        print(f"  - 警告数量: {total_warnings}")


if __name__ == "__main__":
    print("🔍 日志分析工具演示")
    print("=" * 50)
    
    try:
        demo_direct_analysis()
        demo_crewai_tool()
        demo_batch_analysis()
        
        print("\n✅ 演示完成!")
        print("\n💡 提示:")
        print("  - 生成的报告文件可以用Markdown编辑器查看")
        print("  - JSON分析结果可以进一步处理和可视化")
        print("  - 可以集成到CI/CD流程中进行自动化分析")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
